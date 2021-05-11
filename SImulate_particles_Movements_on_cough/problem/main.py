# -*- coding: utf-8 -*-

from PyQt5 import QtCore,QtWidgets
import sys
from ui import Ui_MainWindow
import cv2
import numpy as np
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pylab as plt
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
import time
class ApplicationWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 
        self.index=int(0)
        self.on =1
        self.k2= 42.1
        self.D= 0.05
        self.Uo = 8
        self.hieght=1.7
        self.add_mask=1
        self.t=[]
        self.Xp = []
        self.d_display =1
        self.image=[[]]*2
        self.ax=[]
        self.fig=[]
        self.cax=[]
        self.divider=[]
        self.plotWidget=[]
        self.is_mask=0
        self.planes = ["sagittal","coronal"]
        self.current_img = [np.zeros((251,251)),np.zeros((251,251))]
        self.img = [np.zeros((251,251)),np.zeros((251,251))] 
        self.initialize_plt()                                    
        self.ui.start_simulation.clicked.connect(self.start)
        self.ui.save_video.clicked.connect(self.save_video)
        self.ui.stop_simulation.clicked.connect(self.stop_restart)
        self.ui.distance_slider.valueChanged.connect(self.change_dist)
        self.ui.hide_plot.clicked.connect(self.ui.frame.hide)

    def change_dist(self):
        temp = self.ui.distance_slider.value()
        self.ui.source_distance.setText(f" {temp} m From Source")
    def initialize_plt(self):
        plt.ioff()
        for i in range(3):
            fig,ax = plt.subplots() 
            self.fig.append(fig)
            self.ax.append(ax)
            if i !=2:
                divider = make_axes_locatable(self.ax[i])
                self.divider.append(divider)
                cax=self.divider[i].append_axes('right',size='3%',pad=0)
                self.cax.append(cax)
                self.ax[i].set_title(f"{self.planes[i]} plane ")
                ax =self.ax[i].imshow(np.zeros((251,251)),cmap=plt.cm.jet,origin='lower') 
                self.fig[i].colorbar(ax,cax=self.cax[i],orientation='vertical')
                self.plotWidget.append(FigureCanvas(self.fig[i]))
                self.ui.display_layout.addWidget(self.plotWidget[i])
            else:
                self.plotWidget.append(FigureCanvas(self.fig[i]))
                self.ui.diplay_on_click_layout.addWidget(self.plotWidget[i])  
        cid = self.fig[0].canvas.mpl_connect('button_press_event', lambda event :self.on_press(event,0))
        cid2 = self.fig[1].canvas.mpl_connect('button_press_event', lambda event :self.on_press(event,1))
    
    def start(self):
        self.get_parameters()
        self.ui.stop_simulation.setText("Stop")
        self.ui.frame.hide()
        self.ui.hide_plot.hide()
        self.on =1
        if self.image[0]!=[]:
            self.timer.stop()
            self.image = [[]]*2
            self.img = [np.zeros((251,251)),np.zeros((251,251))] 
            self.index=0
            for i in range(2):
                self.ax[i].cla()
                self.cax[i].cla()
                self.fig[i].delaxes(self.cax[i])
                divider = make_axes_locatable(self.ax[i])
                self.divider.append(divider)
                cax=self.divider[i].append_axes('right',size='3%',pad=0) 
                self.cax[i]=cax      
                ax =self.ax[i].imshow(self.img[i],cmap=plt.cm.jet,origin='lower')   
                self.ax[i].set_title(f"{self.planes[i]} plane ")         
                self.fig[i].colorbar(ax,cax=self.cax[i],orientation='vertical')
                self.fig[i].canvas.draw_idle()
                                     
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.start_simulation)
        self.timer.start()        
    def stop_restart(self):
        
        if self.on ==1:
            self.timer.stop()
            self.on =0
            self.ui.stop_simulation.setText("Restart")
        else:
            self.timer.start()
            self.on =1
            self.ui.stop_simulation.setText("Stop")

    def get_parameters(self):
        self.d_display =   self.ui.distance_slider.value()   
        person_hieght = self.ui.person_hieght.text()  
        discharge_velocity= self.ui.discharge_velocity.text()         
        if discharge_velocity !='':
            self.Uo= float(discharge_velocity)
        if  person_hieght !='':
            self.hieght =float(person_hieght)
        temp = [3,5]
        if self.ui.add_mask.isChecked():
            self.is_mask =1
            self.add_mask =  temp[self.ui.select_mask.currentIndex()] 
        else:
            self.is_mask=0
            self.add_mask=1
            
    def start_simulation(self):                
        if self.index<251 :
            temp_d = ((self.index+1)/250)*self.d_display
            if temp_d <= 0.272:
                temp_t = temp_d/self.Uo      
                self.ui.time_display.setText(f"Time: {np.round(temp_t,5)} s")
                central_velocity = self.Uo *((1-self.is_mask*0.97)/(self.is_mask*self.index +1))
            else:
                temp_t = ((temp_d**2)+ 0.074 )/(0.544*self.Uo)        
                self.ui.time_display.setText(f"Time: {np.round(temp_t,5)} s")                
                central_velocity = (2.176/temp_d )*(1-self.is_mask)
            self.ui.distance_display.setText(f"Distance: {np.round(temp_d,4)} m")
            self.t.append(temp_t)
            limit_pixel=  int(np.round(125 - self.index * np.tan(self.add_mask*np.pi*15/180) - 2))
            
            self.img[0][125,self.index] = central_velocity
            self.img[1][125,125] = central_velocity
            if limit_pixel >250:
                limit_pixel =250
            for n in range(limit_pixel, 126):
                dist_vertical = ((125- n)/125)*self.hieght
                vertial_v = central_velocity*np.exp(-self.k2*0.2*(dist_vertical)**2)
                self.img[0][n,self.index] = vertial_v
                self.img[0][250-n,self.index] = vertial_v
                y = np.sqrt((125-limit_pixel)**2 - (125-n)**2)
                y = int(np.round(y))

                for m in range(125,125+y+1):
                    dist = np.sqrt((n-125)**2 + (m-125)**2)
                    dist_vertical = ((dist)/125)*self.hieght
                    vertial_v2 = central_velocity*np.exp(-self.k2*0.2*(dist_vertical)**2)
                    self.img[1][m,250-n] = vertial_v2
                    self.img[1][250-m,250-n] = vertial_v2 
                    self.img[1][m,n] = vertial_v2
                    self.img[1][250-m,n] = vertial_v2

            for i in range(2):
                self.ax[i].cla()
                self.ax[i].set_title(f"{self.planes[i]} plane at {np.round(temp_t,5)} s")                
                ax =self.ax[i].imshow(self.img[i],cmap=plt.cm.jet,origin='lower') 
                self.cax[i].cla()           
                self.fig[i].colorbar(ax,cax=self.cax[i],orientation='vertical')
                self.fig[i].savefig(f"imgs/img{i}_{self.index}.jpeg")
                self.fig[i].canvas.draw_idle()
                temp = np.empty_like (self.img[i])
                temp[:,:]= self.img[i]
                self.image[i].append(temp)
            self.index +=1 

        else:
            self.timer.stop()
        
        
      
    def on_press(self,point,index):
        if point.xdata != None and point.ydata!=None:
            self.ui.hide_plot.show()
            x_data = point.xdata
            y_data = point.ydata
            area =[0]
            if index==0:
                temp_d = ((x_data+1)/251)*self.d_display
                dist_center = (abs(y_data - 125)/125)*self.hieght 

                if temp_d <= 0.272:
                    t_start = temp_d/self.Uo
                    max_velocit = self.Uo*((1-self.is_mask*0.97)/(self.is_mask*self.index +1))
                else:
                    t_start = ((temp_d**2)+ 0.074 )/(0.544*self.Uo) 
                    max_velocit = (2.176/temp_d) *(1-self.is_mask)
                       
            else:
                temp_d = ((self.index+1)/251)*self.d_display
                if temp_d <= 0.272:
                    t_start = temp_d/self.Uo
                    max_velocit = self.Uo*((1-self.is_mask*0.97)/(self.is_mask*self.index +1))
                else:
                    t_start = ((temp_d**2) + 0.074 )/(0.544*self.Uo)  
                    max_velocit = (2.176/temp_d )*(1-self.is_mask)
                dist_center = (np.sqrt((y_data - 125)**2 + (x_data - 125)**2)/125)*self.hieght        
                x_data = self.index

            self.draw(max_velocit,dist_center,t_start,temp_d,x_data,y_data)
        
    def draw(self,max_velocity,dist_center,t_start,x_dist,xdata,ydata):
        self.ui.frame.show()
        self.ax[2].cla()
        t = np.linspace(0.0001,5.0001,50001)
        if np.abs(ydata-125 )> ( np.abs(xdata)*np.tan(np.pi/12) +4):
            f = np.zeros((np.size(t)))
        else:
            index_of_t_start= int(np.round(t_start / 0.0001))
            f= max_velocity*np.exp(-10*t/((0.272 + ((self.d_display**2)-0.073984)/0.544))/self.Uo)*np.exp(-self.k2*(dist_center)**2)
            f[0:index_of_t_start] = np.repeat(0,index_of_t_start)
        self.ax[2].plot(t,f)
        self.ax[2].set(title = "V at poin Versus Time",xlabel = "time (s)",  ylabel = "V (m/s)")
        self.fig[2].canvas.draw()

    def save_video(self):
        self.frame_no =  int(self.index )-1
        self.ui.save_video.setText("Saving Progressing")
        self.directory=self.get_video_directory()
        if self.directory==None:
            self.directory="kimo"
        frame = cv2.imread("imgs/img0_0.jpeg")
        height, width, layers = frame.shape
        width = int(np.round(width*0.7))*2
        self.ui.videoprogress.show()
        self.video = cv2.VideoWriter(f"{self.directory}.avi", 0, 5, (width, height))
        self.index_2=0        
        self.timer1 = QtCore.QTimer()
        self.timer1.setInterval(50)
        self.timer1.timeout.connect(lambda:self.save_video_iterate(width, height))
        self.timer1.start()         
    def save_video_iterate(self,width, height):
        width =int(0.5*width)
        if self.index_2<=self.frame_no:               
            self.video.write(np.concatenate((cv2.resize(cv2.imread(f"imgs/img{0}_{self.index_2}.jpeg"),(width,height)),cv2.resize(cv2.imread(f"imgs/img{1}_{self.index_2}.jpeg"),(width,height))),axis=1)) 
            self.index_2 += 1
            self.ui.videoprogress.setValue(int(np.round(100*self.index_2/self.frame_no)))
        else:
            self.ui.save_video.setText("Save Video")
            self.timer1.stop()
            cv2.destroyAllWindows()  
            self.video.release() 
            self.ui.videoprogress.setValue(100)
            time.sleep(0.5)
            self.ui.videoprogress.hide()             
            
    def get_video_directory(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Choose Directory and Name", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            return fileName                
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()        