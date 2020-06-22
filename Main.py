from tkinter import filedialog
import tkinter.messagebox as message_box

from PreProcessing import *
from Clustering import *
import pandas as pd
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk


class Main:
    df = None
    clustering = None
    preProcessing = None
    file_path = ""
    clusters_number = 0
    runs_number = 0

    # GUI
    def __init__(self, master):

        self.master = master
        master.title("K Means Clustering")
        master.configure(background="pink")

        # Data path
        self.labelPath = Label(master, text="File Path:").grid(row=1, column=0, sticky=W)
        self.entryPath = Entry(master, width=100)
        self.entryPath.grid(row=1, column=1, sticky=W)
        self.browse_button = Button(master, text="Browse", width=10, command=self.open_file)
        self.browse_button.grid(row=1, column=1, sticky=E)

        # Number of clusters
        self.labelClusterNumber = Label(master, text="Number of clusters k:").grid(row=2, column=0, sticky=W)
        self.entryClusterNumber = Entry(master, width=20, validate="key")
        self.entryClusterNumber.grid(row=2, column=1, sticky=W)

        # Number of runs
        self.labelRunsNumber = Label(master, text="Number of runs:").grid(row=3, column=0, sticky=W)
        self.entryRunsNumber = Entry(master, width=20, validate="key")
        self.entryRunsNumber.grid(row=3, column=1, sticky=W)

        # pre processing
        self.pre_processing_button = Button(master, text="Pre-process", width=25, command=self.pre_processing)
        self.pre_processing_button.grid(row=4, column=1, sticky=W)

        # Clustering
        self.cluster_button = Button(master, text="Cluster", width=25, command=self.cluster, state=DISABLED)
        self.cluster_button.grid(row=5, column=1, sticky=W)

    def open_file(self):
        self.file_path = filedialog.askopenfilename()
        self.entryPath.delete(0, END)
        self.entryPath.insert(0, self.file_path)

        if not (self.file_path.endswith("xlsx") or self.file_path.endswith("xls")):
            message_box.showerror("K Means Clustering", "insert only excel file!")
            return

        self.df = pd.read_excel(self.file_path)

        if self.df.empty:
            message_box.showerror("K Means Clustering", "invalid file!")
            return

    # pre processing
    def pre_processing(self):
        if self.input_tests(self.entryClusterNumber.get(), self.entryRunsNumber.get(), self.file_path):
            self.preProcessing = PreProcessing(self.df).clean()
            message_box.showinfo("K Means Clustering", "Preprocessing completed successfully!")
            self.cluster_button.config(state=NORMAL)

    def cluster(self):
        self.clustering = Clustering(self.preProcessing, int(self.entryClusterNumber.get()),
                                     int(self.entryRunsNumber.get()))
        self.clustering.cluster()

        # show images
        scatter_image = Image.open('scatter.png')
        scatter_image = scatter_image.resize((500, 400), Image.ANTIALIAS)
        scatter = ImageTk.PhotoImage(scatter_image)
        map_image = Image.open('map.png')
        map_image = map_image.resize((500, 400), Image.ANTIALIAS)
        map_plot = ImageTk.PhotoImage(map_image)

        scatter_label = Label(image=scatter)
        scatter_label.image = scatter
        scatter_label.grid(row=6, column=2)
        map_label = Label(root, image=map_plot)
        map_label.image = map_plot
        map_label.grid(row=6, column=1)

        message_box.showinfo("K Means Clustering", "Cluster completed successfully!")

    def input_tests(self, cluster_number, runs_number, path):
        # check entry
        if path == "":
            message_box.showerror("K Means Clustering", "Please enter path")
            return False
        if not cluster_number and not runs_number:
            message_box.showerror("K Means Clustering", "Please enter values")
            return False
        if not cluster_number:
            message_box.showerror("K Means Clustering", "Please enter number of clusters")
            return False
        if not runs_number:
            message_box.showerror("K Means Clustering", "Please enter number of runs")
            return False
        try:
            self.clusters_number = int(cluster_number)
            self.runs_number = int(runs_number)
            # check validate number
            if self.clusters_number < 1:
                message_box.showerror("K Means Clustering", "The number for clusters should be bigger than 0")
                return False
            elif self.clusters_number > len(self.df.columns):
                message_box.showerror("K Means Clustering",
                                      "The number of clusters shouldn't be higher then the number of columns")
                return False
            elif self.runs_number < 1:
                message_box.showerror("K Means Clustering", "The number for runs should be bigger than 0")
                return False
            else:
                return True

        except ValueError:
            message_box.showerror("K Means Clustering",
                                  "Invalid input - Please enter a number")
            return False


root = tk.Tk()
my_gui = Main(root)
root.mainloop()
