import sinatraIO as sIO;
import sinatraFrontEnd as sFE;
import numpy as np;
import matplotlib.pyplot as plt;
from sklearn.neural_network import MLPClassifier;
path = '/home/charizard/Dropbox/UNIVERSIDAD/Master/Workshop/datasetTrial/tablaNombres.csv';
#path = '/home/charizard/Documents/LRS/Dataset/tablaNombres.csv'
reader = sIO.sinatraIO(path);
feWorker = sFE.sinatraFrontEnd();
reader.readTable();
readerTester = sIO.sinatraIO('/home/charizard/Dropbox/UNIVERSIDAD/Master/Workshop/datasetTrial/testing.csv');
readerTester.readTable();
audio1 = next(reader);


matrix, testArray, nt = feWorker.segmentate(audio1);
x=audio1.getAudio();
plt.plot(x);
for iter in range(len(testArray)):
	y = np.zeros(len(x));
	y[testArray[iter,0]:testArray[iter,1]] = x[testArray[iter,0]:testArray[iter,1]];
	plt.plot(y, label="x->{0}".format(iter));
plt.show();
