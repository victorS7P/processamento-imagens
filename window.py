from tkinter import *

from PIL import Image, ImageTk
from skimage import data

IMAGE_WIDTH = 750

class GUI:
  def __init__ (self, master=None):
    self.master = master

    self.frame = Frame(master)
    self.frame.pack()

    self.show_main_image(data.rocket())

  def show_main_image (self, array_img):
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
