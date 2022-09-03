from rest_framework import serializers
from .models import Course, Comment, CourseSelection, Episode
from users.serializer import UserSerializer

class CourseDisplaySerializer(serializers.ModelSerializer):
    student_no = serializers.IntegerField(source='get_enrolled_student')
    author = UserSerializer()
    image_url =serializers.CharField(source='get_absolute_image_url')

    class Meta:
        model = Course
        fields = [
            'title', 'course_uuid', 'student_no', 'author', 'price', 'image_url'
        ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = [
            'id'
        ]

class EpisodeUnpaidSerialser(serializers.ModelSerializer):
    length =  serializers.CharField(source='get_video_length_time')
    class Meta:
        model= Episode
        exclude = [
            'file',
        ]
class EpisodepaidSerialser(serializers.ModelSerializer):
    length =  serializers.CharField(source='get_video_length_time')
    class Meta:
        model= Episode
        fields = '__all__'
        
class CourseSectionUnPaidSerializer(serializers.ModelSerializer):
    episodes  = EpisodeUnpaidSerialser(many=True)
    total_duration = serializers.CharField(source='total_length')
    class Meta:
        model = CourseSelection
        fields = [
            'section_title',
            'episodes',
            'total_duration'
        ]

class CourseSectionPaidSerializer(serializers.ModelSerializer):
    episodes  = EpisodepaidSerialser(many=True)
    total_duration = serializers.CharField(source='total_length')
    class Meta:
        model = CourseSelection
        fields = [
            'section_title',
            'episodes',
            'total_duration'
        ]


class CourseUnpaidSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    author=UserSerializer()
    course_section= CourseSectionUnPaidSerializer(many=True)
    student_no = serializers.IntegerField(source='get_enrolled_student')
    total_lectures=serializers.IntegerField(source='get_total_lectures')
    total_duration = serializers.CharField(source='total_course_length')
    image_url = serializers.CharField(source='get_absolute_image_url')
    class Meta:
        model = Course
        exclude = [
            'id'
        ]

class CoursePaidSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    author=UserSerializer()
    course_section= CourseSectionUnPaidSerializer(many=True)
    student_no = serializers.IntegerField(source='get_enrolled_student')
    total_lectures=serializers.IntegerField(source='get_total_lectures')
    total_duration = serializers.CharField(source='total_course_length')
    image_url = serializers.CharField(source='get_absolute_image_url')
    class Meta:
        model = Course
        exclude = [
            'id'
        ]


class CourseListSerializer(serializers.ModelSerializer):
    student_no  = serializers.CharField(source='get_enrolled_student')
    image_url = serializers.CharField(source='get_absolute_image_url')
    author = UserSerializer()
    total_lectures = serializers.CharField(source='get_total_lectures')
    description = serializers.CharField(source='get_brief_description')
    class Meta:
        model = Course
        fields = [

            'course_uuid',
            'title',
            'student_no',
            'price',
            'author',
            'image_url',
            'description',
            'total_lectures'
        ]


class CartItemSerailizer(serializers.ModelSerializer):
    author = UserSerializer()
    image_url = serializers.CharField(source='get_absolute_image_url')

    class Meta:
        model = Course
        fields = [
            'author', 'title', 'price', 'image_url'
        ]


