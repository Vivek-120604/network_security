import os
import sys

import mlflow

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.ml_utils.metric import classification_metric
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object, load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(self, model, metrics):
        """
        Log given metrics and model to MLflow in a run.
        Metrics is expected to be a ClassificationMetricArtifact with f1_score, precision_score, recall_score attributes.
        """
        with mlflow.start_run():
            f1_score = metrics.f1_score
            precision = metrics.precision_score
            recall = metrics.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.sklearn.log_model(model, "model")
               

    def train_model(self, X_train, y_train, X_test, y_test) -> ModelTrainerArtifact:
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1, max_iter=1000),
                "Adaboost": AdaBoostClassifier(),
            }

            params = {
                "Decision Tree": {
                    'criterion': ['gini', 'entropy', 'log_loss'],
                },
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Gradient Boosting": {
                    'learning_rate': [.1, .01, .05, .001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Logistic Regression": {},
                "Adaboost": {
                    'learning_rate': [.1, .01, 0.5, .001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }

            model_report: dict = evaluate_models(x_train=X_train, y_train=y_train, x_test=X_test, y_test=y_test, models=models, param=params)

            # to get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            best_model.fit(X_train, y_train)

            # save trained model to configured path
            trained_model_dir = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            if trained_model_dir and not os.path.exists(trained_model_dir):
                os.makedirs(trained_model_dir, exist_ok=True)
            save_object(self.model_trainer_config.trained_model_file_path, best_model)

            y_train_pred = best_model.predict(X_train)
            classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)

            # tracking the best model and training metrics
            self.track_mlflow(best_model, classification_train_metric)

            y_test_pred = best_model.predict(X_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
            # tracking the best model and test metrics
            self.track_mlflow(best_model, classification_test_metric)

            # model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            X_train, y_train, X_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )

            # call training routine and return the produced artifact
            return self.train_model(X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
