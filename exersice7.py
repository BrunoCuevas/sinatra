#!/home/charizard/anaconda3/bin/ipython3
import numpy as np;
import matplotlib.pyplot as plt;
import sinatraAudio as sA;
import sinatraFrontEnd as sFE;
import sys;
from scipy.io.wavfile import read;
#
#
#
freq, audio = read(sys.argv[1]);
audio = audio[:,0];
worker = sFE.sinatraFrontEnd();
x = sA.sinatraAudio(audio=audio, freq=freq, languageClass=1, name='');
matrixMelCeps, matrixCoords, nCol = worker.segmentate(x);
for iter in range(len(matrixCoords[:,0])):
	y = np.zeros(len(audio));
	y[matrixCoords[iter,0]:matrixCoords[iter,1]] = audio[matrixCoords[iter,0]:matrixCoords[iter,1]];
	plt.plot(y);
plt.show();
