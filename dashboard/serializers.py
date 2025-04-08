from rest_framework import serializers
from .models import (
    Student, Course, Enrollment, Assessment,
    AttendanceRecord, PerformanceMetrics, StudentPerformanceMetrics
)

class StudentSerializer(serializers.ModelSerializer):
    average_score = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'

class AttendanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceRecord
        fields = '__all__'

class PerformanceMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMetrics
        fields = '__all__'

class StudentPerformanceMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPerformanceMetrics
        fields = '__all__' 