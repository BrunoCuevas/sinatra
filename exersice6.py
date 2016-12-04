#!/home/charizard/anaconda3/bin/ipython3
# Bruno Cuevas Zuviria
# Sinatra. Exersice 6.
#
#	Modules
#
import sys;
import numpy as np;
import sinatraFrontEnd as sFE;
import sinatraFilter as sF;
import sinatraAudio as sA;
import matplotlib.pyplot as plt;
from scipy.io.wavfile import read;
import scipy.stats as ss;
filter = sF.sinatraFiltersBox();
#
#	Input
#
print("reading...");
filepath = sys.argv[1];
freq, audioFile = read(filepath);
print("read!");
#
#	Segmentation
#
print("segmentation...");
try:
	audioFile = audioFile[:,0];
except IndexError:
	pass;
audioFile = (audioFile - np.mean(audioFile))/np.std(audioFile);
wS = 800;
x,y,n = filter.entropyInWindow(audioFile, wS);
statusStart = 0;
for sIter in range(len(audioFile)):
	# Now the aim is to identify where can we start
	if statusStart == 0 and n[sIter] > 14:
		print("starting hit at {0}".format(sIter));
		statusStart = 1;
		start = int(sIter);
	elif statusStart == 1 and n[sIter] < 14:
		print("finishing hit at {0}".format(sIter));
		statusStart = 0;
		end = int(sIter);
		audioTokken = audioFile[start:end];
		#aCX, aCY = filter.shiftedFilterMaxInWindow(audioTokken, wS, wS/2);
		aCX, aCY = filter.exponentialDecay(audioTokken, wS);
		fD = filter.firstDerivative(aCY);
		sD = filter.secondDerivative(aCY);
		for tIter  in range(len(aCX)-1):
			if fD[tIter]*fD[tIter+1]<0:
				print("\tIP found!");
				if ((sD[tIter] + sD[tIter+1])*0.5) < 0:
					print("maxima at {0}".format(tIter));
				else:
					print("minima at {0}".format(tIter));
		plt.plot(audioTokken);
		plt.plot(aCX, aCY);
		plt.plot(aCX, fD, '.-');
		plt.plot(aCX, sD, '*-');
plt.axhline(y=0, color="black");
plt.show();
