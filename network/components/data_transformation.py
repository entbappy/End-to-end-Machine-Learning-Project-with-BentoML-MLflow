import os
import sys

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network.constant import training_pipeline
from network.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)
from network.entity.config_entity import DataTransformationConfig
from network.exception import NetworkException
from network.logger import logging
from network.utils.main_utils import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            self.data_validation_artifact: DataValidationArtifact = (
                data_validation_artifact
            )

            self.data_transformation_config: DataTransformationConfig = (
                data_transformation_config
            )

        except Exception as e:
            raise NetworkException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        It reads a CSV file and returns a Pandas DataFrame

        Args:
          file_path (str): The path to the file you want to read.

        Returns:
          A dataframe
        """
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise NetworkException(e, sys)

    def get_data_transformer_object(cls) -> Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )

        try:
            imputer: KNNImputer = KNNImputer(
                **training_pipeline.DATA_TRANSFORMATION_IMPUTER_PARAMS
            )

            logging.info(
                f"Initialised KNNImputer with {training_pipeline.DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )

            preprocessor: Pipeline = Pipeline([("imputer", imputer)])

            logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )

            return preprocessor

        except Exception as e:
            raise NetworkException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info(
            "Entered initiate_data_transformation method of DataTransformation class"
        )

        try:
            logging.info("Starting data transformation")

            os.makedirs(
                self.data_transformation_config.transformed_data_dir, exist_ok=True
            )

            train_df: pd.DataFrame = DataTransformation.read_data(
                self.data_validation_artifact.training_file_path
            )

            test_df: pd.DataFrame = DataTransformation.read_data(
                self.data_validation_artifact.testing_file_path
            )

            preprocessor: Pipeline = self.get_data_transformer_object()

            logging.info("Got the preprocessor object")

            input_feature_train_df: pd.DataFrame = train_df.drop(
                columns=[training_pipeline.TARGET_COLUMN], axis=1
            )

            target_feature_train_df: pd.DataFrame = train_df[
                training_pipeline.TARGET_COLUMN
            ]

            target_feature_train_df.replace(-1, 0, inplace=True)

            logging.info("Got train features and test features of Training dataset")

            input_feature_test_df: pd.DataFrame = test_df.drop(
                columns=[training_pipeline.TARGET_COLUMN], axis=1
            )

            target_feature_test_df: pd.DataFrame = test_df[
                training_pipeline.TARGET_COLUMN
            ]

            target_feature_test_df.replace(-1, 0, inplace=True)

            logging.info("Got train features and test features of Testing dataset")

            logging.info(
                "Applying preprocessing object on training dataframe and testing dataframe"
            )

            input_feature_train_arr: np.ndarray = preprocessor.fit_transform(
                input_feature_train_df
            )

            logging.info(
                "Used the preprocessor object to fit transform the train features"
            )

            input_feature_test_arr: np.ndarray = preprocessor.transform(
                input_feature_test_df
            )

            logging.info("Used the preprocessor object to transform the test features")

            train_arr: np.array = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]

            test_arr: np.ndarray = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor,
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr,
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr,
            )

            logging.info("Saved the preprocessor object")

            data_transformation_artifact: DataTransformationArtifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            logging.info(
                "Exited initiate_data_transformation method of DataTransformation class"
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworkException(e, sys)
