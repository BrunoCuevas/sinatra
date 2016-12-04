import sinatraMainClass as sMC;
class sinatraFrontEnd(sMC.sinatraMainClass):
	def __init__(self):
		import numpy as np;
		self._sinatraMainClass__className = 'sinatraAudio';
		self.__trainingRows = np.zeros((1,130)); 
		self.__trainingClass = np.zeros((1,1));
	def gatherTrainData(self, aD):
		import numpy as np;
		trainMatrix , thing1, thing2= self.segmentate(aD);
		try:
			rowNumber = len(trainMatrix[:,0]);
		except TypeError:
			return 1;
		
		classArray = np.ones(rowNumber) * aD.getlClass();
		temp = self.__trainingRows;
		newMatrix = np.zeros((rowNumber + len(temp[:,0]), len(temp[0,:]) ));
		newMatrix[0:(len(temp[:,0])),:] = temp;
		newMatrix[(len(temp[:,0])):, :] = trainMatrix;
		self.__trainingRows =newMatrix;
		temp = self.__trainingClass;
		newArray = np.zeros(len(temp) + len(classArray));
		newArray[0:len(temp)] = temp;
		newArray[len(temp):] = classArray;
		self.__trainingClass = newArray;
		return 1;
	def getTrainData(self):
		return self.__trainingRows, self.__trainingClass;
	def writeTrainData(self,name):
		import numpy as np;
		f = open(name, 'w+');
		head="";
		for iter in range(130):
			head=head+"s{0}\t".format(iter);
		head=head+"class\n";
		f.write(str(head));
		f.close()
		f = open(name, 'ab');
		for iter in range(len(self.__trainingRows)):
			row2write = np.zeros(131);
			row2write[0:130]=self.__trainingRows[iter];
			row2write[130]	=self.__trainingClass[iter];
			np.savetxt(f,row2write.reshape(1,-1),fmt="%7.4f", delimiter="\t");
		f.close();
		return 1;
	def trainModel(self):
		#from sklearn.neural_network import MLPClassifier;
		from sklearn import linear_model;
		print("creating nn");
		##nn = MLPClassifier(solver='lbgfs', alpha=1e-5, hidden_layer_sizes=(10,), random_state=1);
		lR = linear_model.LogisticRegression(C=1e5);
		print("starting training");
		#nn.fit(self.__trainingRows, self.__trainingClass);
		lR.fit(self.__trainingRows, self.__trainingClass);
		print("finishing training");
		self.__lR = lR;
		return 1;
	def predict(self, aD):
		import numpy as np;
		predictMatrix, thing1, thing2 = self.segmentate(aD);
		try :
			lenPredict = len(predictMatrix[:,0]);
		except TypeError:
			lenPredict = len(predictMatrix);
		res1 = np.zeros(lenPredict);
		for iter in range(lenPredict):
			row2predict = predictMatrix[iter,:];
			row2predict = row2predict.reshape(1,-1);
			res1[iter] = self.__lR.predict(row2predict);
		return res1;
	def normalize(self, aD):
		#
		#
		#
		#
		import sinatraIO;
		import numpy as np;
		aFAD = aD.getAudio();
		meanAFAD = np.mean(aFAD);
		stdAFAD = np.std(aFAD);
		aFAD = (aFAD - meanAFAD)/stdAFAD;
		aD.modAudio(aFAD);
		return 1;
	def segmentate(self, aD):
		import sinatraIO;
		import sinatraFilter;
		import numpy as np;
		filterBox = sinatraFilter.sinatraFiltersBox();
		coeffCleaning = 1.5;
		wS = 700;
		rowL = 10000;
		rowControl = 1;
		print("reading {0}".format(aD.getName()));
		freqVal = aD.getFreq();
		self.normalize(aD);
		aD = aD.getAudio();
		aD = aD[5000:];
		splitNumber = int(len(aD)/wS);
		aDClean = aD;
		#	yE,zE : depreciated
		#	nE : contains the -log probability of belonging to the normal
		yE,zE,nE = filterBox.entropyInWindow(aDClean, 1400);
		del yE; del zE;
		statusStart = 0;
		matrixX = np.zeros(130);
		testArray = np.zeros(2);
		for sIter in range(2, len(aD)-3):
			if statusStart == 0 and nE[sIter] >= 14:
				statusStart = 1;
				start = int(sIter);
			if statusStart == 1 and nE[sIter] < 14:
				statusStart = 0;
				minControl = 0;
				maxControl = 0;
				end = int(sIter);
				if end-start > 2800:
					audioTokken = aDClean[start:end];
					aCX, aCY = filterBox.exponentialDecay(audioTokken, wS);
					fD = filterBox.firstDerivative(aCY);
					sD = filterBox.secondDerivative(aCY);
					cutPoints = np.array([start]);
					for tIter in range(len(aCX)-1):
						if fD[tIter]*fD[tIter+1]<0:
							if ((sD[tIter] + sD[tIter + 1])*0.5) < 0:
								maxControl = 1;
							else:
								if (maxControl == 1) :
									cutPoints=np.append(cutPoints,aCX[tIter]+start);
									maxControl = 0;
								else:
									print("something weird took place...!");
					cutPoints=np.append(cutPoints, end);
					print(cutPoints);
					for uIter in range(len(cutPoints)-1):
						print("are we inside the loop");
						currentPoints = np.array([cutPoints[uIter], cutPoints[uIter+1]]);
						print("current points are {0} and {1}".format(currentPoints[0], currentPoints[1]));
						tokkenLength = currentPoints[1]-currentPoints[0];
						try:
							tokkenRow = np.zeros(tokkenLength);
						except ValueError:
							print(tokkenLength);
							exit;
						tokkenRow = aDClean[int(currentPoints[0]):int(currentPoints[1])];

						tokkenInfo = self.extractFeatures(tokkenRow, freqVal);
						
						tempTestArray = testArray;
						rowControl = rowControl + 1;
						testArray = np.zeros((rowControl, 2));
						testArray[0:(rowControl-1),:] = tempTestArray;
						testArray[rowControl-1, 0] = currentPoints[0];
						testArray[rowControl-1, 1] = currentPoints[1];
						tempMatrixX = matrixX;
						matrixX = np.zeros((rowControl, 130))
						matrixX[0:(rowControl - 1), :] = tempMatrixX;
						matrixX[(rowControl - 1), :] = tokkenInfo;
						maxControl = 0;
						minControl = 0;
						cStart = tIter;
				statusStart = 0;
		print("task completed");
		try :
			matrixX = matrixX[1:,:];
		except IndexError:
			return [], testArray, 0
		try :
			testArray = testArray[1:,:];
		except IndexError:
			return [], testArray, 0
		testArray = testArray + 5000;
		return matrixX, testArray, (rowControl - 1);

	def extractFeatures(self, tokken, freq):
		import sinatraFilter as sF;
		import numpy as np;
		from python_speech_features import mfcc;
		import math;
		filterBox = sF.sinatraFiltersBox();
		featureVector = np.zeros(130);

		melCepstrum = mfcc(tokken, freq);
	
		for fIter in range(len(melCepstrum[0,:])):
			cR = melCepstrum[:,fIter];
			acy = filterBox.averageMFCC(cR, 10);
			
				
			featureVector[(fIter*10):(fIter+1)*10]=acy[:];
		return featureVector;
