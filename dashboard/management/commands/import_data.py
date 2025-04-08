import csv
import numpy as np
from django.core.management.base import BaseCommand
from django.db import transaction
from dashboard.models import Student, StudentPerformanceMetrics

class Command(BaseCommand):
    help = 'Import processed student data into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting data import...')
        
        try:
            with transaction.atomic():
                with open('data/processed/processed_student_data.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    
                    # Store all scores to calculate percentiles later
                    math_scores = []
                    reading_scores = []
                    writing_scores = []
                    students = []
                    
                    for row in reader:
                        # Get race/ethnicity
                        race_ethnicity = 'A'
                        for group in ['A', 'B', 'C', 'D', 'E']:
                            if row[f'race/ethnicity_group {group}'].lower() == 'true':
                                race_ethnicity = group
                                break
                        
                        # Get parental education
                        education_levels = [
                            "associate's degree", "bachelor's degree", "high school",
                            "master's degree", "some college", "some high school"
                        ]
                        parental_education = next(
                            level for level in education_levels
                            if row[f'parental level of education_{level}'].lower() == 'true'
                        )
                        
                        # Get lunch type
                        lunch_type = 'free/reduced' if row['lunch_free/reduced'].lower() == 'true' else 'standard'
                        
                        # Get test preparation
                        test_prep = 'completed' if row['test preparation course_completed'].lower() == 'true' else 'none'
                        
                        # Create Student
                        student = Student.objects.create(
                            gender='F' if row['gender'] == '0' else 'M',
                            math_score=int(row['math score']),
                            reading_score=int(row['reading score']),
                            writing_score=int(row['writing score']),
                            race_ethnicity=race_ethnicity,
                            parental_education=parental_education,
                            lunch_type=lunch_type,
                            test_preparation=test_prep
                        )
                        
                        math_scores.append(int(row['math score']))
                        reading_scores.append(int(row['reading score']))
                        writing_scores.append(int(row['writing score']))
                        students.append(student)
                    
                    # Calculate percentiles
                    math_scores = np.array(math_scores)
                    reading_scores = np.array(reading_scores)
                    writing_scores = np.array(writing_scores)
                    average_scores = (math_scores + reading_scores + writing_scores) / 3
                    
                    for i, student in enumerate(students):
                        StudentPerformanceMetrics.objects.create(
                            student=student,
                            math_percentile=np.percentile(math_scores, math_scores[i]),
                            reading_percentile=np.percentile(reading_scores, reading_scores[i]),
                            writing_percentile=np.percentile(writing_scores, writing_scores[i]),
                            overall_percentile=np.percentile(average_scores, average_scores[i])
                        )
                
            self.stdout.write(self.style.SUCCESS('Data import completed successfully'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error during import: {str(e)}'))
            raise 