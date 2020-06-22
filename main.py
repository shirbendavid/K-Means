from tkinter import filedialog
import tkinter.messagebox as messageBox

from CleanData import *
from Clustering import *
import pandas as pd
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


class KmeansClustering:
    # data members
    file_path = ""
    n_clusters = 0
    n_init = 0
    df = None
    clustering = None
    cleanData = None

    # Initialize the GUI
    def __init__(self, master):
        self.map_label = PhotoImage(file="map.gif")
        self.scatter_label = PhotoImage(file='scatter.gif')
        self.master = master
        master.title("K Means Clustering")
        master.configure(background="pink")
        # master.geometry("650x300")

        # Data path
        self.labelPath = Label(master, text="File Path:").grid(row=1, column=0)
        self.entryPath = Entry(master, width=70)
        self.entryPath.grid(row=1, column=1)
        self.browse_button = Button(master, text="Browse", width=10, command=self.chooseFile)
        self.browse_button.grid(row=1, column=2)
        # Number of clusters
        self.labelClusterNumber = Label(master, text="Number of clusters k:").grid(row=2, column=0)
        self.entryClusterNumber = Entry(master, width=20, validate="key")
        self.entryClusterNumber.grid(row=2, column=1)

        # Number of runs
        self.labelRunsNumber = Label(master, text="Number of runs:").grid(row=3, column=0)
        self.entryRunsNumber = Entry(master, width=20, validate="key")
        self.entryRunsNumber.grid(row=3, column=1)

        # pre processing
        self.clean_button = Button(master, text="Pre-process", width=20, command=self.clean)
        self.clean_button.grid(row=4, column=0)

        # Clustrization
        self.cluster_button = Button(master, text="Cluster", width=20, command=self.cluster, state=DISABLED)
        self.cluster_button.grid(row=5, column=0)

        # Close
        self.close_button = Button(master, text="Exit", width=10, command=master.quit)
        self.close_button.grid(row=5, column=2)

    def chooseFile(self):
        self.file_path = filedialog.askopenfilename()
        self.entryPath.delete(0, END)
        self.entryPath.insert(0, self.file_path)

        # if not self.file_path:
        # tkMessageBox.showinfo("K Means Clustering", "insert a file")
        # return
        if not (self.file_path.endswith("xlsx") or self.file_path.endswith("xls")):
            messageBox.showerror("K Means Clustering", "insert an excel file")
            return

        self.df = pd.read_excel(self.file_path)

        if self.df.empty:
            messageBox.showerror("K Means Clustering", "invalid file!")
            return

    # pre processing
    def clean(self):
        if self.validate(self.entryClusterNum.get(), self.entryInitNum.get(), self.file_path):
            self.dataCleaner = CleanData(self.df).Clean()
            messageBox.showinfo("K Means Clustering", "Preprocessing completed successfully!")
            self.cluster_button.config(state=NORMAL)

    def cluster(self):
        self.clustering = Clustering(self.dataCleaner, int(self.entryClusterNum.get()), int(self.entryInitNum.get()))
        self.clustering.cluster()

        # show images in gui
        # image1 = r'./scatter.gif'
        # scatter = PhotoImage(file=image1)
        # self.scatter_label.image = scatter

        # image2 = r'./map.gif'
        # map = PhotoImage(file=image2)
        # self.map_label.image = map

        # self.scatter_label.grid(row=8, column=0, columnspan=2, sticky=W)
        # self.map_label.grid(row=8, column=2, columnspan=2, sticky=E)
        scatter_image = Image.open('scatter.gif')
        scatter_plot_photo = ImageTk.PhotoImage(scatter_image)
        map_image = Image.open('map.gif')
        map_photo = ImageTk.PhotoImage(map_image)
        lab1 = Label(image=scatter_plot_photo)
        lab1.image = scatter_plot_photo
        lab1.grid(row=6, column=1)
        lab2 = Label(root, image=map_photo)
        lab2.image = map_photo
        lab2.grid(row=6, column=0)
        messageBox.showinfo("K Means Clustering", "Cluster completed successfully!")

    def validate(self, cluster, init, path):
        if path == "":
            # the field is being cleared
            messageBox.showerror("K Means Clustering", "Please enter path")
            return False
        if not cluster and not init:  # the field is being cleared
            messageBox.showerror("K Means Clustering", "Please enter values")
            return False
        if not cluster:  # the field is being cleared
            messageBox.showerror("K Means Clustering", "Please enter number of clusters")
            return False
        if not init:  # the field is being cleared
            messageBox.showerror("K Means Clustering", "Please enter number of runs")
            return False
        try:
            self.n_clusters = int(cluster)
            self.n_init = int(init)
            # check validate number
            if self.n_clusters < 1:
                messageBox.showerror("K Means Clustering", "The number for clusters should be bigger than 0")
                return False
            elif self.n_clusters > len(self.df.columns):
                messageBox.showerror("K Means Clustering",
                                     "Num of clusters shouldn't be higher then the number of columns")
                return False
            elif self.n_init < 1:
                messageBox.showerror("K Means Clustering", "The number for runs should be bigger than 0")
                return False
            else:
                return True

        except ValueError:
            messageBox.showerror("K Means Clustering",
                                 "Invalid input - Please enter a number")
            return False


root = tk.Tk()
my_gui = KmeansClustering(root)
root.mainloop()
