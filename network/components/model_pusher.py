import sys

from network.configuration.mlflow_connection import MLFlowClient
from network.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact
from network.entity.config_entity import ModelPusherConfig
from network.exception import NetworkException
from network.logger import logging
from network.utils.main_utils import build_and_push_bento_image


class ModelPusher:
    def __init__(
        self,
        model_evaluation_artifact: ModelEvaluationArtifact,
        model_pusher_config: ModelPusherConfig,
    ):
        self.model_evaluation_artifact: ModelEvaluationArtifact = (
            model_evaluation_artifact
        )

        self.model_pusher_config: ModelPusherConfig = model_pusher_config

        self.mlflow_client = MLFlowClient().client

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        If there is no accepted model, raise an exception. If there is an accepted model but no production
        model, move the accepted model to production. If there is an accepted model and a production model,
        move the accepted model to production and the production model to staging
        """
        logging.info("Entered initiate_model_pusher method of ModelPusher class")

        try:
            if self.model_evaluation_artifact.accepted_model_info is None:
                raise Exception("No trained model is accepted")

            elif (
                self.model_evaluation_artifact.accepted_model_info is not None
                and self.model_evaluation_artifact.prod_model_info is None
            ):
                logging.info(
                    "Production model info is None, Accepted model info is not None. Moving accepted model to production"
                )

                self.mlflow_client.transition_model_version_stage(
                    name=self.model_evaluation_artifact.accepted_model_info.model_name,
                    version=self.model_evaluation_artifact.accepted_model_info.model_version,
                    stage=self.model_pusher_config.production_model_stage,
                    archive_existing_versions=self.model_pusher_config.archive_existing_versions,
                )

                build_and_push_bento_image(
                    model_uri=self.model_evaluation_artifact.accepted_model_info.model_uri
                )

            elif (
                self.model_evaluation_artifact.accepted_model_info is not None
                and self.model_evaluation_artifact.prod_model_info is not None
            ):
                logging.info(
                    "Accepted model info is not None and Production model info is not None. Moving accepted model to production and production model to staging"
                )

                self.mlflow_client.transition_model_version_stage(
                    name=self.model_evaluation_artifact.accepted_model_info.model_name,
                    version=self.model_evaluation_artifact.accepted_model_info.model_version,
                    stage=self.model_pusher_config.production_model_stage,
                    archive_existing_versions=self.model_pusher_config.archive_existing_versions,
                )

                self.mlflow_client.transition_model_version_stage(
                    name=self.model_evaluation_artifact.prod_model_info.model_name,
                    version=self.model_evaluation_artifact.prod_model_info.model_version,
                    stage=self.model_pusher_config.staging_model_stage,
                    archive_existing_versions=self.model_pusher_config.archive_existing_versions,
                )

                build_and_push_bento_image(
                    model_uri=self.model_evaluation_artifact.accepted_model_info.model_uri
                )

            else:
                logging.info("something went wrong")

            logging.info("Exited initiate_model_pusher method of ModelPusher class")

        except Exception as e:
            raise NetworkException(e, sys)
