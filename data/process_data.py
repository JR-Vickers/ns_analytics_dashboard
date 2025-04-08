import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import re

def sanitize_filename(name):
    """Replace special characters in filename."""
    return re.sub(r'[\\/:*?"<>| ]', '_', name)

def load_data(file_path):
    """Load and return the dataset."""
    return pd.read_csv(file_path)

def perform_eda(df):
    """Perform exploratory data analysis and save visualizations."""
    # Basic statistics
    print("Dataset Info:")
    print(df.info())
    print("\nBasic Statistics:")
    print(df.describe())
    
    # Create EDA directory
    Path("data/eda").mkdir(exist_ok=True)
    
    # Distribution plots
    for col in ['math score', 'reading score', 'writing score']:
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x=col, kde=True)
        plt.title(f'Distribution of {col}')
        plt.savefig(f'data/eda/{sanitize_filename(col)}_distribution.png')
        plt.close()
    
    # Correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.savefig('data/eda/correlation_matrix.png')
    plt.close()
    
    # Categorical analysis
    for col in ['gender', 'race/ethnicity', 'parental level of education']:
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x=col, y='math score')
        plt.xticks(rotation=45)
        plt.title(f'Math Score by {col}')
        plt.savefig(f'data/eda/math_score_by_{sanitize_filename(col)}.png')
        plt.close()

def preprocess_data(df):
    """Clean and preprocess the data."""
    # Handle missing values
    df = df.dropna()
    
    # Convert categorical variables to numerical
    df['gender'] = df['gender'].map({'female': 0, 'male': 1})
    
    # One-hot encode other categorical variables
    df = pd.get_dummies(df, columns=['race/ethnicity', 'parental level of education', 'lunch', 'test preparation course'])
    
    return df

def main():
    # Load data
    df = load_data('data/raw/StudentsPerformance.csv')
    
    # Perform EDA
    perform_eda(df)
    
    # Preprocess data
    processed_df = preprocess_data(df)
    
    # Save processed data
    Path("data/processed").mkdir(exist_ok=True)
    processed_df.to_csv('data/processed/processed_student_data.csv', index=False)
    
    # Create simple data dictionary
    with open('data/processed/data_dictionary.txt', 'w') as f:
        f.write("Data Dictionary\n")
        f.write("==============\n\n")
        f.write("Preprocessing steps:\n")
        f.write("1. Handled missing values\n")
        f.write("2. Converted gender to binary (0=female, 1=male)\n")
        f.write("3. One-hot encoded categorical variables\n\n")
        f.write("Columns:\n")
        for col in processed_df.columns:
            f.write(f"- {col}\n")

if __name__ == "__main__":
    main() 