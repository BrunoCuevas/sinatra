#!/home/charizard/anaconda3/bin/ipython3
import   sinatraIO as sIO;
import  sinatraFrontEnd as sFE;
import sinatraTokkenSystem as sTS;
import numpy as np;
import matplotlib.pyplot as plt;
from sklearn.neural_network import MLPClassifier;
from sklearn.linear_model import LogisticRegression;
import sys;
path = sys.argv[1];
reader = sIO.sinatraIO(path);
tokkenSystem = sTS.sinatraTokkenSystem('abc');
tokkenSystem.createDictionary();
#print(type(tokkenSystem));
feWorker = sFE.sinatraFrontEnd(tokkenSystem);
feWorker.loadModel('XLR','XMLP');
feWorker.loadNoiseClass('XNM');
reader.readTable();
confussionMatrix1 = np.zeros((4,3));
confussionMatrix2 = np.zeros((4,3));
for audio1 in reader:
	if audio1 == 0:
		break;
	else:
		class_ = audio1.getlClass();
		answer1,answer2 = feWorker.predict(audio1);
		for iter in answer1:
			print("iter = {0}".format(iter));
			confussionMatrix1[class_, iter] = confussionMatrix1[class_,iter] + 1;
		for iter in answer2:
			confussionMatrix2[class_, iter] = confussionMatrix2[class_,iter] + 1;
		print("completed");
print("CONFUSSION MATRIX LR  -> ");
print("\t{0}".format(confussionMatrix1));
print("CONFUSSION MATRIX MLP -> ");
print("\t{0}".format(confussionMatrix2));
#feWorker.trainModel();
#feWorker.saveModel('LOG', 'NEURAL');
#feWorker.loadModel('LOG', 'NEURAL');

