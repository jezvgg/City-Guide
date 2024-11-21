import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

from Src.Clustering import PageRangClustering, clustering
from Src.Clustering.utils import threshold_otsu


class routes_service:
    cluster: clustering


    @staticmethod
    def create_reponse(obj):
        response = []
        for item in obj: 
            del item['entity']['vector']
            response.append({'id':item['id']} | item['entity'])
        return response

    
    def __init__(self, cluster_alg: clustering = PageRangClustering, *args, **kwargs):
        self.cluster = cluster_alg(*args, **kwargs)

    
    def create_route(self, search_result: list[dict], n_points: int):
        distances = np.array([item["distance"] for item in search_result])
        distance_thresh = threshold_otsu(distances)
        places = [item for item in search_result if item['distance'] < distance_thresh]
        data = np.array([place['entity']['vector'] for place in places])

        centers = self.cluster.fit_transform(data, n_points)
        colors = self.cluster.colors

        plot_data = TSNE().fit_transform(data)
        
        plt.scatter(plot_data[:, 0], plot_data[:, 1], c=colors)
        plt.show()

        return [places[center] for center in centers]
