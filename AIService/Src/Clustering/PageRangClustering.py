from typing import Callable

import numpy as np

from Src.Clustering.utils import *
from Src.Clustering.clustering import clustering



class PageRangClustering(clustering):
  weights_func: Callable
  distance_func: Callable
  threshold_func: Callable
  threshold: float

  colors: np.ndarray
  centers: list

  def __init__(self, weights_func: Callable = cosine_weights, distance_func: Callable = l2_distance ,
               threshold_func: Callable = threshold_otsu, threshold: float = None):
    self.weights_func = weights_func
    self.distance_func = distance_func
    self.threshold_func = threshold_func
    if threshold:
      self.threshold_func = lambda: threshold


  def fit_transform(self, data, n_clusters: int = 2):
    weights = self.weights_func(data)
    self.colors = np.zeros(weights.shape)
    self.centers = []
    color = 0
    for _ in range(n_clusters):
      weights[self.colors != 0] = -np.inf
      self.centers.append(np.argmax(weights))
      cluster_center = data[self.centers[-1]]
      distances = 0.1 / self.distance_func(data, cluster_center)
      mask = np.logical_and(self.colors == 0, np.isfinite(distances))

      thresh = self.threshold_func(distances[mask])

      color += 1
      self.colors[np.logical_and(self.colors == 0, distances > thresh)] = color
    return self.centers