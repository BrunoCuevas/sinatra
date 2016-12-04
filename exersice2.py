import sinatraIO as sIO;
import sinatraFrontEnd as sFE;
import numpy as np;
import matplotlib.pyplot as plt;
from sklearn.neural_network import MLPClassifier;
path = '/home/charizard/Dropbox/UNIVERSIDAD/Master/Workshop/datasetTrial/tablaNombres.csv';
reader = sIO.sinatraIO(path);
feWorker = sFE.sinatraFrontEnd();
reader.readTable();
readerTester = sIO.sinatraIO('/home/charizard/Dropbox/UNIVERSIDAD/Master/Workshop/datasetTrial/testing.csv');
readerTester.readTable();
#for iter in range(10):
for aD in reader:
	if aD == 0:
		break;
	else:
		feWorker.gatherTrainData(aD);
feWorker.writeTrainData('dataTrainWeka.txt');
#feWorker.trainModel();
#res = feWorker.predict(next(readerTester));
#for iter in res:
#	print("res = {0}".format(iter));

#res = feWorker.predict(next(readerTester));
#for iter in res:
#	print("res = {0}".format(iter));


#for iter in range(len(testArray)):
	#y = np.zeros(len(x));
	#y[testArray[iter,0]:testArray[iter,1]] = x[testArray[iter,0]:testArray[iter,1]];
	#plt.plot(y, label="x->{0}".format(iter));
#plt.show();
# plt.legend();
#
