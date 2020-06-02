from IPython.display import display
import pandas as pd

def count_percentage(df):
    experience_level_count = df['experience_level'].value_counts()
    experience_level_percentage = df['experience_level'].value_counts(normalize=True)
    
    
    marker_icon_count = df['marker_icon'].value_counts()
    marker_icon_percentage = df['marker_icon'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
    
    
    employment_type_count = df['employment_type'].value_counts()
    employment_type_percentage = df['employment_type'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
    
    df1 = pd.DataFrame({'Count': marker_icon_count, 'Percentage': marker_icon_percentage})
    df2 = pd.DataFrame({'Count': experience_level_count, 'Percentage': experience_level_percentage.mul(100).round(1).astype(str) + '%'})
    df3 = pd.DataFrame({'Count': employment_type_count, 'Percentage': employment_type_percentage})
    display(df1)
    df1.copy()[df1.Count>=25].plot.pie(y='Count', legend=False, figsize=(10, 10), autopct='%1.1f%%', shadow=True, startangle=90)
    display(df2)
    df2.plot.pie(y='Count', figsize=(5, 5), legend=False, autopct='%1.1f%%', shadow=True, startangle=90)
    display(df3)
    df3.plot.pie(y='Count', figsize=(5, 5), legend=False, autopct='%1.1f%%', shadow=True, startangle=90)

