import pandas as pd

def load_data():
    df1 = pd.read_csv(r'D:\End To End ML\End_To_End_Intership\Recommendation_System\Recommendation_System\Research_Notebook\NaukriData_data analytics.csv')
    df2 = pd.read_csv(r'D:\End To End ML\End_To_End_Intership\Recommendation_System\Recommendation_System\Research_Notebook\NaukriData_Data Science.csv')
    # combine both datasets
    df = pd.concat([df1, df2], ignore_index=True)
    return df

def preprocess_data(df):
    # Drop duplicates and missing values
    df = df.drop_duplicates()   
    # Convert "Experience_Required" to a numeric data type (float)
    df['Experience_Required'] = df['Experience_Required'].str.extract('(\d+)').astype(float)
    df = df.dropna() 
    # Replace "None" values with actual NaN values
    df.replace('None', pd.NA, inplace=True)  
    # Drop rows with NaN values in any column
    df.dropna(axis=0, how='any', inplace=True)
    
    return df

