from typing import Protocol


class clustering(Protocol):

    def fit_transform(self, data, n_clusters: int = 2):
        pass