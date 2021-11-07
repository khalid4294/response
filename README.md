# Disaster Response Pipeline Project

This project trains a classifier on a dataset of more than 26K messages thatwere sent during a disaster.
There's a webapp that has a text field where you can add a message and get the most probable type of message. there are 36 labels, your text can have multiple labels at the same time. 


### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/
