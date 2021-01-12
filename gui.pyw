# -*-coding:Utf-8 -*
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
import os
from pathlib import Path
import json
from tkinter.messagebox import *
from LFVegasProject import *

#### TODO ####
# Uncomment to have the right vegas project selector (filter .veg)
# Clean import section
# BONUS : Allow to remove video configuration
# BONUS : Add video configuration side by side instead of one under other?
# BONUS : Better management of resizing
# Bonus : Make fields read-only more visible, same for combobox

class ConfigFile:
    def __init__(self, vegasPath, videos): # Notre méthode constructeur
        self.vegasPath = vegasPath.replace("/", "\\")
        self.videos = videos

class VideoConfig:
    def __init__(self, projectFilePath, outputFilePath, rendererMethod): # Notre méthode constructeur
        self.projectFilePath = projectFilePath.replace("/", "\\")
        self.outputFilePath = outputFilePath.replace("/", "\\")
        if rendererMethod == "MP4":
            self.rendererName = "MAGIX AVC/AAC MP4"
            self.templateName = "Internet HD 1080p 50 fps"
        else:
            self.rendererName = "Windows Media Video V11"
            self.templateName = "Vidéo HD 1080-30p 8 Mbits/s"

    def __repr__(self):
        return self.projectFilePath + "," + self.outputFilePath + "," + self.rendererName + "," + self.templateName

    def dump(self):
        return {'projectFilePath': self.projectFilePath,
                                'rendererName': self.rendererName,
                                'templateName': self.templateName,
                                'outputFilePath': self.outputFilePath}

class VegasRenderingConfiguration:
    def __init__(self, root):
        self.listLFVegasProject = []
        root.title("Vegas renderer configuration")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.mainframe = ttk.Frame(root)
        self.mainframe.grid(row=0, column=0, sticky=(N, W, E, S))
        ttk.Label(self.mainframe, text="Configuration of Vegas rendering script").grid(row=0, column=0, columnspan=6, pady=5, sticky=(N))

        lf_vegasExec = ttk.LabelFrame(self.mainframe, text="Vegas Executable")
        lf_vegasExec.grid(row=1, column=0, columnspan=6, padx=5, pady=5, sticky=(N, W, E, S))
        self.pathVegasExecutable = StringVar()
        ttk.Label(lf_vegasExec, text="Please indicate path to your Vegas executable").grid(row=0, column=0, sticky=(W, E))
        ttk.Entry(lf_vegasExec, state="readonly", width=50, textvariable=self.pathVegasExecutable).grid(row=0, column=1, sticky=(W, E))
        ttk.Button(lf_vegasExec, text="Select Vegas executable", command=self.selectVegasExec).grid(row=0, column=2, sticky=W)

        self.addNewVideo()

        # Row 100 and 101 to be sure to keep the button at the bottom of the window
        ttk.Button(self.mainframe, text="Add new video", command=self.addNewVideo).grid(row=100, column=1, sticky=(E, W))

        ttk.Button(self.mainframe, text="Save configuration", command=self.saveConfiguration).grid(row=101, column=2, padx=5, pady=5, sticky=(S,E))

    def selectVegasExec(self):
        filename = askopenfilename(initialdir=os.environ["ProgramFiles"], filetypes=[("Exe files", ".exe")])
        self.pathVegasExecutable.set(filename)

    def addNewVideo(self):
        if (len(self.listLFVegasProject) < 10):
            self.listLFVegasProject.append(LFVegasProject(self.mainframe, len(self.listLFVegasProject)))
        else:
            showerror(title="No more video configuration", message="You can't configure more than 10 video at once")

    def checkIfAllFieldsAreFilled(self):
        for currentVideoConfiguration in (self.listLFVegasProject):
            if (not currentVideoConfiguration.pathVegasProject.get() or 
                not currentVideoConfiguration.outputPathLabel.get() or
                not currentVideoConfiguration.videoName.get()):
                return False
        return True
        

    def saveConfiguration(self): 
        if self.pathVegasExecutable.get():
            if self.checkIfAllFieldsAreFilled():
                confirmSavingAndQuitting = askokcancel (" Save configuration", "Are you sure to save the configuration and quit the programm ?")
                if confirmSavingAndQuitting:
                    allVideoConfiguration = [VideoConfig(currentVideoConfiguration.pathVegasProject.get(), 
                        currentVideoConfiguration.outputPathLabel.get(), 
                        currentVideoConfiguration.rendererMethod.get()) for currentVideoConfiguration in (self.listLFVegasProject)]
                    with open('../config.json', 'w', encoding='utf8') as json_file:
                        json.dump(ConfigFile(self.pathVegasExecutable.get(), [o.dump() for o in allVideoConfiguration]).__dict__, json_file, ensure_ascii=False)

                    showinfo(title="Configuration saved", message="Your video configuration has been saved")
                    root.destroy()
            else:
                showerror(title="Configuration missing", message="Some fields are missing")
        else:
            showerror(title="Configuration missing", message="Please indicate the path to your Vegas executable")

root = Tk()
root.iconbitmap('Vegas_Pro_15.0.ico')
root.resizable(False, False)
VegasRenderingConfiguration(root)

# Following code about centering window find here 
# => https://yagisanatode.com/2018/02/24/how-to-center-the-main-window-on-the-screen-in-tkinter-with-python-3/
# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/4 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/6 - windowHeight/2)
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))

root.mainloop()

