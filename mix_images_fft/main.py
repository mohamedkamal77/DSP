from ui import Ui_MainWindow
import logging 
#import log_info
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap 
import tkinter 
from tkinter import filedialog
from PIL import Image
import numpy as np
import sip
global image_no 
image_no = 0 #DETERMINR NUMBER OF IMAGE
global output_no
output_no=0 #DETERMINR NUMBER OF OUTPUT
global selected_comp #DETERMINR IF WE SELECTED FROM COMBOBOX OF COMPONENT
selected_comp = [0]*4
global selected_img #DETERMINR IF WE SELECTED FROM COMBOBOX OF IMAGES
selected_img = [0]*4
global comp_to_show #COMPONENT OF OUTPUT
comp_to_show=[[0]]*4
global main_comp #MAIN COMPONENT WHIH DETERMINE THE MODE  i.e if we selected amplitude we should prevent real and imaginary component 
main_comp =100
global comp_tybe #COMP TYPE I.E real and imaginary OR  mag and phase AND WHICH FIRST I.E IMAG FIRST OR REAL
comp_tybe = 0
global im_shape #STORE IMAGE SHAPE
im_shape=(0,0,0)
global im_size #image size one dim array
im_size=1
global which_clicked # STORE  THE ELEMENT SELECTED
which_clicked =0
global component_avaliable  # to determine which component to show  i.e if we selected amplitude we should prevent real and imaginary component 
component_avaliable = [[[1,5],[2,6]] ,[[2,6],[1,5]],[[3],[4]],[[4],[3]],[[1,5],[2,6]] ,[[2,6],[1,5]]]
global comp_av_comb
comp_av_comb = [[1,2,3],[0,2,3],[3,0,1],[2,0,1]] 
global zeros_arr
 
logging.basicConfig(filename='log_info.log',level = logging.INFO,
                    format ='%(asctime)s:%(levelname)s:%(message)s')
