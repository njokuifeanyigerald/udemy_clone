from django.urls import path
from .views import (CourseHomeView, CourseDetailView,SectorCourse,
                     SearchCourse,AddComment,GetCartDetail,CourseStudy
)



urlpatterns = [
    path('', CourseHomeView.as_view()),
    path('details/<uuid:course_uuid>/', CourseDetailView.as_view()),
    path('study/<uuid:course_uuid>/', CourseStudy.as_view()),
    path('comments/<uuid:course_uuid>/', AddComment.as_view()),
    path('sector/<uuid:sector_uuid>/', SectorCourse.as_view()),
    path('search/<str:search>/', SearchCourse.as_view()),
    path('cart/', GetCartDetail.as_view()),
]