import matplotlib
matplotlib.use('QT5Agg')
import sys
from ui import Ui_MainWindow
import matplotlib.pylab as plt
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import pandas as pd
import numpy as np
import cv2
import datetime
from matplotlib.collections import PatchCollection
import reverse_geocoder 
from countries_code import  get_country,get_code
from operator import itemgetter
import time

class save_video(object):
    def __init__(self,self1,index,graph_index,save_btns,save_progress):
        self.self1=self1
        self.frame_no=0
        self.save_btns=save_btns
        self.save_progress=save_progress
        self.graph_index=graph_index
        self.save_btns.clicked.connect(self.save)
    def save(self):    
        self.frame_no =  self.frame_no - np.int(self.frame_no!=0)
        self.save_btns.setText("Saving Progressing")
        self.directory=self.get_video_directory()
        if self.directory==None:
            self.directory="kimo"
        frame = cv2.imread(f"imgs/img{self.graph_index}_0.jpeg")
        height, width, layers = frame.shape
        self.save_progress.show()
        self.video = cv2.VideoWriter(f"{self.directory}.avi", 0, 5, (width, height))
        self.index=0        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(20)
        self.timer.timeout.connect(lambda:self.save_video_iterate(width, height))
        self.timer.start()

    def save_video_iterate(self,width, height):
        if self.index<self.frame_no:               
            self.video.write(cv2.resize(cv2.imread(f"imgs/img{self.graph_index}_{self.index}.jpeg"),(width,height)))
            self.index += 1
            self.save_progress.setValue(int(np.round(100*self.index/self.frame_no)))
        else:
            self.save_btns.setText("Save Video")
            self.timer.stop()
            cv2.destroyAllWindows()  
            self.video.release() 
            self.save_progress.setValue(100)
            time.sleep(0.5)
            self.save_progress.hide()             
            
    def get_video_directory(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self.self1,"Choose Directory and Name", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            return fileName
    def update_frame_no(self,frame_no):
        self.frame_no=frame_no


class ApplicationWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.timer_li=[]
        self.get_data()
        self.initialize_map()
        self.initialize_graph_on_clicked() 
        self.initialize_bubble()  
        self.initialize_chart()      
        self.initialize_temperature()
        self.play_condition=[0,0,0]
        self.ui.tabWidget.currentChanged.connect(self.tab_change)
        self.ui.stop_li[0].clicked.connect(lambda:self.stop_start(0))
        self.ui.stop_li[1].clicked.connect(lambda:self.stop_start(1))
        self.ui.stop_li[2].clicked.connect(lambda:self.stop_start(2))
        self.ui.hide_country.clicked.connect(self.hide_on_click)
        self.ui.restart_2.clicked.connect(lambda:self.initialize_map(1))
        self.ui.restart_1.clicked.connect(lambda:self.initialize_bubble(1))
        self.ui.restart_3.clicked.connect(lambda:self.initialize_chart(1))
    def hide_on_click(self):
        self.ui.frame.hide()

    def tab_change(self):
        current_tab=self.ui.tabWidget.currentIndex()
        for i in range(np.size(self.timer_li)):
            if i != current_tab:
                self.timer_li[i].stop()
                self.ui.stop_li[i].setText('start')
                self.play_condition[i]=0


    def stop_start(self,index):
        if self.play_condition[index]==0:
            self.timer_li[index].start()
            self.play_condition[index]=1
            self.ui.stop_li[index].setText('Stop')
        else:
            self.timer_li[index].stop()
            self.play_condition[index]=0
            self.ui.stop_li[index].setText('start')

        
    def get_data(self):
        plt.ioff()
        data=[]
        data.append(pd.read_csv("dataset/time_series_covid19_confirmed_global.csv"))
        data.append(pd.read_csv('dataset/time_series_covid19_deaths_global.csv'))
        data.append(pd.read_csv('dataset/time_series_covid19_recovered_global.csv'))
        self.temperature_data=pd.read_csv("dataset/modified_weather_data.csv")
        self.countries_codes=list(get_country.keys())
        temp = data[0]
        self.countries_names=list(set(temp['Country/Region']))
        self.countries_no =np.size(self.countries_names)
        self.death_data={}
        self.confirmed_data={}
        self.recoverd_data={}
        self.confirmed_raw=[]
        temp_li=[self.confirmed_data,self.death_data,self.recoverd_data]

        for i in range(self.countries_no):
            for j in range(3):
                temp = data[j]
                temp2 = temp[temp['Country/Region']==self.countries_names[i]]
                temp2 = np.asarray(temp2)
                temp2 = np.sum(temp2[:,4::],axis=0)
                temp_li[j].update({self.countries_names[i]:temp2})
                if j==0:
                    self.confirmed_raw.append(temp2)
        self.confirmed_raw =np.asarray(self.confirmed_raw)
        self.dates=list(data[0].columns)
        self.dates=self.dates[4::]
        self.size=np.size(self.dates)                 

    def initialize_map(self,restart=0):
        if restart ==1:
            if self.index >0:
                self.timer.stop()
                self.pc.remove()
                self.cax.cla()
                self.index= 0
                self.fig.delaxes(self.cax)
                divider = make_axes_locatable(self.ax)
                self.cax=divider.append_axes('right',size='3%',pad=0) 
                self.timer.start()

        else:
            self.fig,self.ax = plt.subplots()
            self.divider = make_axes_locatable(self.ax)
            self.cax=self.divider.append_axes('right',size='3%',pad=0)
                   
            self.map = Basemap(projection='cyl', resolution='h',
                llcrnrlat=-90, urcrnrlat=90,
                llcrnrlon=-180, urcrnrlon=180, ax=self.ax)
            self.map.drawmapboundary(fill_color='aqua')
            self.map.fillcontinents(color='darkblue',lake_color='aqua')
            self.map.drawcoastlines()
            self.map.readshapefile('ne_10m_admin_0_countries/ne_10m_admin_0_countries', 'countries')
            plotWidget = FigureCanvas(self.fig)        
            cid = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
            self.index= 0
            self.ui.map_layout.addWidget(plotWidget)
            self.save_map_v = save_video(self,self.index,0,self.ui.save_li[0],self.ui.prpgress_li[0])
            self.timer = QtCore.QTimer()
            self.timer.setInterval(80)
            self.timer.timeout.connect(self.update_map)
            self.timer_li.append(self.timer)
            self.timer.start()  
    
    def update_map(self):
        if self.index < self.size:     
            self.save_map_v.update_frame_no(self.index)
            cmap=plt.cm.jet
            norm=plt.Normalize(0,np.max(self.confirmed_raw[:,self.index]))
            patches=[Polygon(shape , True, color=cmap(norm(int(self.confirmed_data[get_country[info['WB_A2']]][self.index]))))for info,shape in zip(self.map.countries_info,self.map.countries) if info['WB_A2'] in self.countries_codes if get_country[info['WB_A2']] in self.countries_names]

            if self.index!=0:
                self.pc.remove()
                self.cax.cla()
            else:
                self.timer.stop()

            self.pc = PatchCollection(patches, match_original=True, edgecolor='k', linewidths=1., zorder=2)
            self.ax.add_collection(self.pc)
            self.ax.set_title(f'cases in {self.dates[self.index]}')
            self.sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            self.sm.set_array(list(self.confirmed_raw[:,self.index]))
            self.fig.colorbar(self.sm,ax=self.ax,cax=self.cax,orientation='vertical')
            self.fig.canvas.draw_idle()
            self.fig.savefig(f"imgs/img{0}_{self.index}.jpeg")
            self.index +=1
        else:
            self.stop_start(0)
    
    def  initialize_graph_on_clicked(self):
        self.fig2,self.ax2 = plt.subplots(2,1)
        plotWidget = FigureCanvas(self.fig2)
        self.ui.on_click_layout.addWidget(plotWidget)
        
    def on_press(self,event):
        x_cordinate = event.xdata
        y_cordinate = event.ydata
        map_cordinates = self.map(y_cordinate,x_cordinate)
        country=reverse_geocoder.search(map_cordinates)
        country_code=country[0]
        country_code=country_code['cc']
        if country_code in self.countries_codes:
            country_name =get_country[country_code]
            if country_name in self.countries_names:
                self.draw_country(country_name)
       

    def draw_country(self,country_name):
        self.ax2[0].cla()
        self.ax2[1].cla()
        self.ui.frame.show()
        self.ax2[0].plot(np.arange(self.size),self.confirmed_data[country_name],'r',label='Confirmed cases')
        self.ax2[1].plot(np.arange(self.size),self.death_data[country_name],'b',label='Deathes')
        self.ax2[0].set(title=f'{country_name} cases ',ylabel='no of cases ', xlabel='Date start 22/1')
        self.ax2[1].set(title=f'{country_name} deaths',ylabel='no of  deathes', xlabel='Date start 22/1')
        self.ax2[0].tick_params(axis='x',which='minor',labelsize=5)
        self.ax2[1].tick_params(axis='x',which='minor',labelsize=5)
        self.fig2.tight_layout()
        self.fig2.canvas.draw_idle()


    def  initialize_bubble(self,restart=0):
        if restart==1:
            self.timer1.stop()
            self.ax1.cla()
            self.index1=0
            self.timer1.start()
        else:
            self.fig1,self.ax1 = plt.subplots()
            plotWidget = FigureCanvas(self.fig1)
            self.ui.buble_layout.addWidget(plotWidget)
            self.index1=0
            self.last_values=[[0]*self.countries_no]*3
            self.save_buble_v=save_video(self,self.index1,1,self.ui.save_li[1],self.ui.prpgress_li[1])
            self.timer1 = QtCore.QTimer()
            self.timer1.setInterval(15)
            self.timer1.timeout.connect(self.update_bubble)
            self.timer_li.append(self.timer1)
            self.timer1.start()

    def update_bubble(self):
        if self.index1<self.size:
            self.save_buble_v.update_frame_no(self.index1)
            day=self.dates[self.index1]
            start =int(self.index1!=0) 
            self.ax1.cla()
            x=[]
            y=[]
            size =[]
            for i in range(self.countries_no):
                temp=self.death_data[self.countries_names[i]]
                temp1=temp[self.index1] - temp[self.index1-start]
                x.append(np.log(np.abs(temp1 )+ 1))               

                temp=self.recoverd_data[self.countries_names[i]]
                temp1=temp[self.index1] - temp[self.index1-start]
                y.append(np.log(np.abs(temp1) + 1))

                temp=self.confirmed_data[self.countries_names[i]]
                temp1=temp[self.index1] - temp[self.index1-start]
                size.append(np.sqrt(temp1))
                self.ax1.annotate(get_code[self.countries_names[i]],(x[i],y[i]))

            if self.index1==0:
                self.timer1.stop()
            self.ax1.scatter(x, y, s=size)

            self.ax1.set(title=f'new death Vs recovery Vs new cases {self.dates[self.index1]}',ylabel='log(Recovery)',xlabel='log(Death)')
            self.fig1.savefig(f"imgs/img{1}_{self.index1}.jpeg")
            self.fig1.canvas.draw_idle()
            self.index1+=1
        else:
            self.stop_start(1)
    def initialize_chart(self,restart=0):
        if restart==1:
            self.timer2.stop()
            self.cax1.cla()
            self.ax3.cla()
            self.fig3.delaxes(self.cax3)
            divider = make_axes_locatable(self.ax3)
            self.cax3=divider.append_axes('right',size='3%',pad=0) 
            self.index3=0
            self.timer2.start()
        else:
            self.fig3,self.ax3 = plt.subplots()
            self.divider1 = make_axes_locatable(self.ax3)
            self.cax1=self.divider1.append_axes('right',size='3%',pad=0)
            plotWidget = FigureCanvas(self.fig3)
            self.ui.bar_layout.addWidget(plotWidget)
            self.index3=0
            self.save_bar_v=save_video(self,self.index3,2,self.ui.save_li[2],self.ui.prpgress_li[2])
            self.timer2 = QtCore.QTimer()
            self.timer2.setInterval(15)
            self.timer2.timeout.connect(self.update_chart)
            self.timer_li.append(self.timer2)
            self.timer2.start()  

    def update_chart(self):
        if self.index3<self.size:
            self.save_bar_v.update_frame_no(self.index3)
            countries=np.empty_like(self.countries_names)
            countries[:]=self.countries_names
            data=[]
            
            [ data.append([self.countries_names[i],self.confirmed_data[self.countries_names[i]][self.index3],self.death_data[self.countries_names[i]][self.index3]]) for i in range(self.countries_no)]
      
            data.sort(key=itemgetter(1),reverse=True)
            data=data[0:25]
            data=np.asarray(data)
            y_pos=np.arange(25)

            if self.index3!=0:
                self.cax1.cla()
                self.ax3.cla()
            else:
                self.timer2.stop()

            cmap=plt.cm.jet
            data1=np.asarray(data[:,0]).astype(np.str)
            data2=np.asarray(data[:,1]).astype(np.int)
            data3=np.asarray(data[:,2]).astype(np.int)
            norm=matplotlib.colors.Normalize(np.min(data3),np.max(data3))
            self.ax3.barh(y_pos,data2,color=cmap(norm(data3)))
            self.ax3.set_yticks(y_pos)
            self.ax3.set_yticklabels(data1)
            self.ax3.tick_params(axis='y',which='minor',labelsize=8)
            self.ax3.invert_yaxis()
            self.ax3.set(title=f'Case of highest 20 and death by color {self.dates[self.index3]}' , ylabel='Highes 20 countries',xlabel='no of cases')
            self.sm1 = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            self.sm1.set_array(data3)
            self.fig3.colorbar(self.sm1,ax=self.ax3,cax=self.cax1,orientation='vertical')

            self.fig3.savefig(f"imgs/img{2}_{self.index3}.jpeg")
            self.fig3.canvas.draw_idle()
            self.index3 +=1
        else:
            self.stop_start(2)
    def initialize_temperature(self):
        self.fig4,self.ax4 = plt.subplots(2,1)
        plotWidget = FigureCanvas(self.fig4)
        self.ui.T_layout.addWidget(plotWidget)
        Tempreature = np.asarray(self.temperature_data['T']).astype(np.float)
        Humidity = np.asarray(self.temperature_data['H']).astype(np.float)
        Cases = np.asarray(self.confirmed_data['Italy']).astype(np.int)

        t=[]
        h=[]
        c=[]
        for i in range(np.size(Tempreature)):
            start = int(i !=0)

            temp= np.abs(Cases[i]- Cases[i-start])
            c.append(temp)

        self.ax4[0].scatter(c,Tempreature,c='r',label='Tempreature')
        self.ax4[1].scatter(c,Humidity,c='b',label='Humidity')
        self.ax4[0].set(title=f'Italy cases VS Tempreature ',xlabel='cases',ylabel='Tempreature Celisuse')
        self.ax4[1].set(title=f'Italy cases VS Humidity ' ,xlabel='cases' ,ylabel='Relative Humidity')
        self.fig4.tight_layout()
        self.fig4.canvas.draw_idle()
              

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()        