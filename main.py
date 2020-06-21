from tkinter import filedialog
import tkinter.messagebox as messageBox

from CleanData import *
from Clustering import *
import pandas as pd
import tkinter as tk
from tkinter import *


def gridDefinition(master):
    master.grid_rowconfigure(0, weight=2)
    master.grid_rowconfigure(1, weight=1)
    master.grid_rowconfigure(2, weight=1)
    master.grid_rowconfigure(3, weight=1)
    master.grid_rowconfigure(4, weight=1)
    master.grid_rowconfigure(5, weight=1)
    master.grid_rowconfigure(6, weight=1)
    master.grid_rowconfigure(7, weight=1)
    master.grid_columnconfigure(0, weight=1)
    master.grid_columnconfigure(1, weight=1)
    master.grid_columnconfigure(2, weight=1)
    master.grid_columnconfigure(3, weight=2)


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
        #self.map_label = Label(image=map, width='450px', height='350px')
        #self.scatter_label = Label(image=scatter, width='450px', height='350px')
        self.master = master
        master.title("K Means Clustering")
        # master.geometry("650x300")

        # Data path
        self.labelPath = Label(master, text="File Path:")
        self.entryPath = Entry(master, width=70)
        self.browse_button = Button(master, text="Browse", width=10, command=self.chooseFile)
        #self.browse_button.pack()

        # Num of clusters
        self.labelClusterNum = Label(master, text="Num of clusters k:")
        self.entryClusterNum = Entry(master, width=20, validate="key")

        # Num of runs
        self.labelInitNum = Label(master, text="Num of runs:")
        self.entryInitNum = Entry(master, width=20, validate="key")

        # pre processing
        self.clean_button = Button(master, text="Pre-process", width=20, command=self.clean)
        #self.clean_button.pack()

        # Clustrization
        self.cluster_button = Button(master, text="Cluster", width=20, command=self.cluster, state=DISABLED)
        #self.cluster_button.pack()

        # Close
        self.close_button = Button(master, text="Exit", width=10, command=master.quit)
        #self.close_button.pack()

        # Define grid
        gridDefinition(master)
        # layout the controls in the grid
        self.controlsLayout()

    def controlsLayout(self):
        self.labelPath.grid(row=1, column=0, sticky=E)
        self.entryPath.grid(row=1, column=1, columnspan=2, sticky=W)
        self.browse_button.grid(row=1, column=3, sticky=W)
        self.labelClusterNum.grid(row=2, column=0, sticky=E)
        self.entryClusterNum.grid(row=2, column=1, sticky=W)
        self.labelInitNum.grid(row=3, column=0, sticky=E)
        self.entryInitNum.grid(row=3, column=1, sticky=W)
        self.clean_button.grid(row=5, column=1, columnspan=2)
        self.cluster_button.grid(row=6, column=1, columnspan=2)
        self.close_button.grid(row=10, column=1, columnspan=2)

    def chooseFile(self):
        self.file_path = filedialog.askopenfile()
        self.entryPath.delete(0, END)
        self.entryPath.insert(0, self.file_path)

        if not self.file_path:
            # tkMessageBox.showinfo("K Means Clustering", "insert a file")
            return

        if not (self.file_path[-5:] == ".xlsx" or self.file_path[-4:] == ".xls"):
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
        image1 = r'./scatter.gif'
        scatter = PhotoImage(file=image1)
        self.scatter_label.image = scatter

        image2 = r'./map.gif'
        map = PhotoImage(file=image2)
        self.map_label.image = map

        self.scatter_label.grid(row=8, column=0, columnspan=2, sticky=W)
        self.map_label.grid(row=8, column=2, columnspan=2, sticky=E)
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
