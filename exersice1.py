import   sinatraIO as sIO;
import  sinatraFrontEnd as sFE;
import numpy as np;
import matplotlib.pyplot as plt;
path = '/home/charizard/Documents/LRS/Dataset/tablaNombres.csv';
reader = sIO.sinatraIO(path);
feWorker = sFE.sinatraFrontEnd();
reader.readTable();
audio1 = reader.nextAudio();
x = audio1.getAudio();
matrix, testArray, nTokkens = feWorker.segmentate(audio1);
for iter in range(len(testArray)):
	y = np.zeros(len(x));
	y[testArray[iter,0]:testArray[iter,1]] = x[testArray[iter,0]:testArray[iter,1]];
	plt.plot(y, label="x->{0}".format(iter));
plt.show();
plt.legend();
