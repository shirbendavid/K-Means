import os
import pandas as pd
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import plotly.graph_objects as go
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
        df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

        fig = go.Figure(data=go.Choropleth(
            locations=df['CODE'],
            z=df['GDP (BILLIONS)'],
            text=df['COUNTRY'],
            colorscale='Blues',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_tickprefix='$',
            colorbar_title='GDP<br>Billions US$',
        ))

        fig.update_layout(
            title_text='2014 Global GDP',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),
            annotations=[dict(
                x=0.55,
                y=0.1,
                xref='paper',
                yref='paper',
                text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
                    CIA World Factbook</a>',
                showarrow=False
            )]
        )

        fig.show()
        py.sign_in("shirbendor", "ByDLoTeQOewal6U26ATM")
        #fig = dict(data=data, layout=layout)
        #py.iplot(fig, validate=False, filename='d3-world-map')
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

