import sys
import pandas as pd
from sqlalchemy import create_engine
import sqlite3

def load_data(messages_filepath, categories_filepath):

    '''
    This function loads the data from csv files
    and creates df for each file, then merges dfs together
    returnng the merged dfs
    '''
    
    # load messages dataset
    messages = pd.read_csv(messages_filepath)
    # load categories dataset
    categories = pd.read_csv(categories_filepath)
    # merge datasets
    df = pd.merge(messages, categories, on='id')
    # create a dataframe of the 36 individual category columns
    
    return df

def clean_data(df):
    
    '''
    This funtion takes a df, cleans the categories column and uses its unique values as new columns
    then cleans all values to just hhave either (0) or (1) and removes (2) values
    '''

    df = df
    # create a dataframe of the 36 individual category columns
    categories = df.categories.str.split(expand=True, pat=';')
    # rename columns to use the first row columns
    new_header = categories.iloc[0].str.replace("-", "").str.replace("1", "").str.replace("0", "")
    categories.columns = new_header

    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].str.replace(f"{column}", "").str.replace("-", "")
    
        # convert column from string to numeric
        categories[column] = categories[column].astype(int)
        


    # drop the original categories column from `df`
    df.drop(columns='categories', inplace=True)
    
    

    # concatenate the original dataframe with the new `categories` dataframe
    df_cleaned = pd.concat([df, categories], axis=1)

    # drop values with 2
    df_cleaned.drop(df_cleaned.loc[df_cleaned['related']==2].index, inplace=True)
    
    # drop duplicates
    df_cleaned.drop_duplicates(inplace=True)
    
    return df_cleaned

def save_data(df, database_filename):
    
    '''
    This function takes a dataframe and stores it in a sqlite database
    '''

    #save as sql db
    engine = create_engine(f"sqlite:///{database_filename}")
    df.to_sql('DisasterResponse', engine, index=False, if_exists='replace')


def main():

    '''
    This function runs the whole ETL pipeline:
    - loads data from CSVs
    - cleans teh data
    - and saves the data in a sqlite database
    '''

    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()