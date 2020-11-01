# -*-coding:Utf-8 -*
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
import os
from pathlib import Path
import json
from tkinter.messagebox import *
import math

#### TODO ####
# Add validation message when saving configuration
# BONUS : 
# Make the process repeatable by adding Project section dynamically

class LFVegasProject:
    def __init__(self, parent, frameNumber):
        lf_vegasProject = ttk.LabelFrame(parent, text="Vegas Project")
        # Make col of 5 row, with a colspan of 3 columns
        # Row begin at 2 because this section is the third element of the global window
        lf_vegasProject.grid(row=frameNumber%5+2, column=math.floor(frameNumber/5)*3, columnspan=3, padx=5, pady=5, sticky=(N, W, E, S))
        self.pathVegasProject = StringVar()
        ttk.Label(lf_vegasProject, text="Please indicate path to your Vegas project : ").grid(row=0, column=0, sticky=(W, E))
        ttk.Entry(lf_vegasProject, state="readonly", width=50, textvariable=self.pathVegasProject).grid(row=0, column=1, sticky=(W, E))
        ttk.Button(lf_vegasProject, text="Select Vegas project path", command=self.selectVegasProject).grid(row=0, column=2, sticky=W)

        self.pathOutput = StringVar()
        ttk.Label(lf_vegasProject, text="Please indicate output path of the video : ").grid(row=1, column=0, sticky=(W, E))
        ttk.Entry(lf_vegasProject, width=50, state="readonly", textvariable=self.pathOutput).grid(row=1, column=1, sticky=(W, E))
        ttk.Button(lf_vegasProject, text="Select video output directory", command=self.seletPathOutput).grid(row=1, column=2, sticky=W)

        self.videoName = StringVar()
        ttk.Label(lf_vegasProject, text="Please indicate the name of the video (without suffix) : ").grid(row=2, column=0, sticky=(W, E))
        entryVideoName = ttk.Entry(lf_vegasProject, width=50, textvariable=self.videoName)
        entryVideoName.grid(row=2, column=1, sticky=(W, E))
        entryVideoName.bind('<KeyRelease>', self.refreshVideoNameLabel)

        ttk.Label(lf_vegasProject, text="Choose the type of encoding : ").grid(row=3, column=0, sticky=(W, E))
        self.rendererMethod = StringVar()
        comboRendererMethod = ttk.Combobox(lf_vegasProject, textvariable=self.rendererMethod, state="readonly", values=('MP4', 'WMV'))
        comboRendererMethod.grid(row=3, column=1, sticky=W)
        comboRendererMethod.current(0)
        comboRendererMethod.bind('<<ComboboxSelected>>', self.comboRendererMethodChanged)

        self.outputPathLabel = StringVar()
        ttk.Label(lf_vegasProject, text="Output path : ").grid(row=4, column=0, sticky=(W, E))       
        ttk.Label(lf_vegasProject, textvariable=self.outputPathLabel).grid(row=4, column=1, sticky=(W, E))
        
        for child in lf_vegasProject.winfo_children():
            child.grid_configure(padx=1, pady=1)
        # How to modify the list of all Video config when remonving one?
        # And how re organize the windows
        #ttk.Button(lf_vegasProject, text="remove video configuration", command=lambda: lf_vegasProject.destroy()).grid(row=5, column=1, sticky=(W, E))

    def selectVegasProject(self):
        filename = askopenfilename(filetypes=[("Vegas Project", ".veg")])
        if filename:
            self.pathVegasProject.set(filename)

    def seletPathOutput(self):
            directoryPath = askdirectory(initialdir=self.pathVegasProject.get())
            if directoryPath:
                self.pathOutput.set(directoryPath)
                self.refreshVideoNameLabel()

    # adding optionnal argument to handle the call by modifying entry wich send event param
    def refreshVideoNameLabel(self, *args):
        if self.pathOutput.get():
            if self.videoName.get():
                if self.rendererMethod.get() == "MP4":
                    self.outputPathLabel.set(self.pathOutput.get()+"/"+self.videoName.get()+".mp4")
                else:
                    self.outputPathLabel.set(self.pathOutput.get()+"/"+self.videoName.get()+".wmv")
            else:
                self.outputPathLabel.set(self.pathOutput.get()+"/")

    def comboRendererMethodChanged(self, event):
        if self.outputPathLabel.get():
            if self.rendererMethod.get() == "MP4":
                self.outputPathLabel.set(self.outputPathLabel.get().replace(".wmv", ".mp4"))
            else:
                self.outputPathLabel.set(self.outputPathLabel.get().replace(".mp4", ".wmv"))