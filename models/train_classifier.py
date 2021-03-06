import sys
import re
import pickle 
import sqlite3
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sqlalchemy import create_engine
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# storing regex format for links
url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

def load_data(database_filepath):

    '''
    This function loads data from a sqlite database
    and divide it to X and Y, features, and labes.
    the function returns X, Y and column names of Y
    '''

    # load data from database
    engine = create_engine(f"sqlite:///{database_filepath}")
    df = pd.read_sql('DisasterResponse',con=engine)
    # create X and Y and get column names
    X = df['message']
    Y = df.drop(columns=['id', 'message', 'original', 'genre'])
    category_names = Y.columns
    
    return X, Y, category_names

def tokenize(text):

    '''
    This function receives text, and perffomrs the following:
    - replaces urls with "urlplaceholder"
    - tokenizes words
    - lemmatizes words
    and returns the inputted texted after proccessing
    '''
    
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens



def build_model():
    
    '''
    This function creates a pipeline containing the following:
    - 2 transformrs (CountVectorizer, TfidfTransformer)
    - 1 estimator (MultiOutputClassifier) which uses a RandomForestClassifier

    the function also uses GridSearchCV to go through multipel parameters and returns te best fit
    '''

    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))])
    

    parameters = {
        'vect__max_df': [0.5, 0.75, 1.0],
        'tfidf__use_idf': (True, False),
        'clf__estimator__bootstrap': (True, False),
    }

    cv = GridSearchCV(pipeline, param_grid=parameters)
    
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    
    '''
    This function takes a built model, the test data for X and Y
    as well as column names of the labels and creates a y_pred values
    then prints a classification report on all labels
    '''

    Y_pred = model.predict(X_test)
    print(classification_report(Y_test, Y_pred, target_names=category_names))

def save_model(model, model_filepath):

    '''
    This function stores the model in a pickle file.
    '''

    pickle.dump(model, open(model_filepath, 'wb'))
    
    
def main():

    '''
    This function runs the whole pipeline using the above functions:
    - loads the data
    - splits teh data into train and test splits
    - builds the model
    - trains the model
    - evaluates the model
    - and finally saves the model in a pickle file
    '''

    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()