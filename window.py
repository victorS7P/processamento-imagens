from tkinter import *
from tkinter import filedialog as fd
from matplotlib import image

from PIL import Image, ImageTk
from skimage import data, img_as_ubyte, img_as_float

from functions import Pixelate, Rotate, Blur
from copy import deepcopy

IMAGE_WIDTH = 750

class GUI:
  def __init__ (self, master=None):
    self.master = master

    self.frame = Frame(master)
    self.frame.config(height=768, width=1024)
    self.frame.pack()

    self.createMenu(self.master)

    self.snapshots = list()
    self.update_main_image(data.rocket())
  
  def save(self):
    #TODO: SALVAR ARQUIVO
    pass

  def clean(self):
    self.snapshots = list()
    for child in self.frame.winfo_children():
      child.destroy()

  def select_image(self):
    filetypes=[
      ('image files', ('.tiff', '.jpeg'))
    ]

    filename =  fd.askopenfile(
      title='Open a image',
      initialdir='/',
      filetypes=filetypes
    )
    
    img = image.imread(filename.name)

    self.clean()
    self.update_main_image(img)

  def run_function (self, fn, params, image):
    return img_as_ubyte(fn["function"](img_as_float(image), params))

  def update_main_image (self, image):
    self.snapshots.append(image)
    self.show_main_image(image)

  def undo (self):
    if (len(self.snapshots) > 1):
      self.snapshots.pop()
      self.show_main_image(self.snapshots[len(self.snapshots) - 1])

  def apply_slider_params_function (self, fn, start, end):
    slider_window = Toplevel(self.master, width=250, height=75)
    slider_window.title(fn["name"])
    slider_window.resizable(False, False)
    slider_window.attributes('-topmost', 'true')
    slider_window.grab_set()

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

  def createMenu (self, app):
    menuBar = Menu(app)

    menuImage = Menu(menuBar, tearoff=0)
    menuImage.add_command(label="Novo", command=self.select_image)
    menuImage.add_command(label="Salvar", command=self.save)
    menuImage.add_separator()
    menuImage.add_command(label="Fechar Arquivo", command=app.quit)
    menuBar.add_cascade(label="Arquivo", menu=menuImage)

    menuEditar = Menu(menuBar, tearoff=0)
    menuEditar.add_command(label="Desfazer", command=self.undo)
    menuEditar.add_command(label="Rotação", command=lambda: self.apply_slider_params_function(Rotate, 0, 360))

    menuDesfoque = Menu(menuImage, tearoff=0)
    menuDesfoque.add_command(label="Gaussiano", command=lambda: self.apply_slider_params_function(Blur, 0, 100))
    menuDesfoque.add_command(label="Pixel", command=lambda: self.apply_slider_params_function(Pixelate, 0, 100))

    menuEditar.add_cascade(label="Desfoque", menu=menuDesfoque)
    menuBar.add_cascade(label="Editar", menu=menuEditar)

    app.config(menu=menuBar)

  def show_main_image (self, array_img):
    self.main_image_array = array_img

    image = Image.fromarray(array_img)
    width, height = (float(image.size[0]), float(image.size[1]))

    width_percet = float(IMAGE_WIDTH / width)
    height_size = int(height*width_percet)

    resized = image.resize((IMAGE_WIDTH, height_size), Image.ANTIALIAS)
    self.master.parsed_image = ImageTk.PhotoImage(image=resized)

    self.main_canvas = Canvas(
      self.frame,
      width=IMAGE_WIDTH,
      height=height_size
    )

    self.main_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

    self.main_canvas.create_image(
      IMAGE_WIDTH/2,
      height_size/2,
      anchor="center",
      image=self.master.parsed_image
    )

class Window:
  def __init__ (self):
    self.gui = Tk(className="Processamento de Imagens")
    GUI(self.gui)

  def run (self):
    self.gui.mainloop()
