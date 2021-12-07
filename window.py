from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename
import numpy as np
from copy import deepcopy
import cv2

from PIL import Image, ImageTk
from functions.aula06 import FFT, Canny, HighPass, LowPass
from skimage import data, img_as_ubyte, img_as_float
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from functions.aula11 import texture_segmentation
from functions.aula02 import Pixelate, Rotate, Blur
from functions.aula04 import NoiseClean, Noise, Sharpness
from functions.aula03 import exposure_function, plot_histogram
from functions.aula05 import Segmentation, automatic_segmentation, roberts, gx, gy
from utils import keep_float_range, select_image

from functions.steg import StegEncode, StegDecode

from utils import keep_float_range, select_image

IMAGE_WIDTH = 750
class GUI:
  def __init__ (self, master=None):
    self.master = master
    self.master.configure(background='white')

    self.frame = Frame(master, borderwidth=1, relief="solid")

    self.createMenu(self.master)

    self.hist = False
    self.array_draw = list() 
    self.snapshots = list()
    self.update_main_image(data.camera())
    
  def save_image(self):
    file = self.image.filename = asksaveasfilename(initialdir = "/",title = "Save as",defaultextension="*.jpg"
                                                   ,filetypes = (('JPEG', ('*.jpg','*.jpeg','*.jpe','*.jfif'))
                                                                 ,('PNG', '*.png'),('BMP', ('*.bmp','*.jdib'))))
    self.image.save(file)

  
  def apply_draw(self):
    img = deepcopy(np.array(self.resized))
    for i in self.array_draw:
      cv2.line(img, (i[0], i[1]),(i[2], i[3]),i[4])
    self.update_main_image(img)
    
  def discard_draw(self):
    self.array_draw.clear() 
    self.update_main_image(self.main_image_array)

  def clean(self, all):
    if all == True:
      self.snapshots = list()
      self.array_draw = list()
    for child in self.frame.winfo_children():
      child.destroy()
      
  def clean_hist(self):
    for child in self.frameG.winfo_children():
      child.destroy()
    
  def load_image(self):
    img = select_image()

    self.clean(True)
    self.update_main_image(img)
    
  def run_function (self, fn, params, image):
    new_image = fn["function"](img_as_float(image), params)
    return keep_float_range(new_image)

  def update_main_image (self, image):
    self.snapshots.append(image)
    self.show_main_image(image)

  def undo (self):
    if (len(self.snapshots) > 1):
      self.snapshots.pop()
      self.show_main_image(self.snapshots[len(self.snapshots) - 1])
      self.array_draw = list()

  def undo_all (self):
    if (len(self.snapshots)):
      old_image = self.snapshots[0]
      self.clean(True)
      self.update_main_image(old_image)


  def createSubWindow (self, width, height, name):
    sub_window = Toplevel(self.master, width=width, height=height)
    sub_window.title(name)
    sub_window.resizable(False, False)
    sub_window.attributes('-topmost', 'true')
    sub_window.grab_set()

    return sub_window

  def apply_paramless_function (self, fn):
    new_image = fn["function"](img_as_float(self.main_image_array))
    new_image = keep_float_range(new_image)
    self.update_main_image(new_image)

  def apply_slider_params_function (self, fn, start, end):
    slider_window = self.createSubWindow(250, 75, fn["name"])

    original_image = deepcopy(self.main_image_array)
    slider = Scale(slider_window, from_=start, to=end, orient=HORIZONTAL, command=lambda x:(
      self.show_main_image(self.run_function(fn, [int(x)], original_image))
    ))
    slider.place(relx=0.5, rely=0.25, relwidth=0.95, anchor=CENTER)

    Button(slider_window, text="Cancelar", command=lambda:(
      self.show_main_image(original_image),
      slider_window.destroy()
    )).place(relx=0.45, rely=0.6)

    Button(slider_window, text="OK", command=lambda:(
      self.update_main_image(self.run_function(fn, [int(slider.get())], original_image)),
      slider_window.destroy()
    )).place(relx=0.8, rely=0.6)

  def apply_text_box_params_function (self, fn):
    string_window = self.createSubWindow(350, 400, fn["name"])

    original_image = deepcopy(self.main_image_array)
    string = Text(string_window, height=17)
    string.place(relx=0.5, rely=0.4, relwidth=0.95, anchor=CENTER)

    Button(string_window, text="Cancelar", command=lambda:(
      self.show_main_image(original_image),
      string_window.destroy()
    )).place(relx=0.5, rely=0.9)

    Button(string_window, text="OK", command=lambda:(
      self.update_main_image(self.run_function(fn, [string.get("1.0", END)], original_image)),
      string_window.destroy()
    )).place(relx=0.8, rely=0.9)

  def get_text_function (self, fn):
    string_window = self.createSubWindow(350, 100, fn["name"])

    value = fn["function"](self.main_image_array)
    value = value if value else "Não há mensagem codificada!"

    string = Label(string_window, text=value)
    string.place(relx=0.5, rely=0.5, relwidth=0.8, anchor=CENTER)
    
  def get_pos_xy(self,event):
    global lastx, lasty
    lastx, lasty = event.x, event.y

  def draw(self,event, color, canvas):
    global lastx, lasty
    canvas.create_line((lastx, lasty, event.x, event.y), 
                fill=color[1], 
                width=1)
    self.array_draw.append((lastx, lasty, event.x, event.y, color[0]))
    lastx, lasty = event.x, event.y
    
  def select_color(self):
    colors = askcolor(title = "Cores")
    self.main_canvas.bind("<Button-1>", self.get_pos_xy)
    img = self.main_canvas.bind("<B1-Motion>",lambda event:self.draw(event, colors,self.main_canvas))
    
  def set_hist(self):
    if not self.hist:
      self.hist = True
      self.frameG = Frame(self.master, borderwidth=1, relief="flat" )
    else:
      self.hist = False
      self.frameG.destroy()
    self.update_main_image(self.main_image_array)
  
  def createMenu (self, app):
    menuBar = Menu(app)

    menuImage = Menu(menuBar, tearoff=0)
    menuImage.add_command(label="Abrir", command=self.load_image)
    menuImage.add_command(label="Salvar", command=self.save_image)
    menuImage.add_separator()
    menuImage.add_command(label="Fechar Arquivo", command=app.quit)
    menuBar.add_cascade(label="Arquivo", menu=menuImage)

    menuEditar = Menu(menuBar, tearoff=0)
    menuEditar.add_command(label="Desfazer", command=self.undo)
    menuEditar.add_command(label="Desfazer Tudo", command=self.undo_all)
    menuEditar.add_separator()

    menuEditar.add_command(label="Rotação", command=lambda: self.apply_slider_params_function(Rotate, 0, 360))

    menuDesfoque = Menu(menuImage, tearoff=0)
    menuDesfoque.add_command(label="Gaussiano", command=lambda: self.apply_slider_params_function(Blur, 0, 100))
    menuDesfoque.add_command(label="Pixel", command=lambda: self.apply_slider_params_function(Pixelate, 0, 100))
    menuEditar.add_cascade(label="Desfoque", menu=menuDesfoque)

    menuEditar.add_command(label="Nitidez", command=lambda: self.apply_slider_params_function(Sharpness, 0, 10))

    menuRuido = Menu(menuImage, tearoff=0)
    menuRuido.add_command(label="Adicionar", command=lambda: self.apply_slider_params_function(Noise, 0, 100))
    menuRuido.add_command(label="Remover", command=lambda: self.apply_slider_params_function(NoiseClean, 0, 100))
    menuEditar.add_cascade(label="Ruído", menu=menuRuido)

    menuBordas = Menu(menuImage, tearoff=0)
    menuBordas.add_command(label="Canny", command=lambda: self.apply_slider_params_function(Canny, 0, 10))
    menuBordas.add_command(label="FFT", command=lambda: self.apply_slider_params_function(FFT, 0, 100))
    menuBordas.add_command(label="Roberts",command=lambda: self.update_main_image(roberts(self.main_image_array)))
    menuBordas.add_command(label="Gx",command=lambda: self.update_main_image(gx(self.main_image_array)/255))
    menuBordas.add_command(label="Gy",command=lambda: self.update_main_image(gy(self.main_image_array)/255))
    menuEditar.add_cascade(label="Bordas", menu=menuBordas)
    
    menuEditar.add_command(label="Histograma",command= self.set_hist)
    menuEditar.add_command(label="Exposure",command=lambda: self.update_main_image(exposure_function(self.main_image_array)))
    menuDesenhar = Menu(menuImage, tearoff=0)
    menuDesenhar.add_command(label="Cores", command=self.select_color)
    menuDesenhar.add_command(label="Aplicar", command=self.apply_draw)
    menuDesenhar.add_command(label="Descartar", command=self.discard_draw)
    menuEditar.add_cascade(label="Desenhar", menu=menuDesenhar)

    menuPass = Menu(menuImage, tearoff=0)
    menuPass.add_command(label="Passa Alta", command=lambda: self.apply_paramless_function(HighPass))
    menuPass.add_command(label="Passa Baixa", command=lambda: self.apply_paramless_function(LowPass))
    menuEditar.add_cascade(label="Aplicar Filtro", menu=menuPass)
  
    menuSegm = Menu(menuImage, tearoff=0)
    menuSegm.add_command(label="Segmentação", command=lambda: self.apply_slider_params_function(Segmentation, 0 ,255))
    menuSegm.add_command(label="Limiar Global", command=lambda: self.update_main_image(automatic_segmentation(self.main_image_array, 0)))
    menuSegm.add_command(label="Limiar Local", command=lambda: self.update_main_image(automatic_segmentation(self.main_image_array, 1)))
    menuSegm.add_command(label="Segmentação Textura", command=lambda: self.update_main_image(texture_segmentation(self.main_image_array)))
    menuEditar.add_cascade(label="Segmentação", menu=menuSegm)
    
    menuBar.add_cascade(label="Editar", menu=menuEditar)
    
    menuSteg = Menu(menuImage, tearoff=0)
    menuSteg.add_command(label="Codificar Mensagem", command=lambda: self.apply_text_box_params_function(StegEncode))
    menuSteg.add_command(label="Decodificar Mensagem", command=lambda: self.get_text_function(StegDecode))
    menuBar.add_cascade(label="Esteganografia", menu=menuSteg)

    app.config(menu=menuBar)
    
  def show_main_hist(self):
    if self.hist == True:
      self.clean_hist()
      fig = Figure(figsize = (4, 3),
                dpi = 100)
    
      hr,hg,hb = plot_histogram(self.main_image_array)

      plot1 = fig.add_subplot(111)
      plot1.spines['top'].set_visible(False)
      plot1.spines['right'].set_visible(False)
      plot1.plot(hr, color = 'r')
      plot1.plot(hg, color = 'g')
      plot1.plot(hb, color = 'b')
      plot1.set_facecolor("None")
      
      self.frameG.config(height=3, width=3)
      self.frameG.grid(row=0,column=1,padx=10, pady=5)
      
      self.canvas = FigureCanvasTkAgg(fig,
                        master = self.frameG) 
    
      toolbar = NavigationToolbar2Tk(self.canvas,
                                    self.frameG)
      toolbar.update()
      
      self.canvas.get_tk_widget().pack(side='right',anchor='e',expand=True,fill='both')

  def show_main_image (self, array_img):
    
    self.main_image_array = img_as_ubyte(array_img)

    self.image = Image.fromarray(img_as_ubyte(array_img))
    width, height = (float(self.image.size[0]), float(self.image.size[1]))

    width_percet = float(IMAGE_WIDTH / width)
    height_size = int(height*width_percet)
  
    self.frame.config(height=height_size, width=IMAGE_WIDTH)
    self.frame.grid(row=0,column=0,padx=10, pady=5)
    
    self.resized = self.image.resize((IMAGE_WIDTH, height_size), Image.ANTIALIAS)
    self.master.parsed_image = ImageTk.PhotoImage(image=self.resized)

    self.main_canvas = Canvas(
      self.frame,
      width=IMAGE_WIDTH,
      height=height_size
    )

    self.main_canvas.place(relx=0.5, rely=0.5, anchor="center")

    self.main_canvas.create_image(
      IMAGE_WIDTH/2,
      height_size/2,
      anchor="center",
      image=self.master.parsed_image
    )
     
    self.show_main_hist()

class Window:
  def __init__ (self):
    self.gui = Tk(className="Processamento de Imagens")
    GUI(self.gui)

  def run (self):
    self.gui.mainloop()