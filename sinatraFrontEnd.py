import sinatraMainClass as sMC;
class sinatraFrontEnd(sMC.sinatraMainClass):
	def __init__(self):
		import numpy as np;
		self._sinatraMainClass__className = 'sinatraAudio';
		self.__trainingRows = np.zeros((1, 35));
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
		matrixX = np.zeros(35);
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
					cStart = start;
					for tIter in range(len(aCX)-1):
						if fD[tIter]*fD[tIter+1]<0:
							if ((sD[tIter] + sD[tIter + 1])*0.5) < 0:
								maxControl = 1;
							else:
								minControl = 1;
					if (maxControl==1):
						cutPoints = np.array([start, end]);
						tokkenLength = cutPoints[1]-cutPoints[0];
						tokkenRow = np.zeros(tokkenLength);
						tokkenRow = aDClean[cutPoints[0]:cutPoints[1]];
						tokkenInfo = self.extractFeatures(tokkenRow);
						tempTestArray = testArray;
						rowControl = rowControl + 1;
						testArray = np.zeros((rowControl, 2));
						testArray[0:(rowControl-1),:] = tempTestArray;
						testArray[rowControl-1, 0] = start;
						testArray[rowControl-1, 1] = end;
						tempMatrixX = matrixX;
						matrixX = np.zeros((rowControl, 35))
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

	def extractFeatures(self, tokken):
		import sinatraFilter as sF;
		import numpy as np;
		filterBox = sF.sinatraFiltersBox();
		wS = int(len(tokken) / 10);
		featureVector = list();
		featureBox = {};
		featureBox['mean'] = np.mean(tokken);
		featureBox['std'] = np.std(tokken);
		featureBox['len'] = len(tokken)
		featureBox['meanPositive'] = np.mean(tokken[tokken > 0]);
		featureBox['meanNegative'] = np.mean(tokken[tokken < 0]);
		x, featureBox['XmaxFilter'] = filterBox.filterMaxInWindow(tokken, wS);
		x, featureBox['XsoftMaxFilter'] = filterBox.softenedMaxWindow(tokken,wS);
		x, featureBox['XmeanLogAvWindow'] = filterBox.sumAbsWindow(tokken,wS);
		for fkeys, feature in sorted(featureBox.items()):
			if fkeys[0]=='X':
				for intIter in feature:
					featureVector.append(intIter);
			else:
				featureVector.append(feature);
		return featureVector;
