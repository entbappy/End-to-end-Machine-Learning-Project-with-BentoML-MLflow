import sys

from network.components.data_ingestion import DataIngestion
from network.components.data_transformation import DataTransformation
from network.components.data_validation import DataValidation
from network.components.model_evaluation import ModelEvaluation
from network.components.model_pusher import ModelPusher
from network.components.model_trainer import ModelTrainer
from network.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact,
    ModelEvaluationArtifact,
    ModelPusherArtifact,
    ModelTrainerArtifact,
)
from network.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelEvaluationConfig,
    ModelPusherConfig,
    ModelTrainerConfig,
    TrainingPipelineConfig,
)
from network.exception import NetworkException


class TrainPipeline:
    is_pipeline_running = False

    def __init__(self):
        self.training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        It takes in a training pipeline config, creates a data ingestion config, creates a data ingestion
        object, and then initiates data ingestion

        Returns:
          DataIngestionArtifact
        """
        try:
            self.data_ingestion_config: DataIngestionConfig = DataIngestionConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            data_ingestion: DataIngestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            data_ingestion_artifact: DataIngestionArtifact = (
                data_ingestion.initiate_data_ingestion()
            )

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkException(e, sys)

    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        """
        A function that takes in a data ingestion artifact and returns a data validation artifact.

        Args:
          data_ingestion_artifact (DataIngestionArtifact): DataIngestionArtifact

        Returns:
          DataValidationArtifact
        """
        try:
            self.data_validation_config: DataValidationConfig = DataValidationConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            data_validation: DataValidation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            data_validation_artifact: DataValidationArtifact = (
                data_validation.initiate_data_validation()
            )

            return data_validation_artifact

        except Exception as e:
            raise NetworkException(e, sys)

    def start_data_transformation(
        self, data_validation_artifact: DataValidationArtifact
    ) -> DataTransformationArtifact:
        """
        It takes in a data validation artifact and returns a data transformation artifact

        Args:
          data_validation_artifact (DataValidationArtifact): DataValidationArtifact

        Returns:
          DataTransformationArtifact
        """
        try:
            self.data_transformation_config: DataTransformationConfig = (
                DataTransformationConfig(
                    training_pipeline_config=self.training_pipeline_config
                )
            )

            data_transformation: DataTransformation = DataTransformation(
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=self.data_transformation_config,
            )

            data_transformation_artifact: DataTransformationArtifact = (
                data_transformation.initiate_data_transformation()
            )

            return data_transformation_artifact

        except Exception as e:
            raise NetworkException(e, sys)

    def start_model_trainer(
        self, data_transformation_artifact: DataTransformationArtifact
    ) -> ModelTrainerArtifact:
        """
        It takes in a DataTransformationArtifact object and returns a ModelTrainerArtifact object

        Args:
          data_transformation_artifact (DataTransformationArtifact): DataTransformationArtifact

        Returns:
          ModelTrainerArtifact
        """
        try:
            self.model_trainer_config: ModelTrainerConfig = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config,
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()

            return model_trainer_artifact

        except Exception as e:
            raise NetworkException(e, sys)

    def start_model_evaluation(
        self,
        data_validation_artifact: DataValidationArtifact,
        model_trainer_artifact: ModelTrainerArtifact,
    ) -> ModelEvaluationArtifact:
        """
        It takes in two artifacts, one from the data validation step and one from the model training step,
        and returns an artifact from the model evaluation step

        Args:
          data_validation_artifact (DataValidationArtifact): DataValidationArtifact
          model_trainer_artifact (ModelTrainerArtifact): This is the artifact that is returned by the model
        trainer.

        Returns:
          ModelEvaluationArtifact
        """
        try:
            self.model_eval_config: ModelEvaluationConfig = ModelEvaluationConfig()

            model_evaluation = ModelEvaluation(
                model_eval_config=self.model_eval_config,
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_trainer_artifact,
            )

            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()

            return model_evaluation_artifact

        except Exception as e:
            raise NetworkException(e, sys)

    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact):
        """
        It takes a model evaluation artifact and returns a model pusher artifact

        Args:
          model_evaluation_artifact (ModelEvaluationArtifact): This is the artifact that is returned from
        the model evaluation step.

        Returns:
          The model_pusher_artifact is being returned.
        """
        try:
            self.model_pusher_config: ModelPusherConfig = ModelPusherConfig()

            model_pusher = ModelPusher(
                model_evaluation_artifact=model_evaluation_artifact,
                model_pusher_config=self.model_pusher_config,
            )

            model_pusher_artifact = model_pusher.initiate_model_pusher()

            return model_pusher_artifact

        except Exception as e:
            raise NetworkException(e, sys)

    def run_pipeline(self):
        try:
            TrainPipeline.is_pipeline_running = True

            data_ingestion_artifact: DataIngestionArtifact = self.start_data_ingestion()

            data_validation_artifact: DataValidationArtifact = (
                self.start_data_validation(
                    data_ingestion_artifact=data_ingestion_artifact
                )
            )

            data_transformation_artifact: DataTransformationArtifact = (
                self.start_data_transformation(
                    data_validation_artifact=data_validation_artifact
                )
            )

            model_trainer_artifact: ModelTrainerArtifact = self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact
            )

            model_evaluation_artifact: ModelEvaluationArtifact = (
                self.start_model_evaluation(
                    data_validation_artifact=data_validation_artifact,
                    model_trainer_artifact=model_trainer_artifact,
                )
            )

            model_pusher_artifact: ModelPusherArtifact = self.start_model_pusher(
                model_evaluation_artifact=model_evaluation_artifact
            )

        except Exception as e:
            raise NetworkException(e, sys)
