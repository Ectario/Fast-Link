
import tkinter as tk
import webbrowser
import pickle
import sys
from functools import partial


#This file is made by Ectario


DATA_FILE_NAME= "dataFastLink"
BTN_BACKGROUND= 'grey'


#ScrollFrame from https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01

class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas
        self.vsb.pack(side="right", fill="y")                                      #pack scrollbar to right of self
       
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.



class Application(tk.Frame):
    def __init__(self,root):
        tk.Frame.__init__(self,root)
        self.scrollFrame = ScrollFrame(self)
        self.buttonList = []

        self.donnees = self.readSave()

        buttonExit = tk.Button(self.scrollFrame.viewPort, text="Quitter", command= exit)
        buttonExit['bg'] = 'orange'
        buttonExit.pack(side="top", fill="both",expand=True)

        addContainer = tk.Label(self.scrollFrame.viewPort,text="")
        addContainer.pack(side="top",anchor="w",fill="both",expand=True)

        nameLabel = tk.Label(self.scrollFrame.viewPort,text="Nom :")
        nameLabel.pack(in_=addContainer,anchor="w",fill="y")
        nameEntry = tk.Entry(self.scrollFrame.viewPort)
        nameEntry.pack(in_=addContainer,anchor="center",fill="both")

        urlLabel = tk.Label(self.scrollFrame.viewPort,text="URL/lien :")
        urlLabel.pack(in_=addContainer,anchor="w",fill="y")
        urlEntry = tk.Entry(self.scrollFrame.viewPort)
        urlEntry.pack(in_=addContainer,anchor="center",fill="both")

        buttonAdd = tk.Button(self.scrollFrame.viewPort, text="Ajouter", command= lambda: self.add(nameEntry.get(),urlEntry.get()))
        buttonAdd['bg'] = 'green'
        buttonAdd.pack(in_=addContainer,side="right",fill="y")

        delContainer = tk.Label(self.scrollFrame.viewPort,text="")
        delContainer.pack(side="top",anchor="w",fill="both",expand=True)

        nameDelLabel = tk.Label(self.scrollFrame.viewPort,text="Nom (pour suppression):")
        nameDelLabel.pack(in_=delContainer,anchor="w",fill="y")
        nameDelEntry = tk.Entry(self.scrollFrame.viewPort)
        nameDelEntry.pack(in_=delContainer,anchor="center",fill="both")

        buttonDel = tk.Button(self.scrollFrame.viewPort, text="Supprimer", command= lambda: self.delete(nameDelEntry.get()))
        buttonDel['bg'] = 'red'
        buttonDel.pack(in_=delContainer,side="right",fill="y")

        if self.donnees!= None:
            for i in self.donnees:
                action = partial(self.searchZoom, i)
                newButton = tk.Button(self.scrollFrame.viewPort, text=i, command=action)
                newButton['bg'] = BTN_BACKGROUND
                newButton.pack(side="top", fill="both", expand=True)
                self.buttonList.append(newButton)
            self.scrollFrame.pack(side="top", fill="both", expand=True)
        

    def searchZoom(self,tag):
        url = self.donnees[tag]
        webbrowser.open_new_tab(url)

    def exit(self):
        self.quit
        sys.exit()

    def add(self,name,url):
        newButton = tk.Button(self.scrollFrame.viewPort, text=name, command= lambda: self.searchZoom(name))
        newButton['bg'] = BTN_BACKGROUND
        newButton.pack(side="top", fill="both", expand=True)
        self.buttonList.append(newButton)
        self.donnees[name] = url
        self.writeSave(self.donnees)

    def delete(self,name):
        for i in self.buttonList:
            if i['text'] == name:
                self.buttonList.remove(i)
                try:
                    self.donnees.pop(name)
                    self.writeSave(self.donnees)
                except KeyError:
                    pass
                i.destroy()

    def readSave(self):
        try:
            with open(DATA_FILE_NAME,'rb') as fichier:
                depick=pickle.Unpickler(fichier)
                donnees=depick.load()
        except IOError:
            with open(DATA_FILE_NAME,"wb") as fichier:
                pick=pickle.Pickler(fichier)
                pick.dump({})
                donnees = {}
        return donnees

    def writeSave(self,data):
        with open(DATA_FILE_NAME,"wb") as fichier:
                pick=pickle.Pickler(fichier)
                pick.dump(data)

if __name__ == "__main__":
    root=tk.Tk()
    root.geometry("800x600+325+100")
    app = Application(root).pack(side="top", fill="both", expand=True)
    root.title("Fast Link")
    root.mainloop()
