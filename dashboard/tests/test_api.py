from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from dashboard.models import Student, Course, Enrollment

class StudentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = Student.objects.create(
            gender='M',
            math_score=85,
            reading_score=90,
            writing_score=88,
            race_ethnicity='A',
            parental_education='bachelor',
            lunch_type='standard',
            test_preparation='completed'
        )
        
    def test_get_students(self):
        response = self.client.get(reverse('student-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_get_student_detail(self):
        response = self.client.get(reverse('student-detail', args=[self.student.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['math_score'], 85)
        
    def test_student_performance_summary(self):
        response = self.client.get(reverse('student-performance-summary', args=[self.student.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('average_scores', response.data)
        self.assertIn('course_performance', response.data)
        self.assertIn('attendance', response.data)

class CourseAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            course_code='MATH101',
            course_name='Introduction to Mathematics',
            department='Mathematics',
            credits=3.0
        )
        
    def test_get_courses(self):
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_get_course_detail(self):
        response = self.client.get(reverse('course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['course_code'], 'MATH101')
        
    def test_course_stats(self):
        response = self.client.get(reverse('course-course-stats', args=[self.course.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_students', response.data)
        self.assertIn('grade_distribution', response.data)
        self.assertIn('assessment_stats', response.data)

class EnrollmentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = Student.objects.create(
            gender='F',
            math_score=92,
            reading_score=88,
            writing_score=90
        )
        self.course = Course.objects.create(
            course_code='ENG101',
            course_name='English Composition',
            department='English',
            credits=3.0
        )
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            semester='Fall',
            year=2023,
            final_grade=88.5
        )
        
    def test_get_enrollments(self):
        response = self.client.get(reverse('enrollment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_get_enrollment_detail(self):
        response = self.client.get(reverse('enrollment-detail', args=[self.enrollment.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['final_grade']), 88.5) 