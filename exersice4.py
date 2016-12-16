#!/home/charizard/anaconda3/bin/python3
import sinatraIO as sIO;
import sinatraFrontEnd as sFE;
import numpy as np;
import matplotlib.pyplot as plt;
from sklearn.neural_network import MLPClassifier;
from scipy.io.wavfile import write;
from python_speech_features import mfcc;
import sinatraFilter as sF;
path = '/home/charizard/Dropbox/UNIVERSIDAD/Master/Workshop/testDataset1/testDataset1.csv';
#path = '/home/charizard/Documents/LRS/Dataset/tablaNombres.csv';
#reader = sIO.sinatraIO(path);
feWorker = sFE.sinatraFrontEnd();
#reader = sIO.sinatraIO('/home/charizard/Dropbox/UNIVERSIDAD/Master/Workshop/datasetTrial/tablaNombres.csv');
reader = sIO.sinatraIO(path);
reader.readTable();
#readerTester.readTable();
filter = sF.sinatraFiltersBox();
for audio1 in reader:
	if audio1 == 0:
		break;
	else:
		name = audio1.getName();
		freq = audio1.getFreq();
		audio = audio1.getAudio();
		vector,testArray,nC = feWorker.segmentate(audio1);
	
		
		x=audio1.getAudio();
		#plt.plot(matrix);
		for iter in range(len(testArray)):
			y = np.zeros(len(x));
			try :
				y[testArray[iter,0]:testArray[iter,1]] = x[testArray[iter,0]:testArray[iter,1]];
			except IndexError:
				pass;
			plt.plot(y, label="x->{0}".format(iter));
			#write("f{0}.wav".format(iter), freq, x[testArray[iter,0]:testArray[iter,1]])

		#plt.savefig("fig{0}.pdf".format(name));
		#plt.close()
		
	plt.show();
