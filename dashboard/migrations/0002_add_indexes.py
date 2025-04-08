from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='student',
            index=models.Index(fields=['student_id'], name='student_id_idx'),
        ),
        migrations.AddIndex(
            model_name='course',
            index=models.Index(fields=['course_code'], name='course_code_idx'),
        ),
        migrations.AddIndex(
            model_name='enrollment',
            index=models.Index(fields=['semester', 'year'], name='enrollment_period_idx'),
        ),
        migrations.AddIndex(
            model_name='assessment',
            index=models.Index(fields=['date'], name='assessment_date_idx'),
        ),
        migrations.AddIndex(
            model_name='attendancerecord',
            index=models.Index(fields=['date'], name='attendance_date_idx'),
        ),
        migrations.AddIndex(
            model_name='performancemetrics',
            index=models.Index(fields=['semester', 'year'], name='performance_period_idx'),
        ),
    ] 