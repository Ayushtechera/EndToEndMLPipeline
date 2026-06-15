import os
import sys
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split 
from dataclasses import dataclass
import pandas as pd 

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer
@dataclass
class DataIngestionConfig:
    # Giving input like where to save the train and test data 
    train_data_path:str = os.path.join('artifact','train.csv')
    test_data_path:str = os.path.join('artifact','test.csv')
    raw_data_path:str = os.path.join('artifact','data.csv')

class DataIngestion:
    def __init__(self):
        # Whenever we call DataIngestion all the paths we initialised in DataIngestionConfig will be saved in ingestion_config varieble  
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        # Write code here to read data form different data sources/databases 
        logging.info("Entered the data ingestion method or componenet")
        try:
            # Reading data 
            df = pd.read_csv('notebook/data/stud.csv')
            logging.info("Read the dataset as dataframe")

            # Creating folder named artifact
            os.makedirs(
                os.path.dirname(self.ingestion_config.train_data_path),
                exist_ok=True
            )

            # creating data.csv file and saving it in artifact folder and df(dataset) is saved in artifact/data.csv 
            df.to_csv(
                self.ingestion_config.raw_data_path,
                index=False,header=True
            )

            logging.info("train test split initiated")
            
            # Doing train and test split
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)
            # Saving train file
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            # Saving test file 
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of the data is completed")

            return{
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,

            }
        except Exception as e:
            raise CustomException(e,sys)
        

if __name__ == "__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_array,test_array = data_transformation.initiate_data_transformation(train_data,test_data)

    ModelTrainer=ModelTrainer()
    print(ModelTrainer.initiate_model_trainer(train_array,test_array)) 