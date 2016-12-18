import sinatraMainClass as sMC;
class sinatraFrontEnd(sMC.sinatraMainClass):
	global OUTPUTSIZE ;
	OUTPUTSIZE= 100;
	def __init__(self, referenceSystem = None):
		import numpy as np;
		import sinatraTokkenSystem as sTS;
		self._sinatraMainClass__className = 'sinatraAudio';
		self.__trainingRows = np.zeros((1,OUTPUTSIZE)); 
		self.__trainingClass = np.zeros((1,1));
		self.__tokkenSystem = referenceSystem;
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
		for iter in range(OUTPUTSIZE):
			head=head+"s{0}\t".format(iter);
		head=head+"class\n";
		f.write(str(head));
		f.close()
		f = open(name, 'ab');
		for iter in range(len(self.__trainingRows)):
			row2write = np.zeros(OUTPUTSIZE +1 );
			row2write[0:OUTPUTSIZE]	=self.__trainingRows[iter];
			row2write[OUTPUTSIZE]	=self.__trainingClass[iter];
			np.savetxt(f,row2write.reshape(1,-1),fmt="%7.4f", delimiter="\t");
		f.close();
		return 1;
	def trainModel(self):
		#from sklearn.neural_network import MLPClassifier;
		from sklearn import linear_model;
		from sklearn.neural_network import MLPClassifier;
		print("creating nn");
		lR = linear_model.LogisticRegression(C=1e-8,max_iter=10000);
		mP = MLPClassifier(alpha=1e-5, solver ='lbgfs', random_state=14, max_iter=10000)
		print("starting training");
		mP.fit(self.__trainingRows, self.__trainingClass);
		lR.fit(self.__trainingRows, self.__trainingClass);
		print("finishing training");
		self.__lR = lR;
		self.__mP = mP;
		return 1;
	def saveModel(self, filename1, filename2):
		from sklearn.externals import joblib;
		try:
			joblib.dump(self.__lR,filename1);
		except AttributeError:
			print("Logistic Regression Classifier hasn't been trained!");
			return 0;
		try:
			joblib.dump(self.__mP,filename2);
		except AttributeError:
			print("Multiperceptron hasn't been trained!");
			return 0;
		return 1;
	def loadModel(self, filename1, filename2):
		from sklearn.externals import joblib;
		from sklearn.linear_model import LogisticRegression;
		from sklearn.neural_network import MLPClassifier;
		lR = joblib.load(filename1);
		if type(lR) == LogisticRegression:
			self.__lR = lR;
		else:
			print("Not a LogisticRegression object");
			return 0;
		mP = joblib.load(filename2);
		if type(mP) == MLPClassifier:
			self.__mP = mP;
		else:
			print("Not a MLP Classifier object");
			return 0;
	def predict(self, aD):
		import sinatraTokkenSystem as sTS;
		import numpy as np;
		# Obtain Spectral Density
		predictMatrix, x1, x2= self.segmentate(aD);
		del x1; del x2;
		# Control Matrix
		try :
			lenPredict = len(predictMatrix[:,0]);
		except TypeError:
			lenPredict = len(predictMatrix);
		res1 = np.zeros(lenPredict);
		res2 = np.zeros(lenPredict);
		# Predict elements within tokken
		for iter in range(lenPredict):
			row2predict = predictMatrix[iter,:];
			row2predict = row2predict.reshape(1,-1);
			#resLR_p = self.__lR.predict_proba(row2predict);
			#resMP = self.__mP.predict(row2predict);
			resLR = self.__lR.predict(row2predict);
			resMP = self.__mP.predict(row2predict);
			res1[iter] = resLR;
			res2[iter] = resMP;
		try :
			system = self.__tokkenSystem.getSymbols();
		except AttributeError:
			print("Tokken system is undefined");
			return 0;
		cooc = '';
		for iter in range(len(res1)):
			if res1[iter] > 0 :
				cooc = cooc + system[int(res1[iter]-1)];
			elif res1[iter] == 0:
				cooc = cooc + '-';
		aD.includeCoocurrenceInfo(cooc, self.__tokkenSystem);
		return res1,res2;
	def normalize(self, aD):
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
		import matplotlib.pyplot as plt;
		filterBox = sinatraFilter.sinatraFiltersBox();
		coeffCleaning = 1.5;
		wS = 700;
		rowL = 10000;
		rowControl = 1;
		print("reading {0}".format(aD.getName()), end="\t");
		freqVal = aD.getFreq();
		self.normalize(aD);
		aD = aD.getAudio();
		try:
			aD = aD[5000:];
		except IndexError:
			print ("Index Error");
			
		splitNumber = int(len(aD)/wS);
		aDClean = aD;
		#	yE,zE : depreciated
		#	nE : contains the -log probability of belonging to the normal
		yE,zE,nE = filterBox.entropyInWindow(aDClean, 1400);

		del yE; del zE;
		statusStart = 0;
		matrixX = np.zeros(OUTPUTSIZE);
		testArray = np.zeros(2);
		for sIter in range(2, len(aD)-3):
			if statusStart == 0 and nE[sIter] >= 15:
				statusStart = 1;
				start = int(sIter);
			if statusStart == 1 and nE[sIter] < 15:
				statusStart = 0;
				minControl = 0;
				maxControl = 0;
				derControl = 0;
				end = int(sIter);
				if end-start > 2800:
					audioTokken = aDClean[start:end];
					aCX, aCY = filterBox.exponentialDecay(audioTokken, wS);
					fD = filterBox.firstDerivative(aCY);
					sD = filterBox.secondDerivative(aCY);
					xF,yF = filterBox.filterMaxInWindow(filterBox.derivateSound(audioTokken),wS);
					#plt.plot(xF,yF);plt.show();
					cutPoints = np.array([start]);
					for tIter in range(len(aCX)-1):
						if fD[tIter]*fD[tIter+1]<0:
							if ((sD[tIter] + sD[tIter + 1])*0.5) < 0:
								maxControl = 1;
							else:
								if (maxControl == 1) :#and (derControl == 1) :
									cutPoints=np.append(cutPoints,aCX[tIter]+start);
									maxControl = 0;
									

					cutPoints=np.append(cutPoints, end);
					for uIter in range(len(cutPoints)-1):
						currentPoints = np.array([cutPoints[uIter], cutPoints[uIter+1]]);
						tokkenLength = currentPoints[1]-currentPoints[0];
						try:
							tokkenRow = np.zeros(tokkenLength);
						except ValueError:
							exit;
						tokkenRow = aDClean[int(currentPoints[0]):int(currentPoints[1])];
						tokkenInfo = self.extractFeatures(tokkenRow, freqVal);
						if tokkenInfo == None:
							maxControl = 0;
							minControl = 0;
							cStart = tIter;
							continue;
						tempTestArray = testArray;
						rowControl = rowControl + 1;
						testArray = np.zeros((rowControl, 2));
						testArray[0:(rowControl-1),:] = tempTestArray;
						testArray[rowControl-1, 0] = currentPoints[0];
						testArray[rowControl-1, 1] = currentPoints[1];
						tempMatrixX = matrixX;
						matrixX = np.zeros((rowControl, OUTPUTSIZE))
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
		#from python_speech_features import mfcc;
		import math;
		import matplotlib.pyplot as plt;
		filterBox = sF.sinatraFiltersBox();
	
		# spectral density based feature extraction model
		#plt.plot(tokken); plt.show();
		autocorr, z1 = filterBox.autocorrelation(tokken, 200);
		#plt.plot(autocorr); plt.show();
		spectralDensity = np.abs(np.fft.fft(autocorr));
		spectralDensity = spectralDensity[:100];
		#plt.plot(spectralDensity); plt.show();
		try :
			cL = self.__noiseClass.predict(spectralDensity.reshape(1,-1));
		except AttributeError:
			return spectralDensity;
		if cL == 1:
			return spectralDensity;
		else:
			return None;

	def sortPeaks(self, peakList):
		import numpy as np;
		if len(peakList[:,0]) > 2:
			
			maxVal = 0;
			maxIter = 0;
			for iter in range(len(peakList[:,0])):
				if peakList[iter,1] > maxVal:
					maxVal = peakList[iter,1];
					maxIter = iter;
			nM = np.zeros((len(peakList[:,0])-1,2));
			nM[:maxIter,:] = peakList[:maxIter,:];
			nM[maxIter:,:] = peakList[(maxIter+1):,:];
			nM = self.sortPeaks(nM);
			nnM = np.zeros((len(peakList[:,0]),2));
			nnM[0,:]=np.array([maxIter,maxVal]);
			nnM[1:,:]=nM;
			return nnM;
		else:

			if peakList[0,1] < peakList[1,1]:
				nnM = np.zeros((2,2));
				nnM[0,:] = peakList[1,:];
				nnM[1,:] = peakList[0,:];
				return nnM;
			else:
				return peakList; 


	def trainNoiseClass(self):
		from sklearn.linear_model import LogisticRegression;
		lRClass = LogisticRegression(max_iter = 5000, C=1e5);
		lRClass.fit(self.__trainingRows, self.__trainingClass);
		self.__noiseClass = lRClass;
		return 1;		
	def saveNoiseClass(self, name):
		from sklearn.linear_model import LogisticRegression;
		if type(self.__noiseClass) == LogisticRegression:
			from sklearn.externals import joblib;
			joblib.dump(self.__noiseClass, name);
		return 1;
	def loadNoiseClass(self,name):
		from sklearn.linear_model import LogisticRegression;
		from sklearn.externals import joblib;
		self.__noiseClass = joblib.load(name);
		return 1;
		
