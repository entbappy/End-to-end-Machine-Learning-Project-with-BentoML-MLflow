import bentoml
import numpy as np
from bentoml import Service
from bentoml._internal.runner import Runner
from bentoml.io import NumpyNdarray

from network.constant import training_pipeline

runner: Runner = bentoml.mlflow.get(
    training_pipeline.MODEL_PUSHER_BENTOML_MODEL_NAME
).to_runner()

svc: Service = Service(
    name=training_pipeline.MODEL_PUSHER_BENTOML_SERVICE_NAME, runners=[runner]
)


@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def classify(input_series: np.ndarray) -> np.ndarray:
    result = runner.predict.run(input_series)

    return result
