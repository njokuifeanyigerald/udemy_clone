from decimal import Decimal
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from courses.serializer import ( 
    CourseDisplaySerializer, CourseUnpaidSerializer,CourseListSerializer, 
    CommentSerializer,CartItemSerailizer, CoursePaidSerializer
    )
from .models import Sector, Course
from users.models import User 
from django.db.models import Q

import json


class CourseHomeView(APIView):
    def get(self, request, *args, **kwargs):
        # to make it random and slice and output 6
        sectors = Sector.objects.order_by("?")[:6]

        sector_response = []

        for sector in sectors:
            sector_courses = sector.related_courses.order_by("?")[:4]
            course_Serializer =  CourseDisplaySerializer(sector_courses, many=True)

            sector_obj = {
                "sector_name": sector.name,
                'sector_uuid': sector.sector_uuid,
                'featured_courses': course_Serializer.data,
                'sector_image': sector.get_image_absolute_url()

            }
            sector_response.append(sector_obj)
        return Response(data=sector_response, status=status.HTTP_200_OK)


class CourseDetailView(APIView):
    def get(self, request, course_uuid,*args, **kwargs):
        course= Course.objects.filter(course_uuid=course_uuid)

        if not course:
            return HttpResponseNotFound('course does not exist')
        
        serializer = CourseUnpaidSerializer(course[0])

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class SectorCourse(APIView):
    def get(self, request, sector_uuid, *args, **kwargs):
        sector = Sector.objects.filter(sector_uuid=sector_uuid)
        if not sector:
            return HttpResponseNotFound('sector does not exist')
            # because of manay to many fiels of rwlated courses in the sector model
        sector_courses = sector[0].related_courses.all()
        serializer  = CourseListSerializer(sector_courses, many=True)

        total_students = 0

        for course in sector_courses:
            total_students += course.get_enrolled_student()
        return Response({
            'data': serializer.data,
            'sector_name': sector[0].name,
            'total_students': total_students
        }, status=status.HTTP_200_OK)


class SearchCourse(APIView):
    def get(self, request, search):
        matches = Course.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if not matches:
            return HttpResponseNotFound('search term not found in the database')
        serializer = CourseListSerializer(matches, many=True)
        return Response(data=serializer.data ,status=status.HTTP_200_OK)


class AddComment(APIView):
    def post(self, request,course_uuid,*args,**kwargs):
        try:
            course = Course.objects.get(course_uuid=course_uuid)
        except Course.DoesNotExist:
            return HttpResponseNotFound('course does not exist')

        try:
            content = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return Response("error: pls provide a body", status=status.HTTP_400_BAD_REQUEST)

        if not content.get('message'):
            return HttpResponseBadRequest('input message')

        serializer =  CommentSerializer(data=content)

        if serializer.is_valid():
            # author = User.Objects.get(id=1)
            # comment= serializer.save(user=author)
            comment = serializer.save(user=self.request.user)
            course.comments.add(comment)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetCartDetail(APIView):
    def post(self, request):
        try:
            body = json.loads(request.body)

        except json.decoder.JSONDecodeError:
            return HttpResponseBadRequest()
        
        # because a cart should a list of course uuids
        if type(body.get('cart')) != list:
            return HttpResponseBadRequest()

        if len(body.get("cart")) == 0:
            return Response("message: no item found in cart", status=status.HTTP_200_OK)

        courses = []
        for uuid in body.get('cart'):
            item  = Course.objects.filter(course_uuid=uuid)

            if not item:
                return HttpResponseBadRequest("item not found")

            courses.append(item[0])

        serializer = CartItemSerailizer(courses, many=True)

        cart_total = Decimal(0.00)
        for item in serializer.data:
            cart_total= Decimal(item.get('price'))

        
        context = {
            'cart_detail': serializer.data,
            'cart_total': cart_total
        }

        return Response(data=context, status=status.HTTP_200_OK)

class CourseStudy(APIView):
    def get(self, request, course_uuid):
        try:
            course = Course.objects.filter(course_uuid=course_uuid)
        except Course.DoesNotExist:
            return HttpResponseNotFound("course does not exist")

        # to remove later
        if request.user.is_authenticated:
            # request.user = User.objects.get(id=1)
            user_course = request.user.paid_courses.filter(course_uuid=course_uuid)

            if not user_course:
                return HttpResponseNotAllowed('user does not own this course')
        else:
            return Response("user is not authenticated")
            

        serializer = CoursePaidSerializer(course[0])

        return Response(serializer.data, status.HTTP_200_OK)
        

