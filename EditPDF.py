# https://www.python-course.eu/tkinter_events_binds.php

from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from PIL import ImageTk, Image
from pdf2image import convert_from_path
from PyPDF2 import PdfFileMerger
from tkinter import messagebox
from tkinter import simpledialog
import functools
import os

POPPLER =  os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "\\poppler-0.67.0\\bin")

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text, other):
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self, other):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class PDFEditor: 

    def saveFile(self):
        if(self.combo.get()=="JPG a PDF"):
            
            images = []

            for file in self.files:
                images.append(Image.open(file[0]).convert('RGB'))
            
            file = filedialog.asksaveasfilename(filetypes = [('pdf file', '*.pdf')], defaultextension = [('pdf file', '*.pdf')], initialdir="./") 

            images[0].save(file, save_all=True, append_images=images[1:])

            messagebox.showinfo("Aviso","Archivo guardado correctamente")

        elif(self.combo.get()=="Juntar PDF's"):
            
            merger = PdfFileMerger()

            for file in self.files:
                merger.append(open(file[0], 'rb'))

            file = filedialog.asksaveasfilename(filetypes = [('pdf file', '*.pdf')], defaultextension = [('pdf file', '*.pdf')], initialdir="./") 

            with open(file, "wb") as fout:
                merger.write(fout)

            messagebox.showinfo("Aviso","Archivo guardado correctamente")

    def dragPDF(self, event):

        target = -1
        destiny = -1
        temp_names = []

        for i,file in enumerate(self.files):
            if event.widget == file[1]:
                target = i

        for widget in self.frame.winfo_children():
            if widget.winfo_rootx() + 80 > event.x_root > widget.winfo_rootx() and widget.winfo_rooty() + 80 > event.y_root > widget.winfo_rooty():
                for i,file in enumerate(self.files):
                    if widget == file[1]:
                        destiny = i

        if target == -1 or destiny == -1:
            return False
        elif target == destiny:
            return False
        else:

            temp = self.files
            self.files = []

            for i, file in enumerate(temp):
                if i == destiny:
                    temp_names.append(temp[target][0])
                    temp_names.append(file[0])
                elif i != target:
                    temp_names.append(file[0])

            for widget in self.frame.winfo_children():
                widget.destroy()

            self.renderPDFLabel(temp_names)

    def renderPDFLabel(self, files_open):

        j = 0
        i = 0

        for file in files_open:

            if(i>5):
                j += 1
                i = 0

            pdf_file = convert_from_path(file, 0 , poppler_path = POPPLER)
            render = ImageTk.PhotoImage(pdf_file[0].resize((75,75),Image.LANCZOS))
            label = Label(self.frame, image=render)
            label.image = render
            label.config(width=5)
            label.grid(column = i, row = j)
            label.bind("<ButtonRelease>", self.dragPDF)  
            label.bind("<Double-Button-1>", self.dblclick)    

            toolTip = ToolTip(label)

            label.bind('<Button-3>', functools.partial(toolTip.showtip, file))
            label.bind('<Button-1>', toolTip.hidetip)

            i += 1

            self.files.append([file, label])
        
    def renderItems(self, files_open):

        j = 0
        i = 0

        for file in self.files:

            if(i>5):
                j += 1
                i = 0

            load = Image.open(file[0]).resize((75, 75))
            render = ImageTk.PhotoImage(load)
            label = Label(self.frame, image=render)
            label.image = render
            label.config(width=5)
            label.grid(column = i, row = j )
            label.bind("<ButtonRelease>", self.drag)  
            label.bind("<Double-Button-1>", self.dblclick)     

            toolTip = ToolTip(label)

            label.bind('<Button-3>', functools.partial(toolTip.showtip, file))
            label.bind('<Button-1>', toolTip.hidetip)

            i += 1

        for file in files_open:

            if(i>5):
                j += 1
                i = 0
                
            load = Image.open(file).resize((75, 75))
            render = ImageTk.PhotoImage(load)
            label = Label(self.frame, image=render)
            label.image = render
            label.config(width=5)
            label.grid(column = i, row = j )
            label.bind("<ButtonRelease>", self.drag)    
            label.bind("<Double-Button-1>", self.dblclick)

            toolTip = ToolTip(label)

            label.bind('<Button-3>', functools.partial(toolTip.showtip, file))
            label.bind('<Button-1>', toolTip.hidetip)

            self.files.append([file, label])

            i += 1

    def comboSelected(self, event):

        self.files = []
        self.status = 0

        for widget in self.frame.winfo_children():
            widget.destroy()

        if self.combo.get()=="JPG a PDF" :
            self.satus = 0
        elif self.combo.get()=="Juntar PDF's":
            self.status = 1
        else:
            self.status = 2

    def dblclick(self, event):
        temp_names = []

        for i,file in enumerate(self.files):
            if event.widget == file[1]:
                self.files.pop(i)

        temp = self.files
        self.files = []

        for file in temp:
            temp_names.append(file[0])

        for widget in self.frame.winfo_children():
                widget.destroy()

        self.renderItems(temp_names)

    def drag(self ,event):

        target = -1
        destiny = -1
        temp_names = []

        for i,file in enumerate(self.files):
            if event.widget == file[1]:
                target = i

        for widget in self.frame.winfo_children():
            if widget.winfo_rootx() + 80 > event.x_root > widget.winfo_rootx() and widget.winfo_rooty() + 80 > event.y_root > widget.winfo_rooty():
                for i,file in enumerate(self.files):
                    if widget == file[1]:
                        destiny = i

        if target == -1 or destiny == -1:
            return False
        elif target == destiny:
            return False
        else:

            temp = self.files
            self.files = []

            for i, file in enumerate(temp):
                if i == destiny:
                    temp_names.append(temp[target][0])
                    temp_names.append(file[0])
                elif i != target:
                    temp_names.append(file[0])

            for widget in self.frame.winfo_children():
                widget.destroy()

            self.renderItems(temp_names)

    def open_files(self):

        for widget in self.frame.winfo_children():
            widget.destroy()

        filetype = []

        if(self.combo.get()=="JPG a PDF"):

            files_open = filedialog.askopenfilenames(initialdir="./",title="Seleccione los archivos",filetypes=[("jpeg files","*.jpg")])

            if len(files_open) > 36:
                files_open = files_open[0:36]

            self.renderItems(files_open)

        elif (self.combo.get()=="Juntar PDF's"):
            files_open = filedialog.askopenfilenames(initialdir="./",title="Seleccione los archivos",filetypes=[("pdf files","*.pdf")])

            if len(files_open) > 36:
                files_open = files_open[0:36]

            self.renderPDFLabel(files_open)

        else:
            file_open = filedialog.askopenfile(initialdir="./",title="Seleccione los archivos",filetypes=[("pdf files","*.pdf")])

            numbersSTR = simpledialog.askstring("Información", "¿Qué páginas del PDF desea conservar? Ingrese el número de las páginas separado por comas (Ejemplo: 1,2,3)", parent = self.root)
            numbers = numbersSTR.split(",")

            print(file_open.name)

            pdf_file = convert_from_path(file_open.name, 0 , poppler_path = POPPLER)
            images = []

            for number in numbers:
                images.append(pdf_file[int(number) - 1])

            file = filedialog.asksaveasfilename(filetypes = [('pdf file', '*.pdf')], defaultextension = [('pdf file', '*.pdf')], initialdir="./") 

            images[0].save(file, save_all=True, append_images=images[1:])

            messagebox.showinfo("Aviso","Archivo guardado correctamente")

    def __init__(self): 

        self.files = []
        self.destiny = -1
        self.status = 0
          
        self.root = Tk() 
        self.root.geometry('475x500')
        self.root.title("PDF Editor")
        self.root.resizable(False, False)

        top = Frame(self.root)
        bottom = Frame(self.root)
        top.pack(side=TOP)
        bottom.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.combo = Combobox(self.root, width = 15, height = 15, state="readonly")

        self.btn = Button(self.root,text="Abrir archivos", command= self.open_files)
        self.save = Button(self.root,text="Guardar", command= self.saveFile)
        self.combo['values']= ("JPG a PDF", "Juntar PDF's", "Dividir PDF")
        self.combo.current(0)
        self.combo.bind("<<ComboboxSelected>>", self.comboSelected)
        self.btn.pack(side=LEFT)
        self.combo.pack(side=LEFT)
        self.save.pack(side=LEFT)

        self.frame = Frame(self.root, width=35, height=15)
        self.frame.pack(in_=bottom, side=LEFT, fill=BOTH, expand=True)
        
        self.root.mainloop() 
  
s = PDFEditor() 