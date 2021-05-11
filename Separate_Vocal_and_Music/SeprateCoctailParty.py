import numpy as np
from sklearn.decomposition import FastICA, PCA
from scipy.io.wavfile import write
import librosa

class SeprateCoctailParty:
	def seprate(self,dir):
		y ,self.sr= librosa.load(dir,mono=False)

		self.y = y.T
		source_1, source_2= self.y[:,0], self.y[:,1]	
		data = np.c_[source_1, source_2]
		data = data / 2.0 ** 15
		fast_ica= FastICA(n_components=2)
		separated = fast_ica.fit_transform(data)
		max_source, min_source = 1.0, -1.0
		max_result, min_result = np.max(separated.flatten()), np.min(separated.flatten())
		max_min= max_result - min_result
		separated = [ ((2.0 * (x - min_result))/max_min)   for x in separated.flatten() ]
		separated = np.array(separated)
		separated = separated - 1
		self.result= np.reshape( separated, (int(np.size(separated)/ 2), 2) )
		return self.sr,self.y.T,self.result

	def save_result(self,dir,index):
		write(f'{dir}.wav',self.sr,self.result[:,index])


		