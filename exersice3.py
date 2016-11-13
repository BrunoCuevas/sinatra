#!/usr/bin/python3
import   sinatraIO as sIO;
import  sinatraFrontEnd as sFE;
import numpy as np;
import matplotlib.pyplot as plt;
import sinatraFilter as sF;

path = '/home/charizard/Documents/LRS/Dataset/tablaNombres.csv';
reader = sIO.sinatraIO(path);
feWorker = sFE.sinatraFrontEnd();
reader.readTable();
filterer = sF.sinatraFiltersBox()
worker = sFE.sinatraFrontEnd();
audio1 = next(reader);
a = worker.normalize(audio1);
x = audio1.getAudio()
plt.plot(x, color='orange');
aCX, aCY = filterer.softenedMaxWindow(x, 650);
plt.plot(aCX, aCY, linewidth=3)
aCX, aCY = filterer.filterMaxInWindow(x, 650);
plt.plot(aCX, aCY, linewidth=3)
plt.show()
