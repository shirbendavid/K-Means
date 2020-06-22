import pandas as pd
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import plotly.graph_objects as go
from sklearn.cluster import KMeans


class Clustering:
    k_means = pd.DataFrame({})
    df = pd.DataFrame({})
    n_clusters = 0
    n_init = 0

    def __init__(self, data, clusters, runs):
        self.df = data
        self.n_clusters = clusters
        self.n_init = runs

    def cluster(self):
        self.k_means_algorithm()
        self.draw_scatter_image()
        self.draw_map_image()

    # k_means algorithm
    def k_means_algorithm(self):
        self.k_means = KMeans(n_clusters=self.n_clusters, n_init=self.n_init).fit(self.df)
        self.df["cluster"] = self.k_means.labels_
        self.df.reset_index(level=0, inplace=True)
        self.df["code"] = self.df["country"].str[:3]
        self.df["code"] = self.df["code"].str.upper()
        return self.df

    # scatter
    def draw_scatter_image(self):
        sc = plt.scatter(x=self.df["Social support"], y=self.df["Generosity"], c=self.df["cluster"])
        plt.title("K Means Clustering")
        plt.ylabel("Generosity")
        plt.xlabel("Social support")
        plt.colorbar(sc)
        plt.savefig("./scatter.png")

    # map
    def draw_map_image(self):
        df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
        fig = go.Figure(data=go.Choropleth(
            locations=df['CODE'],
            z=self.df['cluster'],
            text=self.df['country'],
            colorscale='Blues',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title='Cluster Group',
        ))
        fig.update_layout(
            title_text='K Means Clustering Visualization',
            geo=dict(
                showframe=True,
                showcoastlines=False,
                projection_type='equirectangular'
            ),
            annotations=[dict(
                x=0.55,
                y=0.1,
                xref='paper',
                yref='paper',
                showarrow=False
            )]
        )
        py.sign_in("shirbendor", "ByDLoTeQOewal6U26ATM")
        py.image.save_as(fig, filename="./map.png")

