import sys

from network.cloud_storage.aws_operations import S3Sync
from network.entity.artifact_entity import DataIngestionArtifact
from network.entity.config_entity import DataIngestionConfig
from network.exception import NetworkException
from network.logger import logging


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.s3 = S3Sync()

        self.data_ingestion_config: DataIngestionConfig = data_ingestion_config

    def export_data_into_feature_store(
        self, bucket_name: str, bucket_folder_name: str, feature_store_folder_name: str
    ) -> None:
        """
        It syncs the data from the S3 bucket to the feature store folder

        Args:
          bucket_name (str): The name of the bucket where the data is stored
          bucket_folder_name (str): The name of the folder in the S3 bucket that contains the data to beexported into the feature store.
          feature_store_folder_name (str): The folder name in the feature store
        """
        logging.info(
            "Entered export_data_into_feature_store method of DataIngestion class"
        )

        try:
            logging.info(
                f"Syncing {bucket_folder_name} folder from {bucket_name} to {feature_store_folder_name}"
            )

            self.s3.sync_folder_from_s3(
                folder=feature_store_folder_name,
                bucket_name=bucket_name,
                bucket_folder_name=bucket_folder_name,
            )

            logging.info(
                f"Synced {bucket_folder_name} folder from {bucket_name} to {feature_store_folder_name}"
            )

            logging.info(
                "Exited export_data_into_feature_store method of DataIngestion class"
            )

        except Exception as e:
            raise NetworkException(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of DataIngestion class")

        try:
            self.export_data_into_feature_store(
                bucket_name=self.data_ingestion_config.data_ingestion_bucket_name,
                bucket_folder_name=self.data_ingestion_config.data_ingestion_bucket_folder_name,
                feature_store_folder_name=self.data_ingestion_config.data_ingestion_feature_store_folder_name,
            )

            data_ingestion_artifact: DataIngestionArtifact = DataIngestionArtifact(
                feature_store_folder_path=self.data_ingestion_config.data_ingestion_feature_store_folder_name
            )

            logging.info(f"Data Ingestion artifact is : {data_ingestion_artifact}")

            logging.info("Exited initiate_data_ingestion method of DataIngestion class")

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkException(e, sys)
