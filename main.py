#Фоторедактор Easy Editor

#Connect (присоединяем списки и словари)
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PIL import Image, ImageFilter
import os

#Save (хранение картинки)
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'

    def load_image(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(self.dir,self.filename)
        self.image = Image.open(image_path)

    def show_image(self, path):
        Kartinka_Image.hide()
        pixmap_image = QPixmap(path)
        w, h = Kartinka_Image.width(), Kartinka_Image.height()
        pixmap_image = pixmap_image.scaled(w, h, Qt.KeepAspectRatio)
        Kartinka_Image.setPixmap(pixmap_image)
        Kartinka_Image.show()

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)

    def saveImage(self):
        path = os.path.join(workdir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(
            workdir,self.save_dir, self.filename
        )
        self.show_image(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(
            workdir,self.save_dir, self.filename
        )
        self.show_image(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(
            workdir,self.save_dir, self.filename
        )
        self.show_image(image_path)

    def do_blur(self):
        self.image = self.image.filter(ImageFilter.GaussianBlur(1))
        self.saveImage()
        image_path = os.path.join(
            workdir,self.save_dir, self.filename
        )
        self.show_image(image_path)

    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(
            workdir,self.save_dir, self.filename
        )
        self.show_image(image_path)

#Window (открываем окно)
app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy Editor')

#Widgets (кнопки и всякое такое)
Knopka_Papka = QPushButton('папка')
Knopka_Left = QPushButton('лево')
Knopka_Right = QPushButton('право')
Knopka_Mirror = QPushButton('зеркало')
Knopka_Blur = QPushButton('размытие')
Knopka_BlackAndWhite = QPushButton('Ч/Б')
Knopka_Sharpness = QPushButton('резкость')
Kartinka_Image = QLabel('картинка')
Spisok_List = QListWidget()

#Layouts (где находятся кнопки)
layout_1 = QVBoxLayout()
layout_1.addWidget(Knopka_Papka)
layout_1.addWidget(Spisok_List)

layout_2 = QHBoxLayout()
layout_2.addWidget(Knopka_Left)
layout_2.addWidget(Knopka_Right)
layout_2.addWidget(Knopka_Mirror)
layout_2.addWidget(Knopka_Blur)
layout_2.addWidget(Knopka_Sharpness)
layout_2.addWidget(Knopka_BlackAndWhite)

layout_3 = QVBoxLayout()
layout_3.addWidget(Kartinka_Image)
layout_3.addLayout(layout_2)

layout_4 = QHBoxLayout()
layout_4.addLayout(layout_1, stretch = 1)
layout_4.addLayout(layout_3, stretch = 4)
main_win.setLayout(layout_4)

workdir = ''

#Image (список картинок)
def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

#Global (переменные)
def chooseworkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg', '.jpg', '.png', '.gif', '.bmp']
    chooseworkdir()
    filenames = filter(os.listdir(workdir), extensions)
    Spisok_List.clear()
    for filename in filenames:
        Spisok_List.addItem(filename)

work_image = ImageProcessor()

def showShosenImage():
    if Spisok_List.currentRow() >= 0:
        filename = Spisok_List.currentItem().text()
        work_image.load_image(workdir, filename)
        image_path = os.path.join(work_image.dir, work_image.filename)
        work_image.show_image(image_path)

#List (папки)
Spisok_List.currentRowChanged.connect(showShosenImage)
Knopka_Papka.clicked.connect(showFilenamesList)

Knopka_BlackAndWhite.clicked.connect(work_image.do_bw)

Knopka_Mirror.clicked.connect(work_image.do_flip)

Knopka_Left.clicked.connect(work_image.do_left)

Knopka_Right.clicked.connect(work_image.do_right)

Knopka_Blur.clicked.connect(work_image.do_blur)

Knopka_Sharpness.clicked.connect(work_image.do_sharp)

#Launch поехали!
main_win.showMaximized()
app.exec()