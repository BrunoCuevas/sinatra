#!/home/charizard/anaconda3/bin/python3
from scipy.io.wavfile import read;
import sinatraFilter as sF;
import matplotlib.pyplot as plt;
import numpy as np;
import sys;
freq, audio = read(sys.argv[1]);
audio = (audio-np.mean(audio))/np.std(audio);
try:
	audio = audio[:,0];
except IndexError:
	pass;
x = sF.sinatraFiltersBox();
#sA = x.smoother(audio,345,3);
plt.plot(audio);
#plt.plot(sA);
sA2x, sA2y = x.exponentialDecay(audio,500);
a,sA3z,sA3y = x.entropyInWindow(audio, 700);
plt.plot(sA2x, sA2y, linewidth=3);
#sA3x, sA3y = x.shiftedFilterMaxInWindow(sA, 500, 250);
#plt.plot(sA3x, sA3y, linewidth=3); plt.show()
plt.plot(sA3y, linewidth=3);
plt.plot(a,sA3z,'*-');
plt.show()
