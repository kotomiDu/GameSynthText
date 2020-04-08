from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mainWindow import Ui_MainWindow
from pathlib import Path
import sys

from gen import *
import global_util


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setupUi(self)

        
        self.initial_setting()

        self.pushButton_path.pressed.connect(self.imagedata_open)
        self.pushButton_font.pressed.connect(self.choosefont)
        self.pushButton_addfont.pressed.connect(self.addfont)
        self.pushButton_data.pressed.connect(self.generatedata)
        self.pushBotton_clearfont.pressed.connect(self.clear_font)
        self.pushButton_colordialog.pressed.connect(self.openColorDialog)
        self.pushButton_textsource.pressed.connect(self.openTextSource)
        self.pushButton_detectlabel.pressed.connect(self.generate_detection_data)
        self.pushButton_recoglabel.pressed.connect(self.generate_recog_data)

        self.comboBox_font.currentIndexChanged.connect(self.fontopen) 

        self.show()

        self.parameters = {}
        self.fontlist = []
    def initial_setting(self):
        '''bg preparation'''
        img = cv2.imread("data/source/bg.png")
        h = self.label_sample.height()
        w = self.label_sample.width()
        resize_img = cv2.resize(img,(w,h))
        showImage = QImage(resize_img.data, resize_img.shape[1], resize_img.shape[0],resize_img.shape[1]*3, QImage.Format_RGB888).rgbSwapped()
        pix =QPixmap.fromImage(showImage) 
        self.label_sample.setPixmap(pix)

        '''font style'''
        img = cv2.imread("data/source/bg1.png")
        h = self.label_font.height()
        w = self.label_font.width()
        resize_img = cv2.resize(img,(w,h))
        showImage = QImage(resize_img.data, resize_img.shape[1], resize_img.shape[0],resize_img.shape[1]*3, QImage.Format_RGB888).rgbSwapped()
        pix =QPixmap.fromImage(showImage) 
        self.label_font.setPixmap(pix)
        self.fontlist_temppath = "data/fonts/fontlist.txt"
        self.initial_font()


        '''propety setting'''
        self.textEdit_fontcolor.setText("default")
        self.textEdit_fontsize.setText("default")
        self.textsource = None
        self.textsource_temppath = "data/textsource_temp.txt"

    def initial_font(self):
        import glob
        import os
        self.comboBox_font.addItem("---please select---")
        fontlist = []
        for ext in ("*.ttf","*.ttc","*.otf"):
            fontlist.extend(glob.glob(os.path.join("data/fonts/",ext)))
        for font in fontlist:
            fontname = Path(font).name
            self.comboBox_font.addItem(fontname) 

    def imagedata_open(self):
        # open screenshot file location
        ofdir= QFileDialog.getExistingDirectory(self, 'Open data path')
        if ofdir is '':
            return
        path = Path(ofdir)
        if path.exists() == False or path.is_dir() == False:
            return 
        self.lineEdit_samplepath.setText(ofdir)
        import glob
        imglist = glob.glob(ofdir + '/*[jpg,png,bmp]')
        '''show data info'''
        data_number = len(imglist)
        QMessageBox.about(self, "Notice", "{} {} will be used for generating data".format(str(data_number), 'image' if data_number == 1 else 'images'))
    
            
    def fontopen(self):
        import cv2
        fontname = self.comboBox_font.currentText()

        if fontname == "---please select---":
            return
        fontimage = "data/fonts/"+Path(fontname).stem+".png"
        img = cv2.imread(fontimage)
        h = self.label_sample.height()
        w = self.label_sample.width()
        resize_img = cv2.resize(img,(w,h))
        showImage =QImage(resize_img.data, resize_img.shape[1], resize_img.shape[0],resize_img.shape[1]*3, QImage.Format_RGB888).rgbSwapped()
        pix = QPixmap.fromImage(showImage)    
        self.label_font.setPixmap(pix)

    def choosefont(self):
        fontname = self.comboBox_font.currentText()
        if fontname == "---please select---":
            return
        self.fontlist.append(fontname)
        self.textEdit_fontlist.insertPlainText(fontname+"\n")

    def addfont(self):
        font,_= QFileDialog.getOpenFileName(self, 'Open font','','*.ttf *.ttc *.otf')
        if font is '':
            return
        fontname,_ = os.path.splitext(os.path.basename(font))
        self.lineEdit_addfont.setText(font)
        self.textEdit_fontlist.insertPlainText(fontname+"\n")
        self.label_font.setText("cannot show the outside font style ")
        self.fontlist.append(font)
        
  

    def clear_font(self):
        self.fontlist = []
        self.textEdit_fontlist.setText("")


    def openColorDialog(self):
        '''
        show format #417dff
        pass format [R,G,B]
        '''
        color = QColorDialog.getColor()

        if color.isValid():
            self.font_color_value  = np.array(color.getRgb()[:3])
            self.textEdit_fontcolor.setText(color.name())

    def openTextSource(self):
        textsource,_= QFileDialog.getOpenFileName(self, 'Open text source','','*.txt')
        if textsource is "":
            return 
        self.textsource = str(textsource)
        print(type(self.textsource))
        self.textEdit_textcontent.setText("please check the detail in {}".format(textsource))

    def bgpreparation_ready(self):
        self.ofdir = self.lineEdit_samplepath.text()
        if self.ofdir == "":
            QMessageBox.about(self,"Warning","Please import image data")
            return False
        path = Path(self.ofdir)
        if path.exists() == False or path.is_dir() == False:
            QMessageBox.about(self,"Warning","Please import correct path")
            return False
        #create relative dir
        self.rootpath = path.parent
        self.txtdir =  self.rootpath/'text'
        self.outimgdir = self.rootpath/'img_gen'
        self.outtxtdir = self.rootpath/'label_gen'

        if self.outimgdir.exists() == False:
            self.outimgdir.mkdir()
        if self.outtxtdir.exists() == False:
            self.outtxtdir.mkdir()
        #print(txtdir,outtxtdir,outimgdir)
        return True

    def fontstyle_ready(self):
        fontlist = self.textEdit_fontlist.toPlainText()
        if fontlist == "":
            QMessageBox.about(self,"Warning","Please choose font style")
            return False
        
        fontfile = open(self.fontlist_temppath,'w',encoding = "utf-8")
        
        for font in self.fontlist:
            fontfile.write(font+"\n")
        fontfile.close()

        #create font model
        import update_font_model 
        update_font_model.start()

        return True

    def fontproperty_ready(self):
        font_size = self.textEdit_fontsize.toPlainText()
        font_color = self.textEdit_fontcolor.toPlainText()
        reuse_number_per_image = self.textEdit_reusenumber.toPlainText()
        text_number_per_image = self.textEdit_textnumber.toPlainText()
        text_content = self.textEdit_textcontent.toPlainText()

        if font_size == '' or font_color == ''  or reuse_number_per_image == ''  or text_number_per_image == '' or text_content == '':
            msgBox = QMessageBox.about(self, "Warning", "please set font property(size, color, etc)")
            return False
        if font_size not in "default":
            if not font_size.isdigit():
                msgBox = QMessageBox.about(self, "Warning", "please set font size with number")
                return False
        if not reuse_number_per_image.isdigit():
            msgBox = QMessageBox.about(self, "Warning", "please set reuse_number with interger, e.g. 1,2")
            return False
        if not text_number_per_image.isdigit():
            msgBox = QMessageBox.about(self, "Warning", "please set text_number with interger, e.g. 1,2")
            return False

        if font_size in "default":
            self.font_size = -1
        else:
            self.font_size = eval(font_size)

        if font_color in "default":
            self.font_color_value = None
        
        self.reuse_number_per_image = eval(reuse_number_per_image)
        self.text_number_per_image = eval(text_number_per_image)

        if self.textsource is None:
            textfile = open("data/textsource_temp.txt","w",encoding="utf-8")   
            text_content_list = text_content.split(",")
            print(text_content_list,text_content)
            for text in text_content_list:
                textfile.write(text+"\n")
            textfile.close()
            self.textsource = self.textsource_temppath
        
        import update_char_freq
        update_char_freq.start(self.textsource)
        return True

    def generatedata(self):

        if not self.bgpreparation_ready():
            return
        
        if not self.fontstyle_ready():
            return

        if not self.fontproperty_ready():
            return


        self.parameters["dir"]=[self.ofdir, self.txtdir, self.outimgdir, self.outtxtdir]
        self.parameters["fontstyle"]=[self.font_size,self.font_color_value]
        self.parameters["text"]=[self.reuse_number_per_image,  self.text_number_per_image, self.textsource]

        global_util.logfile = open(os.path.join(self.rootpath, "generation.log"),'w')
        generate_flag = start_generate(self.parameters)
        if generate_flag == 1:
            QMessageBox.about(self, "Notice", "Finish generation, go to {} to check!".format(self.rootpath))
            #release memory
            self.textsource = None
            if os.path.exists(self.textsource_temppath):
                os.remove(self.textsource_temppath)
            if os.path.exists(self.fontlist_temppath):
                os.remove(self.fontlist_temppath)
        global_util.logfile.close()

    def generate_detection_data(self):
        if not self.bgpreparation_ready():
            return 
        import gen_detect_data
        gen_detect_data.start(self.rootpath)
        QMessageBox.about(self, "Notice", "Finish generation, go to {} to check!".format(os.path.join(self.rootpath,"detection_label")))
    
    def generate_recog_data(self):
        if not self.bgpreparation_ready():
            return 
        import gen_recog_data
        gen_recog_data.start(self.rootpath)
        QMessageBox.about(self, "Notice", "Finish generation, go to {} to check!".format(os.path.join(self.rootpath,"recognition_data")))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Data Generator")

    window = MainWindow()
    window.setWindowIcon(QIcon('./data/source/title.png'))
    window.setWindowTitle("SynthText")
    app.exec_()