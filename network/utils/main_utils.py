import os
import sys
from typing import Dict, Union

import bentoml
import dill
import numpy as np
import yaml

from network.cloud_storage.aws_operations import S3Sync
from network.constant import training_pipeline
from network.exception import NetworkException
from network.logger import logging


def read_yaml(file_name: str) -> Dict:
    """
    It reads a yaml file and returns a dictionary

    Args:
      file_name (str): str

    Returns:
      A dictionary
    """
    logging.info("Entered the read_yaml class of MainUtils class")

    try:
        with open(file_name) as f:
            dic: Dict = yaml.safe_load(f)

        logging.info(f"Read the yaml content from {file_name}")

        logging.info("Exited the read_yaml class of MainUtils class")

        return dic

    except Exception as e:
        raise NetworkException(e, sys)


def read_text(file_name: str) -> str:
    """
    It reads the text content from a file and returns it

    Args:
      file_name (str): str = The name of the file to read from

    Returns:
      The text content of the file.
    """
    logging.info("Entered the read_text class of MainUtils class")

    try:
        with open(file_name, "r") as f:
            txt: str = f.read()

        logging.info(f"Read the text content from {file_name}")

        logging.info("Exited the read_text class of MainUtils class")

        return txt

    except Exception as e:
        raise NetworkException(e, sys)


def save_numpy_array_data(file_path: str, array: Union[np.array, np.ndarray]) -> None:
    """
    It saves a numpy array to a file

    Args:
      file_path (str): str = "C:/Users/user/Desktop/test_data/test_data.npy"
      array (Union[np.array, np.ndarray]): The numpy array to be saved
    """
    logging.info("Entered the save_numpy_array_data class of MainUtils class")

    try:
        dir_path: str = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)

        logging.info(f"Saved {array} numpy array to {file_path}")

        logging.info("Exited the save_numpy_array_data class of MainUtils class")

    except Exception as e:
        raise NetworkException(e, sys)


def load_numpy_array_data(file_path: str) -> Union[np.array, np.ndarray]:
    """
    It loads a numpy array from a file

    Args:
      file_path (str): str

    Returns:
      The object is being returned.
    """
    logging.info("Entered the load_numpy_array_data class of MainUtils class")

    try:
        with open(file_path, "rb") as file_obj:
            obj = np.load(file_obj, allow_pickle=True)

        logging.info(f"Loaded numpy array from {file_path}")

        logging.info("Exited the load_numpy_array_data class of MainUtils class")

        return obj

    except Exception as e:
        raise NetworkException(e, sys)


def load_object(file_path: str) -> object:
    """
    It loads an object from a file

    Args:
      file_path (str): The path to the file to load the object from

    Returns:
      The object that was loaded from the file.
    """
    logging.info("Entered the load_object method of MainUtils class")

    try:
        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)

        logging.info(f"Loaded object from {file_path}")

        logging.info("Exited the load_object method of MainUtils class")

        return obj

    except Exception as e:
        raise NetworkException(e, sys)


def save_object(file_path: str, obj: object) -> None:
    """
    It saves an object to a file

    Args:
      file_path (str): The path to the file where the object will be saved.
      obj (object): object
    """
    logging.info("Entered the save_object method of MainUtils class")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logging.info("Exited the save_object method of MainUtils class")

    except Exception as e:
        raise NetworkException(e, sys)


def sync_artifacts() -> None:
    """
    It syncs the contents of the ARTIFACT_DIR and LOG_DIR to the APP_ARTIFACTS_BUCKET
    """
    try:
        s3 = S3Sync()

        s3.sync_folder_to_s3(
            folder=training_pipeline.ARTIFACT_DIR,
            bucket_name=training_pipeline.APP_ARTIFACTS_BUCKET,
            bucket_folder_name=training_pipeline.PIPELINE_NAME
            + "/"
            + training_pipeline.ARTIFACT_DIR,
        )

    except Exception as e:
        raise NetworkException(e, sys)


def build_and_push_bento_image(model_uri: str) -> None:
    """
    It takes a model URI as input, imports the model into BentoML, containerizes it, and pushes it to
    ECR

    Args:
      model_uri (str): The URI of the model to be pushed to the BentoML service.
    """
    try:
        logging.info(f"Importing the {model_uri} model")

        bentoml.mlflow.import_model(
            name=training_pipeline.MODEL_PUSHER_BENTOML_MODEL_NAME, model_uri=model_uri
        )

        logging.info(f"Imported {model_uri} model")

        os.system(
            f"bash scripts/bento.sh {training_pipeline.MODEL_PUSHER_BENTOML_MODEL_NAME}"
        )

        logging.info("Bentofile is created")

        os.system(
            "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 566373416292.dkr.ecr.us-east-1.amazonaws.com"
        )

        logging.info("Logged into AWS ECR")

      
        os.system(
            f"bentoml containerize {training_pipeline.MODEL_PUSHER_BENTOML_SERVICE_NAME}:latest -t 566373416292.dkr.ecr.us-east-1.amazonaws.com/{training_pipeline.MODEL_PUSHER_BENTOML_MODEL_IMAGE}:latest"
        )

        logging.info(f"Containerized the bento")

      

        os.system(
            f"docker push 566373416292.dkr.ecr.us-east-1.amazonaws.com/{training_pipeline.MODEL_PUSHER_BENTOML_MODEL_IMAGE}:latest"
        )

        logging.info("Pushed the bento docker image")

    except Exception as e:
        raise NetworkException(e, sys)
