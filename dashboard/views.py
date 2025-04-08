from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Student, Course, Enrollment, Assessment,
    AttendanceRecord, PerformanceMetrics, StudentPerformanceMetrics
)
from .serializers import (
    StudentSerializer, CourseSerializer, EnrollmentSerializer,
    AssessmentSerializer, AttendanceRecordSerializer,
    PerformanceMetricsSerializer, StudentPerformanceMetricsSerializer
)

# Create your views here.

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['gender', 'race_ethnicity', 'parental_education', 'lunch_type']
    ordering_fields = ['math_score', 'reading_score', 'writing_score']

    @action(detail=True)
    def performance_summary(self, request, pk=None):
        student = self.get_object()
        enrollments = Enrollment.objects.filter(student=student)
        
        summary = {
            'average_scores': {
                'math': student.math_score,
                'reading': student.reading_score,
                'writing': student.writing_score,
                'overall': student.average_score
            },
            'course_performance': enrollments.aggregate(
                avg_grade=Avg('final_grade'),
                courses_taken=Count('id')
            ),
            'attendance': AttendanceRecord.objects.filter(
                enrollment__student=student
            ).aggregate(
                attendance_rate=Avg('present')
            )
        }
        return Response(summary)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'credits']
    search_fields = ['course_code', 'course_name']

    @action(detail=True)
    def course_stats(self, request, pk=None):
        course = self.get_object()
        enrollments = Enrollment.objects.filter(course=course)
        
        stats = {
            'total_students': enrollments.count(),
            'grade_distribution': enrollments.exclude(
                final_grade__isnull=True
            ).aggregate(
                avg_grade=Avg('final_grade'),
                passing_rate=Count('id', filter=models.Q(final_grade__gte=60)) / Count('id')
            ),
            'assessment_stats': Assessment.objects.filter(
                enrollment__course=course
            ).aggregate(
                avg_score=Avg('score')
            )
        }
        return Response(stats)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['semester', 'year', 'student', 'course']

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assessment_type', 'enrollment']

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['enrollment', 'date', 'present']

class PerformanceMetricsViewSet(viewsets.ModelViewSet):
    queryset = PerformanceMetrics.objects.all()
    serializer_class = PerformanceMetricsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'semester', 'year']

class StudentPerformanceMetricsViewSet(viewsets.ModelViewSet):
    queryset = StudentPerformanceMetrics.objects.all()
    serializer_class = StudentPerformanceMetricsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student']
