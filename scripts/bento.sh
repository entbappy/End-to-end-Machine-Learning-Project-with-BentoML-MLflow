#!bin/bash

export BENTOML_MLFLOW_MODEL_PATH=$(bentoml models get $1:latest -o path)

bentoml build
