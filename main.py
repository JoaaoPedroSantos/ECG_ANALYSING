from mod import *
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog as dlg
#import time


class ECG(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self._frame = None
        self.switch_frame(Home)

    def switch_frame(self, frame_class):
        # Destroys current frame and replaces it with a new one
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def Load(self):
        global path
        path = dlg.askopenfilename()

    def plot_grafico(self, grafico):
        self.window = Toplevel(app)

        # Background da nova janela
        self.plotImage = PhotoImage(file="art/Resultados_ML.png")
        self.w = self.plotImage.width()
        self.h = self.plotImage.height()
        self.plotLabel = Label(self.window, image=self.plotImage)
        self.plotLabel.pack()

        # Dimensões
        self.window.resizable(width=0, height=0)  # Para tamanho da janela não alterar
        self.window.geometry('%dx%d+0+0' % (self.w, self.h))

        # Label do gráfico
        self.my_label = Label(self.window, image=grafico, bg="white")
        self.my_label.place(x=50, y=100)

    def plot_result(self,img_path):

        Gra = Image.open(img_path)
        resized = Gra.resize((400, 300), Image.ANTIALIAS)
        my_img = ImageTk.PhotoImage(resized)
        self.plot_grafico(my_img)

    def trainML(self, train_button1):
        #global Svm
        if Frame.svm.get() == 1:
           img_ad = SVM(path)
           self.plot_result(img_ad)


    #def testML(self, test_button1):


    #def trainDL(self, train_button2):


    #def testDL(self, test_button2):

class Home(Frame):
    def __init__(self, master):
        global w, h
        Frame.__init__(self, master)
        w = Home.winfo_screenwidth(self)
        h = Home.winfo_screenheight(self)


        # Background
        Frame.b_home = Image.open("art/Iniciar.png")
        Frame.resized1 = Frame.b_home.resize((w, h), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.b_home = ImageTk.PhotoImage(Frame.resized1)

        Label(self, image=Frame.b_home).pack()

        # Botões
        Frame.info = Image.open("art/Info_button.png")
        Frame.resized2 = Frame.info.resize((240, 63), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.info = ImageTk.PhotoImage(Frame.resized2)
        Button(self, text="Info", image=Frame.info, borderwidth=0, bg="#235291", relief=FLAT,
               command=lambda: master.switch_frame(Info)).place(x=(w - 240) / 2, y=h * 370 / 1080)

        Frame.iniciar = Image.open("art/Iniciar_button.png")
        Frame.resized3 = Frame.iniciar.resize((240, 63), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.iniciar = ImageTk.PhotoImage(Frame.resized3)
        Button(self, text="Iniciar", image=Frame.iniciar, borderwidth=0, bg="#264E8E", relief=FLAT,
               command=lambda: master.switch_frame(Iniciar)).place(x=(w - 240) / 2, y=h * 580 / 1080)


class Info(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # Background
        Frame.b_info = Image.open("art/Info.png")
        Frame.resized4 = Frame.b_info.resize((w, h), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.b_info = ImageTk.PhotoImage(Frame.resized4)

        Label(self, image=Frame.b_info).pack()

        # Botão
        Frame.back = Image.open("art/back_button.png")
        Frame.resized5 = Frame.back.resize((124, 36), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.back = ImageTk.PhotoImage(Frame.resized5)
        Button(self, text="Voltar", image=Frame.back, borderwidth=0, bg="#235291", relief=FLAT,
               command=lambda: master.switch_frame(Home)).place(x=w * 1615 / 1920, y=h * 960 / 1080)


class Iniciar(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # Background
        Frame.b_tecnica = Image.open("art/tecnica.png")
        Frame.resized6 = Frame.b_tecnica.resize((w, h), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.b_tecnica = ImageTk.PhotoImage(Frame.resized6)

        Label(self, image=Frame.b_tecnica).pack()

        # Botões
        Frame.ml = Image.open("art/button1.png")
        Frame.resized7 = Frame.ml.resize((277, 95), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.ml = ImageTk.PhotoImage(Frame.resized7)
        Button(self, text="ML", image=Frame.ml, borderwidth=0, bg="#F8F8F8", relief=FLAT,
               command=lambda: master.switch_frame(ML)).place(x=(w - 277) / 2, y=h * 350 / 1080)

        Frame.dl = Image.open("art/button2.png")
        Frame.resized8 = Frame.dl.resize((277, 95), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.dl = ImageTk.PhotoImage(Frame.resized8)
        Button(self, text="DL", image=Frame.dl, borderwidth=0, bg="#F8F8F8", relief=FLAT,
               command=lambda: master.switch_frame(DL)).place(x=(w - 277) / 2, y=h * 600 / 1080)

        Frame.back = Image.open("art/back_button.png")
        Frame.resized9 = Frame.back.resize((124, 36), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.back = ImageTk.PhotoImage(Frame.resized9)
        Button(self, text="Voltar", image=Frame.back, borderwidth=0, bg="#235291", relief=FLAT,
               command=lambda: master.switch_frame(Home)).place(x=w * 1615 / 1920, y=h * 960 / 1080)


class ML(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # Background
        Frame.b_ML = Image.open("art/ML.png")
        Frame.resized10 = Frame.b_ML.resize((w, h), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.b_ML = ImageTk.PhotoImage(Frame.resized10)

        Label(self, image=Frame.b_ML).pack()

        # Botões
        Frame.load = Image.open("art/Load_button.png")
        Frame.resized11 = Frame.load.resize((750, 90), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.load = ImageTk.PhotoImage(Frame.resized11)
        Button(self, text="load", image=Frame.load, borderwidth=0, bg="#F8F8F8", relief=FLAT,
               command=lambda: master.Load()).place(x=(w - 750) / 2, y=h * 90 / 1080)
        # Button.config(self, image = Frame.load)

        Frame.train1 = Image.open("art/Train_button.png")
        Frame.resized12 = Frame.train1.resize((126, 51), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.train1 = ImageTk.PhotoImage(Frame.resized12)
        Frame.train_button1 = Button(self, text="Treinar", image=Frame.train1, borderwidth=0, bg="#F8F8F8", relief=FLAT,
                                     command=lambda: master.trainML(Frame.train_button1)).place(x=w * 690 / 1920,
                                                                                                y=h * 795 / 1080)

        Frame.test1 = Image.open("art/Test_button.png")
        Frame.resized13 = Frame.test1.resize((126, 51), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.test1 = ImageTk.PhotoImage(Frame.resized13)
        Frame.test_button1 = Button(self, text="Testar", image=Frame.test1, borderwidth=0, bg="#F8F8F8", relief=FLAT,
                                    command=lambda: master.switch_frame(Resultados_ML)).place(x=w * 980 / 1920,
                                                                                              y=h * 795 / 1080)
        # master.testML(Frame.test_button1)

        Button(self, text="Voltar", image=Frame.back, borderwidth=0, bg="#235291", relief=FLAT,
               command=lambda: master.switch_frame(Iniciar)).place(x=w * 1615 / 1920, y=h * 960 / 1080)

        # CheckButtons
        Frame.svm = IntVar()
        Frame.DT = IntVar()
        Frame.DF = IntVar()
        Frame.NB = IntVar()
        Frame.VFI = IntVar()
        Frame.KNN = IntVar()
        Checkbutton(self, variable=Frame.svm, onvalue=1, offvalue=0,
                    borderwidth=0, bg="#F8F8F8").place(x=w * 390 / 1920, y=h * 455 / 1080)
        Checkbutton(self, variable=Frame.DT, onvalue=1, offvalue=0,
                    borderwidth=0, bg="#F8F8F8").place(x=w * 390 / 1920, y=h * 560 / 1080)
        Checkbutton(self, variable=Frame.DF, onvalue=1, offvalue=0,
                    borderwidth=0, bg="#F8F8F8").place(x=w * 390 / 1920, y=h * 670 / 1080)
        Checkbutton(self, variable=Frame.NB, onvalue=1, offvalue=0,
                    borderwidth=0, bg="#F8F8F8").place(x=w * 1080 / 1920, y=h * 455 / 1080)
        Checkbutton(self, variable=Frame.VFI, onvalue=1, offvalue=0,
                    borderwidth=0, bg="#F8F8F8").place(x=w * 1080 / 1920, y=h * 560 / 1080)
        Checkbutton(self, variable=Frame.KNN, onvalue=1, offvalue=0,
                    borderwidth=0, bg="#F8F8F8").place(x=w * 1080 / 1920, y=h * 670 / 1080)

class DL(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # Background
        Frame.b_DL = Image.open("art/DL.png")
        Frame.resized14 = Frame.b_DL.resize((w, h), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.b_DL = ImageTk.PhotoImage(Frame.resized14)

        Label(self, image=Frame.b_DL).pack()

        # Botões
        Frame.load2 = Image.open("art/Load_button_2.png")
        Frame.resized15 = Frame.load2.resize((750, 90), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.load2 = ImageTk.PhotoImage(Frame.resized15)
        Button(self, text="load", image=Frame.load2, borderwidth=0, bg="#F8F8F8", relief=FLAT,
               command=lambda: master.Load()).place(x=(w - 750) / 2, y=h * 90 / 1080)
        # Button.config(self, image = Frame.load2)

        Frame.train2 = Image.open("art/Train_button.png")
        Frame.resized16 = Frame.train2.resize((126, 51), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.train2 = ImageTk.PhotoImage(Frame.resized16)
        Frame.train_button2 = Button(self, text="Treinar", image=Frame.train2, borderwidth=0, bg="#F8F8F8", relief=FLAT,
                                     command=lambda: master.trainDL(Frame.train_button2)).place(x=w * 690 / 1920,
                                                                                                y=h * 795 / 1080)

        Frame.test2 = Image.open("art/Test_button.png")
        Frame.resized17 = Frame.test2.resize((126, 51), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.test2 = ImageTk.PhotoImage(Frame.resized17)
        Frame.test_button2 = Button(self, text="Testar", image=Frame.test2, borderwidth=0, bg="#F8F8F8", relief=FLAT,
                                    command=lambda: master.switch_frame(Resultados_DL)).place(x=w * 980 / 1920,
                                                                                              y=h * 795 / 1080)
        # master.testDL(Frame.test_button2)

        Button(self, text="Voltar", image=Frame.back, borderwidth=0, bg="#235291", relief=FLAT,
               command=lambda: master.switch_frame(Iniciar)).place(x=w * 1615 / 1920, y=h * 960 / 1080)

        # CheckButtons
        Frame.CNN1 = IntVar()
        Frame.CNN2 = IntVar()
        Frame.CNN3 = IntVar()

        Checkbutton(self, variable=Frame.CNN1, onvalue=1, offvalue=0,
                    borderwidth=0, bg="#F8F8F8").place(x=w * 390 / 1920, y=h * 490 / 1080)
        Checkbutton(self, variable=Frame.CNN2, onvalue=1, offvalue=0,
                    borderwidth=0, bg="#F8F8F8").place(x=w * 390 / 1920, y=h * 600 / 1080)
        Checkbutton(self, variable=Frame.KNN, onvalue=1, offvalue=0,
                    borderwidth=0, bg="#F8F8F8").place(x=w * 1080 / 1920, y=h * 490 / 1080)


class Resultados_ML(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # Background
        Frame.b_RML = Image.open("art/Resultados_ML.png")
        Frame.resized18 = Frame.b_RML.resize((w, h), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.b_RML = ImageTk.PhotoImage(Frame.resized18)

        Label(self, image=Frame.b_RML).pack()

        # Botão
        Frame.close = Image.open("art/close_button.png")
        Frame.resized19 = Frame.close.resize((124, 36), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.close = ImageTk.PhotoImage(Frame.resized19)
        Button(self, text="Fechar", image=Frame.close, borderwidth=0, bg="#EFF2F7", relief=FLAT,
               command=lambda: master.switch_frame(ML)).place(x=w * 1615 / 1920, y=h * 960 / 1080)


class Resultados_DL(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        # Background
        Frame.b_RDL = Image.open("art/Resultados_DL.png")
        Frame.resized20 = Frame.b_RDL.resize((w, h), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.b_RDL = ImageTk.PhotoImage(Frame.resized20)

        Label(self, image=Frame.b_RDL).pack()

        # Botão
        Frame.close = Image.open("art/close_button.png")
        Frame.resized21 = Frame.close.resize((124, 36), Image.ANTIALIAS)  # Tamanho da imagem
        Frame.close = ImageTk.PhotoImage(Frame.resized21)
        Button(self, text="Fechar", image=Frame.close, borderwidth=0, bg="#EFF2F7", relief=FLAT,
               command=lambda: master.switch_frame(DL)).place(x=w * 1615 / 1920, y=h * 960 / 1080)


#    class PageOne(Frame):
#        def __init__(self, master):
#            Frame.__init__(self, master)
#            Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
#            Button(self, text="Return to start page",
#                      command=lambda: master.switch_frame(StartPage)).pack()


if __name__ == "__main__":
    app = ECG()
    app.title("Análise de ECG")

    app.geometry('%dx%d+0+0' % (w, h))
    app.resizable(width=0, height=0)  # Para tamanho da janela não alterar

    app.mainloop()

