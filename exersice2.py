#!/home/charizard/anaconda3/bin/ipython3
import sinatraIO as sIO;
import sinatraFrontEnd as sFE;
import numpy as np;
import matplotlib.pyplot as plt;
from sklearn.neural_network import MLPClassifier;
import sys;
inpath = sys.argv[1];
expath = sys.argv[2];
reader = sIO.sinatraIO(inpath);
feWorker = sFE.sinatraFrontEnd();
reader.readTable();
readerTester = sIO.sinatraIO('/home/charizard/Dropbox/UNIVERSIDAD/Master/Workshop/datasetTrial/testing.csv');
readerTester.readTable();
for aD in reader:
	if aD == 0:
		break;
	else:
		feWorker.gatherTrainData(aD);
feWorker.writeTrainData(expath);

