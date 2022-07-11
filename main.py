import image_slicer
import cv2
import os

import tkinter as tk
from tkinter import filedialog

from kivy.app import App
from kivy.base import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
Builder.load_string("""
<rootwi>:
    cols: 3
    Label:
        text: "Выберите ролик: "
        id: name1
    Label:
        text: "Путь до ролика"
        id: label1
    FileButton:
        text: "Обзор"
        on_press: label1.text =  self.get_path()
    Label:
        text: "Выберите маски: "
        id: name2
    Label:
        text: "Путь до ролика"
        id: label2
    FolderButton:
        text: "Обзор"
        on_press: label2.text =  self.get_path()
    Label:
        text: "Папка результата: "
        id: name2
    Label:
        text: "Путь для результата"
        id: label3
    FolderButton:
        text: "Обзор"
        on_press: label3.text =  self.get_path()
    StartButton:
        text: "Старт"
        on_press: self.cutTheCrap(label1.text, label2.text, label3.text)
""")


class StartButton(Button):
  @staticmethod
  def cutTheCrap(vname, masks, parts):
    vidcap = cv2.VideoCapture(vname)
    success, image = vidcap.read()
    count = 0
    while success:
      cv2.imwrite(parts+ '/' + "frame%d.jpg" % count, image)
      frame = parts + '/' + "frame%d.jpg" % count
      success, image = vidcap.read()
      print('Framing: %d ' % count, success)
      image_slicer.slice(frame, 2)
      count += 1
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(masks) if isfile(join(masks, f))]
    for file in onlyfiles:
        print('Framing:' + file)
        image_slicer.slice(masks + '/' + file, 2)
    print('Framing')
    command = "python test.py --model e2fgvi --video %s --mask %s --ckpt release_model/E2FGVI-CVPR22.pth" % (parts,masks)
    os.system(command)

class FileButton(Button):
    @staticmethod
    def get_path():
        root = tk.Tk()
        root.withdraw()

        return( filedialog.askopenfilename() )


class FolderButton(Button):
  @staticmethod
  def get_path():
    root = tk.Tk()
    root.withdraw()

    return (filedialog.askdirectory())

class rootwi(GridLayout):
    pass


class MyApp(App):
    def build(self):
        return rootwi()


if __name__ == '__main__':
    MyApp().run()