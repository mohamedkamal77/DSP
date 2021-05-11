import matplotlib
matplotlib.use('QT5Agg')
import sys
from ui import Ui_MainWindow
import matplotlib.pylab as plt
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from SseprateSong import  SeprateSong
from SeprateCoctailParty import  SeprateCoctailParty

class ApplicationWindow(QtWidgets.QMainWindow):
    
	def __init__(self):
		super(ApplicationWindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		seprate_song = SeprateSong()
		seprate_cocktail = SeprateCoctailParty()
		self.seprator = [seprate_song,seprate_cocktail]
		self.initialize_plots()
		self.ui.AddSongBtn.clicked.connect(lambda:self.AddAudio(0)) 
		self.ui.AddCocktailBtn.clicked.connect(lambda:self.AddAudio(1))
		self.ui.Saveusic.clicked.connect(lambda:self.SaveResult(0,1))
		self.ui.SaveVocal.clicked.connect(lambda:self.SaveResult(0,0))
		self.ui.SaveS_1.clicked.connect(lambda:self.SaveResult(1,0))
		self.ui.SaveS_2.clicked.connect(lambda:self.SaveResult(1,1))

	def AddAudio(self,index):
		dir =self.ChoseAudio()
		if dir != 'no':
			self.sr,self.input,self.result=self.seprator[index].seprate(dir)
			self.plot(index)

	def plot(self,index):
		
		if index ==0:
			self.ui.frame.show()
			size = np.size(self.result[0])
		else:
			self.ui.frame2.show()
			size = np.size(self.result[:,0])
		t = np.arange(0,size/self.sr,1/self.sr)
		#print(self.input.shape)
		m_v = ['Music','Vocal']
		for i in range(2):
			self.ax[index][0,i].cla()
			self.ax[index][0,i].plot(t,self.input[i,0:size])
			self.ax[index][0,i].set(title=f'Input Micrphone {i +1}',xlabel='time s',ylabel='amplitude')
			self.ax[index][1,i].cla()
			if index ==1:
				self.ax[index][1,i].plot(t,self.result[:,i])
				self.ax[index][1,i].set(title=f'Source {i +1}',xlabel='time s',ylabel='amplitude')	
			else:
				self.ax[index][1,i].plot(t,self.result[i])

				self.ax[index][1,i].set(title=f'{m_v[i]} ',xlabel='time s',ylabel='amplitude')	

			
		self.fig[index].tight_layout()
		self.fig[index].canvas.draw_idle()	

	def SaveResult(self,TabIndex,SourceIndex):
		dir=self.ChoseNameDir()
		self.seprator[TabIndex].save_result(dir,SourceIndex)


	def initialize_plots(self):
		fig ,ax = plt.subplots(2,2)
		plotwidget = FigureCanvas(fig)   
		self.ui.PlotResultLayout.addWidget(plotwidget)

		fig_1 ,ax_1 = plt.subplots(2,2)
		plotwidget = FigureCanvas(fig_1)   
		self.ui.PlotResultLayout_2.addWidget(plotwidget)
		self.fig=[fig,fig_1]
		self.ax =[ax,ax_1]


	def ChoseAudio(self):
		"""IMPORT IMAGE AUDIO LOCAL"""
		options = QtWidgets.QFileDialog.Options()
		options |= QtWidgets.QFileDialog.DontUseNativeDialog
		fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			return fileName

		else:
			self.ui.msg.setWindowTitle("No file chosen ")
			self.ui.msg.setText("please, choose audio file ")
			return  'no' 

	def ChoseNameDir(self):
		options = QtWidgets.QFileDialog.Options()
		options |= QtWidgets.QFileDialog.DontUseNativeDialog
		fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"Choose Directory and Name", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			return fileName
		else:
			return 'Team4'

def main():
	app = QtWidgets.QApplication(sys.argv)
	application = ApplicationWindow()
	application.show()
	app.exec_()


if __name__ == "__main__":
	main()