class cr_image:
    """this class create viewr (label contain image's name ,label contain image ,label contain image 
        component,combobox to choose component """
    def __init__(self,scrollAreaWidgetContents,verticalLayout,comp_combo_l,img_combo_l,delete_ch,open_img):
        global image_no
        image_no = image_no +1
        self.image_n = image_no
        logging.info(f'open image {self.image_n }')
        print('k')
        self.photo_files = ["assets/result/input/amp.png","assets/result/input/ph.png","assets/result/input/real.png","assets/result/input/imag.png"]
        self.scrollAreaWidgetContents = scrollAreaWidgetContents
        self.verticalLayout =verticalLayout
        self.comp_combo_l =comp_combo_l
        self.img_combo_l =img_combo_l
        self.delete_ch =delete_ch
        self.open_img = open_img
        self.comp_l=[]
        
        self.image_dir = self.import_image()
        self.image_data(self.image_dir)
        self.orig_photo = QPixmap(self.image_dir)
        self.comp_photo = QPixmap(self.photo_files[0])        
        self.imgs = QtWidgets.QVBoxLayout()
        self.imgs.setObjectName("img")
        self.image_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.image_name =f"IMAGE {self.image_n}"
        self.image_label.setText(self.image_name)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.image_label.setFont(font)
        self.image_label.setObjectName("image_label")
        self.imgs.addWidget(self.image_label)
        
        self.image = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.image.setPixmap(self.orig_photo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(sizePolicy)
        self.image.setMinimumSize(QtCore.QSize(250, 250))
        self.image.setObjectName("image")
        self.image.setScaledContents(True)                
        self.imgs.addWidget(self.image)        
        self.comp_view_select = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.comp_view_select.setObjectName("comp_view_select")
        self.imgs.addWidget(self.comp_view_select)        
        self.image_comp = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.image_comp.setPixmap(self.comp_photo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_comp.sizePolicy().hasHeightForWidth())
        self.image_comp.setSizePolicy(sizePolicy)
        self.image_comp.setMinimumSize(QtCore.QSize(250, 250))
        self.image_comp.setObjectName("image_comp")
        self.image_comp.setScaledContents(True)        
        self.imgs.addWidget(self.image_comp)
        self.imgs.setStretch(0, 1)
        self.imgs.setStretch(1, 5)
        self.imgs.setStretch(2, 1)
        self.imgs.setStretch(3, 5)
        self.verticalLayout.addLayout(self.imgs)        
        self.comp_view_select.addItem("amplitude")
        self.comp_view_select.addItem("phase")
        self.comp_view_select.addItem("real")
        self.comp_view_select.addItem("imaginary")
        
        for i in self.img_combo_l:
            i.addItem(f'Img_{self.image_n}')
        self.img_combo_l[0].currentIndexChanged.connect(lambda: self.select_img(0) )
        self.img_combo_l[1].currentIndexChanged.connect(lambda: self.select_img(1))
        self.img_combo_l[2].currentIndexChanged.connect(lambda: self.select_img(2))
        self.img_combo_l[3].currentIndexChanged.connect(lambda: self.select_img(3))                
        self.comp_view_select.currentIndexChanged.connect(self.change_comp)
        self.comp_combo_l[0].currentIndexChanged.connect(lambda:self.select_comp(0))
        self.comp_combo_l[1].currentIndexChanged.connect(lambda:self.select_comp(1))
        self.comp_combo_l[2].currentIndexChanged.connect(lambda:self.select_comp(2))
        self.comp_combo_l[3].currentIndexChanged.connect(lambda:self.select_comp(3))
        self.image.mouseReleaseEvent= lambda event: self.image_clicked(event)
        self.image_comp.mouseReleaseEvent= lambda event: self.image_clicked(event)
        self.delete_ch.clicked.connect(self.delete)
        self.open_img.clicked.connect(self.over_wite_img)
    def image_clicked(self,d):
        """determine which channel we clicked"""
        logging.info(f'click image{self.image_n}')
        global which_clicked 
        which_clicked = self.image
    
    def select_img(self,ind): 
        """selecting the image from combobox"""
        logging.info(f'select image{self.image_n} for component{ind}') 
        temp_ind = str(self.img_combo_l[ind].currentText())
        global selected_img
        global main_comp 
        global comp_to_show
        
        if temp_ind[-1] == str(self.image_n):   
            selected_img[ind] = 1
            if main_comp == 100:
                
                for i in range(6):
                    self.comp_combo_l[ind].view().setRowHidden( (i + 1)  ,False)                        
            else:
                print(comp_to_show[ind]) 
                if comp_to_show[ind][0]!=0:                
                    for i in comp_to_show[ind] :
                        print(i)
                        self.comp_combo_l[ind].view().setRowHidden( i ,False)                                           
        
        self.select_comp(ind)        
                     
    def select_comp(self,ind):
        """selecting component to mix by combobox"""
        global selected_comp
        global comp_to_show
        global main_comp
        global comp_tybe 
        global im_shape 

        if main_comp == 100 :
            main_comp = ind
                        
        temp_ind = self.comp_combo_l[ind].currentIndex()
        temp_text = self.comp_combo_l[ind].currentText()
        logging.info(f'chose {temp_text} for component{ind}')
        temp_im_ind = str(self.img_combo_l[ind].currentText())
        if temp_im_ind[-1] == str(self.image_n):
            if selected_img[ind]==1:
                if temp_ind!=0:   #if none is not chosen 
                    
                    if main_comp != ind:
                        selected_comp[ind] = self.comp_l[temp_ind - 1] #save the array of comp chosen in global var to use later                                                                   
                        
                    #if this combo is the main combonet by which we decide we work (im & real or ampl&phase)                                   
                    else:
                        if temp_ind in [1,5,2,6]: #to determine the kind of combonent (im & real or ampl&phase)
                            if ind <= 1:
                                comp_tybe = 1
                            else:    
                                comp_tybe = 3
                        else :
                            if ind <=1:
                                comp_tybe = 2
                            else:    
                                comp_tybe = 4
                        for i in range(4):
                            selected_comp[i]= zeros_arr
                        selected_comp[ind] = self.comp_l[temp_ind - 1]
                        for i in self.comp_combo_l :
                            #frist we hide all the componet of combobox t
                            for indx in range(6): 
                                i.view().setRowHidden( (indx + 1) ,True)
                            
                        #second we show again all component for the main combobox        
                        for indx in range(6):      
                            self.comp_combo_l[ind].view().setRowHidden( (indx + 1) ,False)        
                        #determine wich combo will represent (im / real or ampl / phase)    
                        self.temp1=component_avaliable[temp_ind - 1][0] 
                        self.temp2=component_avaliable[temp_ind - 1][1]
                        #show the component in ewvery combbox                        
                        comp_to_show[ind] =np.arange(1,8,1)                        
                        for i in range(3):
                            temp_indx = comp_av_comb[ind][i]
                            if i == 0:
                                comp_to_show[temp_indx] = self.temp1
                                self.hide_show_row(self.temp1,self.comp_combo_l[temp_indx],False) 
                            else:
                                comp_to_show[temp_indx] = self.temp2
                                self.hide_show_row(self.temp2,self.comp_combo_l[temp_indx],False)
                else:
                    #temp = np.repeat(0,im_size )    
                    selected_comp[ind] = zeros_arr
                    #np.reshape(temp,im_shape)
                                        
                                           
    def hide_show_row(self,affected_indces ,element,show ):
        """HIDE ROW IN COMBOBOX"""
        for i in affected_indces :                        
            element.view().setRowHidden( i ,show)                                       
        
    def change_comp(self):
        """CHANGE THE COMP DISPLAYED IN VIEW """
        ind = self.comp_view_select.currentIndex()
        temp_text = self.comp_view_select.currentText()
        logging.info(f'chose {temp_text} for component view')
        self.photo = QPixmap(self.photo_files[ind])
        self.image_comp.setPixmap(self.photo)
        
    def over_wite_img(self):
        """SHOW NEW IMAGE IN PLACE OF CURRENT ONE"""
        global which_clicked        
        if which_clicked== self.image:
            self.image_dir = self.import_image()
            logging.info(f'open {self.image_dir} instead of current image ')
            self.image_data(self.image_dir)
            self.orig_photo = QPixmap(self.image_dir)
            self.comp_photo = QPixmap(self.photo_files[0])            
            self.image.setPixmap(self.orig_photo)
            self.image_comp.setPixmap(self.comp_photo)

                     
    def import_image(self):
        """IMPORT IMAGE FROM LOCAL"""
        main_win = tkinter.Tk() 
        main_win.withdraw()
        main_win.overrideredirect(True)
        main_win.geometry('0x0+0+0')
        main_win.deiconify()
        main_win.lift()
        main_win.focus_force()       
        main_win.sourceFile = filedialog.askopenfilename(parent=main_win, initialdir= "/",
        title='Please select a directory') 
        main_win.destroy()
        logging.info(f'import image {main_win.sourceFile} ')
        return  main_win.sourceFile
                
    def image_data(self,dirctory):
        """GET THE DATA OF IMAGE I.E AMPL,PHASE,IMAGINARY....."""
        logging.info(f' get all data about image{self.image_n}')
        im = (Image.open(dirctory).convert('LA'))
        global im_size        
        global im_shape
        global zeros_arr
        temp_shape = np.array(im).shape
        #determine if it is the first image or not tp determine the generalize shape
        if im_size == 1:
            im_shape =temp_shape
            logging.info(f'shape of this ssesio  is {im_shape}')
            self.im_dim = np.size(im_shape)
            for i in range(self.im_dim):
                im_size  = im_size  *im_shape[i]
        else:
            #if new image's size is different from general resize it
            if temp_shape != im_shape:
                logging.info(f'change shape of image{self.image_n} to  {im_shape}')
                temp_size = im_shape[0:2]
                im = im.resize(temp_size[::-1])      
        self.im_array = np.array(im) #convert to array 
        #get fourrier transform and store the component of image in variable inside each image     
        self.im_array_f = np.fft.rfft2(self.im_array)
        self.im_amplitude = np.abs(self.im_array_f) 
        self.comp_l.append(self.im_amplitude)
        Image.fromarray(np.uint8(20*np.log( np.fft.fftshift( self.im_amplitude)))).save(self.photo_files[0])
        self.im_phase = (np.angle(self.im_array_f))
        self.comp_l.append(self.im_phase)
        Image.fromarray(np.uint8(self.im_phase)).save(self.photo_files[1])
        self.im_real = (np.real(self.im_array_f))
        self.comp_l.append(self.im_real)
        Image.fromarray(np.uint8(self.im_real)).save(self.photo_files[2])
        self.im_imag = (np.imag(self.im_array_f))
        self.comp_l.append(self.im_imag)
        Image.fromarray(np.uint8(self.im_imag)) .save(self.photo_files[3]) 
        
        #generate uniform ampl and phase                            
        self.im_uni_amp = np.repeat(1,im_size)
        self.im_uni_amp =np.reshape(self.im_uni_amp ,im_shape)
        self.comp_l.append(self.im_uni_amp)
        self.im_uni_ph =  np.repeat(0,im_size)
        self.im_uni_ph =np.reshape(self.im_uni_ph ,im_shape)
        zeros_arr = self.im_uni_ph
        self.comp_l.append(self.im_uni_ph)

        
    def delete(self):
        """delete selected image"""        
        if which_clicked == self.image:#determine if this image is selected
            logging.info(f'delete image{self.image_n}')
            self.imgs.removeWidget(self.image_label)
            self.image_label.deleteLater()
            self.image_label = None
            self.imgs.removeWidget(self.image)
            self.image.deleteLater()
            self.image = None
            self.imgs.removeWidget(self.comp_view_select)
            self.comp_view_select.deleteLater()
            self.comp_view_select = None
            self.imgs.removeWidget(self.image_comp)
            self.image_comp.deleteLater()
            self.image_comp = None            
            self.verticalLayout.removeItem(self.imgs)
            sip.delete(self.imgs)
            self.imgs = None
                    
########################################################################################            
class cr_output:
    def __init__(self,scrollAreaWidgetContents,output_display,comp_combo_l,output_select,ratio_l,img_combo_l,save_img,delete_ch):
        """this class generate output (label contain output no and the output pic)"""
        global output_no
        output_no = output_no + 1
        logging.info(f'create output{output_no}')
        self.comp_combo_l =comp_combo_l
        self.img_combo_l=img_combo_l
        self.output_no = output_no
        self.ratio_l =ratio_l
        self.save_img = save_img
        self.delete_ch = delete_ch
        self.scrollAreaWidgetContents=scrollAreaWidgetContents
        self.output_display =output_display
        self.output_select =output_select
        self.current_img =[]
        self.output1_view = QtWidgets.QVBoxLayout()
        self.output1_view.setObjectName("output1_view")
        self.output1_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.output1_label.setFont(font)
        self.output1_label.setObjectName("output1_label")
        self.output1_label.setText(f"Output_{self.output_no}")
        self.output1_view.addWidget(self.output1_label)
        self.output = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.output.setScaledContents(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output.sizePolicy().hasHeightForWidth())
        self.output.setSizePolicy(sizePolicy)
        self.output.setMinimumSize(QtCore.QSize(250, 250))
        self.output.setObjectName("output")
        self.output1_view.addWidget(self.output)
        self.output_display.addLayout(self.output1_view)
        self.output_select.addItem(f"Output_{self.output_no}")
        self.output_select.currentIndexChanged.connect(self.change_output)
        for i in self.comp_combo_l:
            i.currentIndexChanged.connect(self.change_output)
        for i in self.ratio_l:
            i.valueChanged.connect(self.change_output)
        for i in self.img_combo_l:
            i.currentIndexChanged.connect(self.change_output)
    
        self.save_img.clicked.connect(self.save)
        self.delete_ch.clicked.connect(self.delete)
        self.output.mouseReleaseEvent= lambda event: self.output_clicked(event)
    def output_clicked(self,d):
        """determine if this output is selected"""
        global which_clicked
        
        which_clicked = self.output
            
    def change_output(self):
        """change the output every time any comp changes"""
        temp_text = str(self.output_select.currentText())
        if self.output_select.currentIndex()!=0:
            logging.info(f'change output{output_no}')             
            if int(temp_text[-1])==self.output_no:
                self.apply_output()  
                

    def apply_output(self):
        """combine the component and show the output"""
        global comp_tybe
        global selected_comp
        global im_shape

        if comp_tybe!=0 :
            logging.info(f'apply output{output_no}')
            w=[0,0]
            temp = [0,0]  
            for i in range(2):
                #get the value of slider(weight)  
                w[i] = self.ratio_l[i].value()/100 
                print(w[i])
                temp[i] = np.add((w[i]*selected_comp[i*2]) , ((1- w[i])*(selected_comp[i*2 +1])))                
            if comp_tybe==1: #detrmine if mag&PHASE MAG BEFORE PHASE
                self.output_arr = temp[0] *np.exp(temp[1]*1j )
            elif comp_tybe==3: #detrmine if mag&PHASE MAG BEFORE PHASE
                self.output_arr = temp[1] *np.exp(temp[0]*1j ) 
            elif comp_tybe==2: #detrmine mode real&imag real before imag
                self.output_arr = np.add(temp[0] , 1j*temp[1])
            elif comp_tybe==4: #detrmine mode real&imag real after image 
                self.output_arr = np.add(temp[1] , 1j*temp[0])
            
            self.current_img = np.fft.irfft2(self.output_arr)
            
            self.current_img  = np.uint8(self.current_img    )  
            Image.fromarray(self.current_img).save(f'assets/result/output/output{self.output_no}.png')
            self.photo = QPixmap(f'assets/result/output/output{self.output_no}.png')
            self.output.setPixmap(self.photo)
    
    def save(self):
        """choose directory to save current image"""
        global which_clicked
        if which_clicked ==self.output:
            main_win = tkinter.Tk() 
            main_win.withdraw()
            main_win.overrideredirect(True)
            main_win.geometry('0x0+0+0')
            main_win.deiconify()
            main_win.lift()
            main_win.focus_force()
            main_win.sourceFile = filedialog.asksaveasfilename(parent=main_win, initialdir= "/",
                                                             title='Please select a directory')
            main_win.destroy()
            size=np.size(main_win.sourceFile)
            if size !=0:
                directory = f"{main_win.sourceFile}.png"
                Image.fromarray(self.current_img).save(f'{directory}')
                logging.info(f'save output{output_no} at {directory}')
            else:
                #if no name give pop up warnning
                self.ui.msg.setWindowTitle("no name")
                self.ui.msg.setText("choose name to your file  ")
                self.ui.msg.exec_()
 
    def delete(self):
        """delete output if selected"""
        global which_clicked
        if which_clicked == self.output:
            logging.info(f'delete output{output_no} ')
            self.output1_view.removeWidget(self.output1_label)
            self.output1_label.deleteLater()
            self.output1_label = None
            self.output1_view.removeWidget(self.output)
            self.output.deleteLater()
            self.output = None
            
            self.output_display.removeItem(self.output1_view)
            sip.delete(self.output1_view)
            self.output1_view = None
               
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.images =[]
        self.outputs =[]
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.new_ch.clicked.connect(self.add_img)
        self.ui.new_ch_2.clicked.connect(self.add_output)

    def add_img(self):
        """add image and it's cpmponent there is NO number limit"""
        logging.info(f'add new image channel')
        a = cr_image(self.ui.scrollAreaWidgetContents_2,self.ui.verticalLayout_2,self.ui.comp_combo_l,self.ui.img_combo_l,self.ui.delete_ch,self.ui.open_img)
        self.images.append(a)
    def add_output(self):
        """add output there is NO number limit"""
        logging.info(f'add new output channel')
        a = cr_output(self.ui.scrollAreaWidgetContents,self.ui.output_display,self.ui.comp_combo_l,self.ui.output_select,self.ui.ratio_l,self.ui.img_combo_l,self.ui.save_img,self.ui.delete_ch_2)
        self.outputs.append(a)
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()