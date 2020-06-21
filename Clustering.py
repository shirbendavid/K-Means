import os
import pandas as pd
import matplotlib.pyplot as plt
import chart_studio.plotly as py
from PIL import Image
from sklearn.cluster import KMeans


class Clustering:

    kmeans = pd.DataFrame({})
    df = pd.DataFrame({})
    n_clusters = 0
    n_init = 0

    def __init__(self,data,n_clusters, n_init):
        self.df = data
        self.n_clusters = n_clusters
        self.n_init = n_init

    #cluster flow
    def cluster(self):
        self.calcKmeans()
        self.drawScatter()
        self.horoplethMap()
        self.ConvertPngToGif()

    #kmeans function
    def calcKmeans(self):
        self.kmeans = KMeans(n_clusters=self.n_clusters, n_init=self.n_init).fit(self.df)
        self.df["cluster"]= self.kmeans.labels_
        self.df.reset_index(level=0, inplace=True)
        self.df["code"]=self.df["country"].str[:3]
        self.df["code"] = self.df["code"].str.upper()
        return self.df

    #scatter
    def drawScatter(self):
        cm = plt.cm.get_cmap('RdYlBu')
        sc = plt.scatter(x=self.df["Social support"], y=self.df["Generosity"], c=self.df["cluster"])
        plt.title("K-Meams Clustering")
        plt.ylabel("Generosity")
        plt.xlabel("Social support")
        plt.colorbar(sc)
        plt.savefig("./scatter.png")

    #map
    def horoplethMap(self):
        #username: ilanamor
        # PuJAQXTCGxrq3pgAHvqo

        data = [dict(
            type='choropleth',
            locations=self.df['code'],
            z=self.df['cluster'],
            text=self.df['country'],
            colorscale=[[0, "rgb(5, 10, 172)"], [0.35, "rgb(40, 60, 190)"], [0.5, "rgb(70, 100, 245)"], \
                        [0.6, "rgb(90, 120, 245)"], [0.7, "rgb(106, 137, 247)"], [1, "rgb(220, 220, 220)"]],
            autocolorscale=False,
            reversescale=True,
            marker=dict(
                line=dict(
                    color='rgb(180,180,180)',
                    width=0.5
                )),
            colorbar=dict(
                autotick=False,
                #tickprefix='$',
                title='Cluster Group'),
        )]

        layout = dict(
            title='K-Means Clustering Visualization',
            geo=dict(
                showframe=True,
                showcoastlines=False,
                projection=dict(
                    type='Mercator'
                )
            )
        )
        py.sign_in("shirbendor", "ByDLoTeQOewal6U26ATM")
        #py.tools.set_credentials_file(username="shirbendor", api_key="ByDLoTeQOewal6U26ATM")
        fig = dict(data=data, layout=layout)
        py.iplot(fig, validate=False, filename='d3-world-map')
        py.image.save_as(fig, filename="./map.png")

    #convert images from png to gif
    def ConvertPngToGif(self):

        scatter = Image.open('./scatter.png')
        map = Image.open('./map.png')

        scatter = scatter.resize((450, 350), Image.ANTIALIAS)
        scatter.convert('RGB').convert('P', palette=Image.ADAPTIVE)
        scatter.save('./scatter.gif')
        os.remove('./scatter.png')

        map = map.resize((450, 350), Image.ANTIALIAS)
        map.convert('RGB').convert('P', palette=Image.ADAPTIVE)
        map.save('./map.gif')
        os.remove('./map.png')

