'''GUI' PYTHON'''

from tkinter import *
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import pandas as pd
import tkinter.filedialog as fd
import Scipy__ as Sc #Zoom class
import os

class MasterPanel():
    def __init__(self):
        self.window = Tk() #Create the window
        self.window.title('PLOT TITLE GEOMETRY == "1800X900" ')  # Title of the window
        self.window.geometry("1800x900") #size in pixels
        self.window.resizable(width=False, height=False) #Whether or not we can resize the window

        self.frame = Frame(self.window, bg='blue')  # FRAME 0
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.frame.config(width='600', height=150)

        self.frame1 = Frame(self.window, bg='black')  # FRAME 1
        self.frame1.grid(row=0, column=1, sticky='nsew')
        self.frame1.config(width='1200', height=150)

        self.frame2 = Frame(self.window, bg='black')  # FRAME 2
        self.frame2.grid(row=1, column=0, sticky='nsew')
        self.frame2.config(width='600', height=600)

        self.frame3 = Frame(self.window, bg='blue')  # FRAME 3
        self.frame3.grid(row=1, column=1, sticky='nsew')
        self.frame3.config(width='1200', height=600)

        self.frame_on0 = Frame(self.frame2, bg='gray')  # FRAME 3.1
        self.frame_on0.grid(row=4, column=0, sticky='nsew')
        self.frame_on0.config(width=200, height=350)

        self.frame_on1 = Frame(self.frame2, bg='blue')  # FRAME 3.2
        self.frame_on1.grid(row=4, column=1, sticky='nsew')
        self.frame_on1.config(width=200, height=350)

        self.frame_on2 = Frame(self.frame2, bg='gray')  # FRAME 3.3
        self.frame_on2.grid(row=4, column=2, sticky='nsew')
        self.frame_on2.config(width=200, height=350)

        self.frame4 = Frame(self.window, bg='blue')  # FRAME 4
        self.frame4.grid(row=2, column=0, sticky='nsew')
        self.frame4.config(width='600', height=150)

        self.frame5 = Frame(self.window, bg='black')  # FRAME 5
        self.frame5.grid(row=2, column=1, sticky='nsew')
        self.frame5.config(width='1200', height=150)

        self.label0 = Label(self.frame2, text='  NEXT FRAME  ', bg='black', fg='white').grid(row=0, column=0, padx=10, pady=5)
        self.label1 = Label(self.frame2, text='PREVIOUS FRAME', bg='black', fg='white').grid(row=0, column=1, padx=10, pady=5)
        self.label2 = Label(self.frame2, text='SELECTED FRAME', bg='black', fg='white').grid(row=0, column=2, padx=10, pady=5)

        self.button0 = Button(self.frame2, bg='black', fg='white', text='accept_1', command=self.print_plus).grid(row=1, column=0, padx=10, pady=5)
        self.button1 = Button(self.frame2, bg='black', fg='white', text='accept_2', command=self.print_minus).grid(row=1, column=1,padx=10, pady=5)
        self.button2 = Button(self.frame2, bg='black', fg='white', text='accept_3', command=self.fer1).grid(row=2, column=2, padx=10,pady=5)

        self.fer = IntVar()
        self.entry2 = Entry(self.frame2, textvariable=self.fer).grid(row=1, column=2, padx=20, pady=10)
        self.Select_bit()

        self.window.mainloop()

    def Select_bit(self):
        global t, ax, archivo
        # print(t)
        tipos = (("text files", "*.dat"), ("all files", "*.*"))
        archivo = fd.askopenfilename(title='Abrir archivo bat...',
                                     initialdir='C:/Users/johnf/Desktop',
                                     filetypes=tipos)
        df_1 = pd.read_table(archivo, sep='\t')
        self.plot()

    def plot(self):
        global t, line, df_bit, ax
        t=1
        df_bit = pd.read_csv(archivo, sep='\t') #read
        num = df_bit['Disp'][t]
        ruta = os.path.split(archivo)[0]
        read = '{ruta}/graf{num1}.txt'.format(ruta=ruta, num1=num)
        df = pd.read_table(read, sep='\t') #ruta
        df_1 = pd.DataFrame(columns=('Time(ns)', 'Iexperimental'))

        for i in range(len(df)):
            fer = np.fromstring(df.iloc[i][0], dtype=int, sep=' ')
            df_1 = df_1.append({'Time(ns)': fer[0], 'Iexperimental': fer[1]}, ignore_index=True)

        fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
        line, = plt.plot(df_1['Iexperimental'], lw=0.5, color='black')
        canvas = FigureCanvasTkAgg(fig, master=self.frame3)
        canvas.get_tk_widget().pack()

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.grid()

        scale = 1.2
        zp = Sc.ZoomPan()
        figZoom = zp.zoom_factory(fig, plt, ax, base_scale=scale)  # ZOOM WITH SCROLL
        figPan = zp.pan_factory(fig, plt, ax)  # MOVE WITH CLICK

    def print_plus(self):
        global t, ax
        t += 1
        num = df_bit['Disp'][t]
        ruta = os.path.split(archivo)[0]
        read = '{ruta}/graf{num1}.txt'.format(ruta=ruta, num1=num)
        df = pd.read_table(read, sep='\t')  # ruta
        df_1 = pd.DataFrame(columns=('Time(ns)', 'Iexperimental'))

        for i in range(len(df)):
            fer = np.fromstring(df.iloc[i][0], dtype=int, sep=' ')
            df_1 = df_1.append({'Time(ns)': fer[0], 'Iexperimental': fer[1]}, ignore_index=True)

        ax.set_ylim(bottom=df_1['Iexperimental'].min(), top=df_1['Iexperimental'].max())
        ax.set_xlim(left=df_1['Time(ns)'].min(), right=df_1['Time(ns)'].max())
        line.set_xdata(df_1['Time(ns)'])
        line.set_ydata(df_1['Iexperimental'])

        plt.draw()

    def print_minus(self):
        global t, ax
        t -= 1
        num = df_bit['Disp'][t]
        ruta = os.path.split(archivo)[0]
        read = '{ruta}/graf{num1}.txt'.format(ruta=ruta, num1=num)
        df = pd.read_table(read, sep='\t')  # ruta
        df_1 = pd.DataFrame(columns=('Time(ns)', 'Iexperimental'))

        for i in range(len(df)):
            fer = np.fromstring(df.iloc[i][0], dtype=int, sep=' ')
            df_1 = df_1.append({'Time(ns)': fer[0], 'Iexperimental': fer[1]}, ignore_index=True)

        ax.set_ylim(bottom=df_1['Iexperimental'].min(), top=df_1['Iexperimental'].max())
        ax.set_xlim(left=df_1['Time(ns)'].min(), right=df_1['Time(ns)'].max())
        line.set_xdata(df_1['Time(ns)'])
        line.set_ydata(df_1['Iexperimental'])

        plt.draw()

    def fer1(self):
        global t, ax
        print(self.fer.get())
        t = self.fer.get() - 1001
        num = df_bit['Disp'][t]
        ruta = os.path.split(archivo)[0]
        read = '{ruta}/graf{num1}.txt'.format(ruta=ruta, num1=num)
        df = pd.read_table(read, sep='\t')  # ruta
        df_1 = pd.DataFrame(columns=('Time(ns)', 'Iexperimental'))

        for i in range(len(df)):
            fer = np.fromstring(df.iloc[i][0], dtype=int, sep=' ')
            df_1 = df_1.append({'Time(ns)': fer[0], 'Iexperimental': fer[1]}, ignore_index=True)

        ax.set_ylim(bottom=df_1['Iexperimental'].min(), top=df_1['Iexperimental'].max())
        ax.set_xlim(left=df_1['Time(ns)'].min(), right=df_1['Time(ns)'].max())
        line.set_xdata(df_1['Time(ns)'])
        line.set_ydata(df_1['Iexperimental'])

        plt.draw()

MasterPanel()