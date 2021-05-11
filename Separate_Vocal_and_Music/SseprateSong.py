import numpy as np
import librosa 
from scipy.io.wavfile import write


class SeprateSong:

	def seprate(self,dir):
		self.y ,self.sr=librosa.load(dir,mono=False)
		y =librosa.core.to_mono(self.y)
		S , phase = librosa.magphase(librosa.stft(y))
		S_F =librosa.decompose.nn_filter(S,aggregate=np.median,metric='cosine',width=int(librosa.time_to_frames(2,sr=self.sr)))
		S_F = np.minimum(S,S_F)
		margin_music , margin_vocal=2,5
		power=2
		mask_music = librosa.util.softmask(S_F , margin_music*(S - S_F),power = power)
		mask_vocal = librosa.util.softmask(S - S_F , margin_vocal* S_F,power = power)
		S_v = mask_vocal *S
		S_m = mask_music*S
		S_v=S_v*np.exp(phase*1j)
		S_m=S_m*np.exp(phase*1j)
		S_v = np.array(librosa.istft( S_v))
		S_m = np.array(librosa.istft(S_m ))
		self.results=[S_v,S_m]
		return self.sr,self.y ,self.results

	def save_result(self,dir,index):
		write(f'{dir}.wav',self.sr,self.results[index])





