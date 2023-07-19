from dataclasses import dataclass
from typing import List

from network.entity.config_entity import MLFlowModelInfo


@dataclass
class DataIngestionArtifact:
    feature_store_folder_path: str


@dataclass
class DataValidationArtifact:
    valid_data_dir: str

    invalid_data_dir: str

    training_file_path: str

    testing_file_path: str


@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str

    transformed_train_file_path: str

    transformed_test_file_path: str


@dataclass
class ClassificationMetricArtifact:
    roc_auc_score: float


@dataclass
class ModelTrainerArtifact:
    trained_model_list: List

    trained_model_dir: str

    best_model_dir: str

    best_model_name: str


@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool

    trained_model_info: MLFlowModelInfo

    accepted_model_info: MLFlowModelInfo

    prod_model_info: MLFlowModelInfo


@dataclass
class ModelPusherArtifact:
    trained_model_uri: str

    prod_model_uri: str
