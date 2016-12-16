#!/home/charizard/anaconda3/bin/ipython3
import numpy as np;
import matplotlib.pyplot as plt;
from scipy.io.wavfile import read;
import sinatraFilter as sF;
import sinatraFrontEnd as sFE;
import sinatraAudio as sA;

import sys;
inpath = sys.argv[1];
freq, audio = read(inpath);
try:
	audio = audio[:,0];
except IndexError:
	pass;
worker = sFE.sinatraFrontEnd();
worker.loadNoiseClass('NM');
filterer = sF.sinatraFiltersBox();
x = sA.sinatraAudio(audio=audio, freq=freq, languageClass=1, name='x');
matrixFeatures, coords, ncol = worker.segmentate(x);
dictioSound = {};
#print(coords);
for iter in range(len(coords[:,0])):
	nameCol = "x{0}".format(iter);
	y = np.zeros(len(audio));
	dictioSound[nameCol]=audio[coords[iter,0]:coords[iter,1]];
	y[coords[iter,0]:coords[iter,1]]=dictioSound[nameCol];
	plt.plot(y);
	#z,r2 = filterer.autocorrelation(dictioSound[nameCol], 1000);
	#print("s = {0} e = {1} r2={2}".format(coords[iter,0], coords[iter,1], r2));
	#if r2 < 0.5:
	#	plt.plot(np.arange(len(dictioSound[nameCol]))+coords[iter,0], dictioSound[nameCol]);

plt.show()

