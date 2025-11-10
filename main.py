from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, ModelTrainerConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig

import sys


if __name__ == "__main__":
    try: # Fix: Added a try block for the entire main execution
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiating data ingestion...") # Fix: Corrected typo "Intiate" to "Initiating"
        data_ingestion_artifact = data_ingestion.intiate_data_ingestion()
        logging.info(f"Data Ingestion Completed: {data_ingestion_artifact}") # Fix: Added artifact to log
        print(data_ingestion_artifact)

        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("Initiating data validation...") # Fix: Corrected typo "Intiate" to "Initiating"
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info(f"Data Validation Completed: {data_validation_artifact}") # Fix: Added artifact to log
        print(data_validation_artifact) # Fix: Moved print statement inside the try block
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        logging.info("data transformation started")
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info(f"Data Transformation Completed: {data_transformation_artifact}")
        print(data_transformation_artifact)
        
        logging.info(f"Model training started")
        
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        
        logging.info(f"Model Trainer Completed: {model_trainer_artifact}")
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e