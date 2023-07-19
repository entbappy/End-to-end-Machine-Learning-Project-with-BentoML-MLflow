import sys

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.metrics import roc_auc_score

from network.entity.artifact_entity import ClassificationMetricArtifact
from network.exception import NetworkException


def calculate_metric(
    model: BaseEstimator, x: pd.DataFrame, y: pd.DataFrame
) -> ClassificationMetricArtifact:
    """
    It takes a model, a dataframe of features, and a dataframe of labels, and returns a classification
    metric.

    Args:
      model (BaseEstimator): BaseEstimator - the model that you want to evaluate
      x (pd.DataFrame): pd.DataFrame
      y (pd.DataFrame): pd.DataFrame

    Returns:
      ClassificationMetricArtifact
    """
    try:
        yhat = model.predict(x)

        classification_metric: float = roc_auc_score(y, yhat)

        return classification_metric

    except Exception as e:
        raise NetworkException(e, sys)
