from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from dashboard.models import Student, StudentPerformanceMetrics
from django.core.management import call_command

class StudentModelTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            gender='M',
            math_score=85,
            reading_score=90,
            writing_score=88,
            race_ethnicity='B',
            parental_education="bachelor's degree",
            lunch_type='standard',
            test_preparation='completed'
        )

    def test_student_creation(self):
        """Test that a student can be created with valid data"""
        self.assertEqual(self.student.gender, 'M')
        self.assertEqual(self.student.math_score, 85)
        self.assertEqual(self.student.average_score, (85 + 90 + 88) / 3)

    def test_invalid_scores(self):
        """Test that scores must be between 0 and 100"""
        with self.assertRaises(ValidationError):
            student = Student(
                gender='F',
                math_score=101,  # Invalid score
                reading_score=90,
                writing_score=88,
                race_ethnicity='A',
                parental_education='high school',
                lunch_type='standard',
                test_preparation='none'
            )
            student.full_clean()

    def test_invalid_gender(self):
        """Test that gender must be either 'M' or 'F'"""
        with self.assertRaises(ValidationError):
            student = Student(
                gender='X',  # Invalid gender
                math_score=85,
                reading_score=90,
                writing_score=88,
                race_ethnicity='A',
                parental_education='high school',
                lunch_type='standard',
                test_preparation='none'
            )
            student.full_clean()

class StudentPerformanceMetricsTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            gender='F',
            math_score=85,
            reading_score=90,
            writing_score=88,
            race_ethnicity='A',
            parental_education='high school',
            lunch_type='standard',
            test_preparation='none'
        )

    def test_metrics_creation(self):
        """Test that performance metrics can be created"""
        metrics = StudentPerformanceMetrics.objects.create(
            student=self.student,
            math_percentile=75.5,
            reading_percentile=80.0,
            writing_percentile=78.5,
            overall_percentile=78.0
        )
        self.assertEqual(metrics.math_percentile, 75.5)
        self.assertEqual(metrics.student, self.student)

    def test_invalid_percentile(self):
        """Test that percentiles must be between 0 and 100"""
        with self.assertRaises(ValidationError):
            metrics = StudentPerformanceMetrics(
                student=self.student,
                math_percentile=101.0,  # Invalid percentile
                reading_percentile=80.0,
                writing_percentile=78.5,
                overall_percentile=78.0
            )
            metrics.full_clean()

class DataImportTests(TestCase):
    def test_import_command(self):
        """Test that the import_data command runs without errors"""
        try:
            call_command('import_data')
            # Check that we have data in the database
            self.assertTrue(Student.objects.exists())
            self.assertTrue(StudentPerformanceMetrics.objects.exists())
            
            # Check some basic data integrity
            student_count = Student.objects.count()
            metrics_count = StudentPerformanceMetrics.objects.count()
            self.assertEqual(student_count, metrics_count, 
                           "Each student should have performance metrics")
            
            # Check that scores and percentiles are within valid ranges
            invalid_scores = Student.objects.filter(
                math_score__gt=100
            ).union(
                Student.objects.filter(reading_score__gt=100)
            ).union(
                Student.objects.filter(writing_score__gt=100)
            ).count()
            self.assertEqual(invalid_scores, 0, "Found scores greater than 100")
            
            invalid_percentiles = StudentPerformanceMetrics.objects.filter(
                math_percentile__gt=100
            ).union(
                StudentPerformanceMetrics.objects.filter(reading_percentile__gt=100)
            ).union(
                StudentPerformanceMetrics.objects.filter(writing_percentile__gt=100)
            ).union(
                StudentPerformanceMetrics.objects.filter(overall_percentile__gt=100)
            ).count()
            self.assertEqual(invalid_percentiles, 0, "Found percentiles greater than 100")
            
        except Exception as e:
            self.fail(f"Import command failed: {str(e)}") 