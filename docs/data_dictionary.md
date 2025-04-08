# Data Dictionary

## Raw Data Fields

### Student Demographics
- gender: Student's gender (male/female)
- race/ethnicity: Student's racial/ethnic group
- parental level of education: Highest education level of parents
- lunch: Type of lunch program (standard/free/reduced)
- test preparation course: Whether student completed test prep (completed/none)

### Academic Performance
- math score: Score on math exam (0-100)
- reading score: Score on reading exam (0-100)
- writing score: Score on writing exam (0-100)

## Preprocessing Steps
1. Missing Value Handling
   - Removed rows with missing values
   
2. Feature Engineering
   - Converted gender to binary (0=female, 1=male)
   - One-hot encoded categorical variables
   - Calculated total score (sum of all scores)
   - Calculated average score (mean of all scores)

3. Data Validation
   - Score range validation (0-100)
   - Categorical value validation
   - Data type conversion

## Data Quality Notes
- All scores are normalized to 0-100 scale
- No duplicate records present
- Categorical variables are properly encoded
- No outliers removed (all scores within valid range) 