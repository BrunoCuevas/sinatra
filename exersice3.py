#!/usr/bin/python3
import   sinatraIO as sIO;
import  sinatraFrontEnd as sFE;
import numpy as np;
import matplotlib.pyplot as plt;
import sinatraFilter as sF;

#path = '/home/charizard/Dropbox/UNIVERSIDAD/Master/Workshop/datasetTrial/tablaNombres.csv';
path = '/home/charizard/Documents/LRS/Dataset/tablaNombres.csv';
reader = sIO.sinatraIO(path);
feWorker = sFE.sinatraFrontEnd();
reader.readTable();
filterer = sF.sinatraFiltersBox()
worker = sFE.sinatraFrontEnd();
audio1 = next(reader);

a = worker.normalize(audio1);
x = audio1.getAudio()
fx = np.fft.fft(x);
fx[20000:] = 0;
x = np.fft.ifft(fx);
x = np.real(x);
y,z,n = filterer.entropyInWindow(x, 700);
plt.plot(n);
x = x*(n>=1);
plt.plot(x);
y,z = filterer.averageWindow(x,500);
plt.plot(y,z)
w = filterer.firstDerivative(z);
m = filterer.secondDerivative(z);
plt.plot(y,w)
plt.plot(y,m)

#plt.plot(y, w);
#plt.plot(y, m);
plt.show();
# plt.plot(x, color='orange');
# aCX, aCY = filterer.softenedMaxWindow(x, 650);
# plt.plot(aCX, aCY, linewidth=3)
# aCX, aCY = filterer.exponentialDecay(x, 450);
# plt.plot(aCX, aCY, linewidth=3)
# plt.show()
