import os
import sys
from typing import Dict

import mlflow
import numpy as np
from mlflow.pyfunc import PythonModel
from neuro_mf import BestModel, ModelFactory

from network.constant import training_pipeline
from network.entity.artifact_entity import (
    ClassificationMetricArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from network.entity.config_entity import ModelTrainerConfig
from network.exception import NetworkException
from network.logger import logging
from network.ml.metric import calculate_metric
from network.ml.mlflow import MLFLowOperation
from network.ml.model.estimator import NetworkModel
from network.utils.main_utils import load_numpy_array_data, load_object, save_object


class ModelTrainer:
    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig,
    ):
        self.data_transformation_artifact: DataTransformationArtifact = (
            data_transformation_artifact
        )

        self.model_trainer_config: ModelTrainerConfig = model_trainer_config

        self.mlflow_op: MLFLowOperation = MLFLowOperation()

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """
        It takes in the transformed data and trains a model using the model factory

        Returns:
          The ModelTrainerArtifact object is being returned.
        """
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            train_arr: np.ndarray = load_numpy_array_data(
                file_path=self.data_transformation_artifact.transformed_train_file_path
            )

            test_arr: np.ndarray = load_numpy_array_data(
                file_path=self.data_transformation_artifact.transformed_test_file_path
            )

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_factory: ModelFactory = ModelFactory(
                model_config_path=self.model_trainer_config.model_config_file_path
            )

            best_model_detail: BestModel = model_factory.get_best_model(
                X=x_train,
                y=y_train,
                base_accuracy=self.model_trainer_config.expected_score,
            )

            preprocessing_obj: object = load_object(
                file_path=self.data_transformation_artifact.transformed_object_file_path
            )

            best_model: PythonModel = NetworkModel(
                preprocessing_object=preprocessing_obj,
                trained_model_object=best_model_detail.best_model,
            )

            best_model_path: str = os.path.join(  
                self.model_trainer_config.best_model_file_dir,
                best_model.trained_model_object.__class__.__name__
                + "-"
                + training_pipeline.EXP_NAME
                + ".pkl",
            )

            save_object(file_path=best_model_path, obj=best_model)

            for model in model_factory.grid_searched_best_model_list:
                with mlflow.start_run(
                    run_name=training_pipeline.EXP_NAME
                    + "-"
                    + model.model_serial_number
                ):
                    model_score: ClassificationMetricArtifact = calculate_metric(
                        model=model.best_model, x=x_test, y=y_test
                    )

                    model_parameters: Dict = model.best_parameters

                    trained_model = NetworkModel(
                        preprocessing_object=preprocessing_obj,
                        trained_model_object=model.best_model,
                    )

                    trained_model_path: str = os.path.join(
                        self.model_trainer_config.trained_model_file_dir,
                        trained_model.trained_model_object.__class__.__name__
                        + "-"
                        + training_pipeline.EXP_NAME
                        + ".pkl",
                    )

                    save_object(file_path=trained_model_path, obj=trained_model)

                    self.mlflow_op.log_all_for_model(
                        model=trained_model,
                        model_parameters=model_parameters,
                        model_score=model_score,
                    )

            mlflow.end_run()

            if best_model_detail.best_score < self.model_trainer_config.expected_score:
                logging.info("No best model found with score more than base score")

                raise Exception("No best model found with score more than base score")

            model_trainer_artifact: ModelTrainerArtifact = ModelTrainerArtifact(
                trained_model_dir=self.model_trainer_config.trained_model_file_dir,
                best_model_dir=self.model_trainer_config.best_model_file_dir,
                best_model_name=best_model_detail.best_model.__class__.__name__
                + "-"
                + training_pipeline.EXP_NAME,
                trained_model_list=model_factory.grid_searched_best_model_list,
            )

            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise NetworkException(e, sys)
