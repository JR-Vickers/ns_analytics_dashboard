from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    math_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    reading_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    writing_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    race_ethnicity = models.CharField(max_length=1, default='A')  # A, B, C, D, or E
    parental_education = models.CharField(max_length=50, default='high school')
    lunch_type = models.CharField(max_length=20, default='standard')
    test_preparation = models.CharField(max_length=20, default='none')
    
    @property
    def average_score(self):
        return (self.math_score + self.reading_score + self.writing_score) / 3
    
    def __str__(self):
        return f"Student (ID: {self.id})"

class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    credits = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        validators=[MinValueValidator(0)]
    )
    
    def __str__(self):
        return f"{self.course_code}: {self.course_name}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)  # e.g., "Fall 2023"
    year = models.IntegerField()
    final_grade = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    class Meta:
        unique_together = ['student', 'course', 'semester', 'year']

class Assessment(models.Model):
    ASSESSMENT_TYPES = [
        ('QUIZ', 'Quiz'),
        ('EXAM', 'Exam'),
        ('PROJECT', 'Project'),
        ('HOMEWORK', 'Homework'),
    ]
    
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES)
    date = models.DateField()
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    weight = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

class AttendanceRecord(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField()
    
    class Meta:
        unique_together = ['enrollment', 'date']

class PerformanceMetrics(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(4)]
    )
    attendance_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    class Meta:
        unique_together = ['student', 'semester', 'year']

class StudentPerformanceMetrics(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    math_percentile = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    reading_percentile = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    writing_percentile = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    overall_percentile = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    
    class Meta:
        get_latest_by = 'created_at'
