from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)
router.register(r'assessments', views.AssessmentViewSet)
router.register(r'attendance', views.AttendanceRecordViewSet)
router.register(r'performance-metrics', views.PerformanceMetricsViewSet)
router.register(r'student-performance', views.StudentPerformanceMetricsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
] 