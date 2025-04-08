# Database Schema Design

## Tables

### students
- id (PK)
- gender (INT)
- race_ethnicity (VARCHAR)
- parental_education (VARCHAR)
- lunch (VARCHAR)
- test_preparation (BOOLEAN)

### scores
- id (PK)
- student_id (FK)
- math_score (INT)
- reading_score (INT)
- writing_score (INT)
- total_score (INT)
- average_score (FLOAT)

## Relationships
- One-to-One: students -> scores
- Each student has exactly one set of scores

## Indexes
- students(id)
- scores(student_id)
- scores(total_score)
- scores(average_score)

## Constraints
- math_score, reading_score, writing_score: 0-100
- total_score: 0-300
- average_score: 0-100
- gender: 0 or 1
- test_preparation: true or false

## Normalization
- First Normal Form (1NF): All attributes are atomic
- Second Normal Form (2NF): All non-key attributes are fully dependent on the primary key
- Third Normal Form (3NF): No transitive dependencies

## Query Optimization
- Indexes on frequently queried columns
- Materialized views for common aggregations
- Partitioning by academic year (if temporal data is added) 