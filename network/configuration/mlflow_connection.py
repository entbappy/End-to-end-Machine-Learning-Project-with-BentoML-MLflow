import os

from mlflow.client import MlflowClient

from network.constant.env_variable import MLFLOW_TRACKING_URI_KEY


class MLFlowClient:
    client = None

    def __init__(self):
        if MLFlowClient.client == None:
            __mlflow_tracking_uri = os.getenv(MLFLOW_TRACKING_URI_KEY)

            if __mlflow_tracking_uri is None:
                raise Exception(
                    f"Environment variable: {MLFLOW_TRACKING_URI_KEY} is not set."
                )

            MLFlowClient.client = MlflowClient(tracking_uri=__mlflow_tracking_uri)

        self.client = MLFlowClient.client
