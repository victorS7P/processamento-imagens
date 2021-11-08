from tkinter import *
from tkinter import filedialog as fd
from matplotlib import image

from PIL import Image, ImageTk
from skimage import data

IMAGE_WIDTH = 750

class GUI:
  def __init__ (self, master=None):
    self.master = master

    self.frame = Frame(master)
    self.frame.pack()

    self.show_main_image(data.rocket())
  
  #comandos a serem implementados
  def semComando(self):
    print("")

  def clean(self):
    for child in self.frame.winfo_children():
      child.destroy()

  def select_image(self):
    filetypes=[
            ('image files', ('.tiff', '.jpeg'))
        ]

    filename =  fd.askopenfile(
        title='Open a image',
        initialdir='/',
        filetypes=filetypes)
    
    img = image.imread(filename.name)
    self.clean()
    self.show_main_image(img)

  def menu (self, app):
    menuBar = Menu(app)
    menuImage=Menu(menuBar, tearoff=0)
    menuImage.add_command(label="Novo", command=self.select_image)
    menuImage.add_command(label="Salvar", command=self.semComando)
    menuImage.add_separator()
    menuImage.add_command(label="Fechar Arquivo", command=app.quit)
    menuBar.add_cascade(label="Arquivo", menu=menuImage)

    app.config(menu=menuBar)

  def show_main_image (self, array_img):
    self.menu(self.master)
    image = Image.fromarray(array_img)
    width, height = (float(image.size[0]), float(image.size[1]))

    width_percet = float(IMAGE_WIDTH / width)
    height_size = int(height*width_percet)

    resized = image.resize((IMAGE_WIDTH, height_size), Image.ANTIALIAS)
    self.master.parsed_image = ImageTk.PhotoImage(image=resized)

    self.main_image = Canvas(
      self.frame,
      width=IMAGE_WIDTH,
      height=height_size,
    )

    self.main_image.pack()
    self.main_image.create_image(
      IMAGE_WIDTH/2,
      height_size/2,
      anchor="center",
      image=self.master.parsed_image
    )
class Window:
  def __init__ (self):
    self.gui = Tk(className="Processamento de Imagens")
    self.gui.geometry("1024x768")
    GUI(self.gui)

  def run (self):
    self.gui.mainloop()
