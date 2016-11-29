#!/usr/bin/python3
import sinatraMainClass as sMC;
class sinatraFiltersBox(sMC.sinatraMainClass):
	def __init__(self):
		self._sinatraMainClass__className = 'sinatraFiltersBox';
	def _guessSize(self, audioArray, wS):
		import numpy as np;
		wN = int(len(audioArray)/wS);
		aCX = (np.arange(wN) + 0.5)*wS;
		aCY = np.zeros(wN);
		return wN, aCX, aCY;
	def firstDerivative(self, array):
		import numpy as np;
		der = np.zeros(len(array));
		for iter in range(1, len(array)-1):
			der[iter]=0.5*(array[iter + 1]-array[iter - 1]);
		return der;
	def secondDerivative(self, array):
		import numpy as np;
		der = np.zeros(len(array));
		for iter in range(1, len(array)-1):
			der[iter]=0.25*(array[iter + 1]+array[iter - 1]-(2*array[iter]));
		return der;
	def filterMaxInWindow(self, audioArray, wS):
		#	wS = window Size
		import numpy as np;
		wN, aCX, aCY = self._guessSize(audioArray, wS);
		for fIter in range(wN):
			aCY[fIter] = np.max(audioArray[(fIter*wS):(fIter+1)*wS]);
		return aCX, aCY;
	def averageWindow(self, audioArray, wS):
		import numpy as np;
		wN, aCX, aCY = self._guessSize(audioArray, wS);
		for fIter in range(wN):
			aCY[fIter] = np.mean(np.mean(audioArray[(fIter*wS):(fIter+1)*wS]));
		return aCX, aCY;
	def averagePositiveWindow(self, audioArray, wS):
		import numpy as np;
		wN, aCX, aCY = self._guessSize(audioArray, wS);
		for fIter in range(wN):
			aCY[fIter] = np.mean(audioArray[(fIter*wS):(fIter+1)*wS] * (audioArray[(fIter*wS):(fIter+1)*wS] > 0));
		return aCX, aCY;
	def averageNegativeWindow(self, audioArray, wS):
		import numpy as np;
		wN, aCX, aCY = self._guessSize(audioArray, wS);
		for fIter in range(wN):
			aCY[fIter] = np.mean(audioArray[(fIter*wS):(fIter+1)*wS] * (audioArray[(fIter*wS):(fIter+1)*wS] < 0));
		return aCX, aCY;
	def sumAbsWindow(self, audioArray, wS):
		import numpy as np;
		wN, aCX, aCY = self._guessSize(audioArray, wS);
		for fIter in range(wN):
			aCY[fIter] = np.sum(np.abs(audioArray[(fIter*wS):(fIter+1)*wS]));
		return aCX, aCY;
	def logAverageWindow(self, audioArray, wS):
		import numpy as np;
		import math;
		wN, aCX, aCY = self._guessSize(audioArray, wS);
		for fIter in range(wN):
			aCY[fIter] = math.log(np.abs(np.mean(audioArray[(fIter*wS):(fIter+1)*wS])));
		return aCX, aCY;
	def meanLogAverageWindow(self, audioArray, wS):
		import numpy as np;
		import math;
		wN, aCX, aCY = self._guessSize(audioArray, wS);
		mACX, mACY = self.averageWindow(audioArray, wS);
		lACX, lACY = self.logAverageWindow(audioArray, wS);

		aCY = mACY*lACY;
		return aCX, aCY;
	def softenedMaxWindow(self, audioArray, wS):
		import numpy as np;
		import math;
		wN, aCX, aCY = self._guessSize(audioArray, wS);
		for fIter in range(1,wN-1):
			aCY[fIter] = np.max(audioArray[(fIter*wS):(fIter+1)*wS]);
			aCY[fIter] = aCY[fIter] + 0.5*np.max(audioArray[((fIter-1)*wS):(fIter)*wS]);
			aCY[fIter] = aCY[fIter] + 0.5*np.max(audioArray[((fIter+1)*wS):(fIter+2)*wS]);
		return aCX, aCY;
	def exponentialDecay(self, audioArray, wS):
		import numpy as np;
		import math;
		aCX, aCY = self.filterMaxInWindow(audioArray, wS);
		wN = len(aCX);
		mCY = np.zeros(len(aCY));
		for iter in range(1,wN-1):
			for preIter in range(iter):
				mCY[iter] = mCY[iter] + (math.exp(0.5*(preIter - iter))*aCY[preIter]);
			for postIter in range(iter, len(mCY)):
				mCY[iter] = mCY[iter] + (math.exp(0.5*(iter - postIter))*aCY[postIter]);
		return aCX, mCY;
	def entropyInWindow(self, audioArray, wS):
		import numpy as np;
		import math;
		import scipy.stats as ss;
		sample = np.zeros(5000);
		#sample[:2500] = audioArray[:2500];
		#sample[2500:] = audioArray[(len(audioArray)-2500):];
		minMV = 1000;
		cutPoint = 0;
		for iter in range(len(audioArray)-5000):
			mV = np.sum(np.abs(audioArray[iter:iter+5000]));
			if mV < minMV:
				minMV = mV;
				cutPoint = iter;
		sample = audioArray[cutPoint:cutPoint + 5000];
		pValues = np.array([1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11, 1e-12, 1e-13, 1e-14, 1e-15, 1e-16, 1e-17, 1e-18]);
		pValues = 1 - pValues;
		qValues = ss.norm.ppf(pValues, np.mean(sample), np.std(sample));
		qValues[0] = 0;
		pArray = np.zeros(len(audioArray));
		for iter in range(len(audioArray)):
			pV = max((np.abs(audioArray[iter])>qValues)*pValues);
			pArray[iter] = -np.log10(1 - pV);
		wN, aCX, aCY = self._guessSize(audioArray, wS);
		for iter in range(wN):
			aCY[iter] = np.max(pArray[iter*wS:(iter+1)*wS]);
			pArray[iter*wS:(iter+1)*wS] = aCY[iter];
		return aCX, aCY, pArray;
	def smoother(self, audioArray, degree, iterations):
		import numpy as np;
		import math;
		lA = len(audioArray);
		aD = audioArray[:];

		try :
			aD = aD[:,0];
		except IndexError:
			pass;
		aD = aD*(aD > 0);
		mX = np.zeros(lA);
		if degree % 2 == 0 :
			print("ERROR : degree must be odd\n");
		else :
			boundaryUp = int(degree/2);
			boundaryDn = lA - int(degree/2);
			for rec in range(iterations):
				for iter in range(boundaryUp, boundaryDn ):

					mX[iter] = np.mean(aD[(iter-boundaryUp):(iter+boundaryUp)]);
				aD = mX;
		return aD;
	def shiftedFilterMaxInWindow(self, audioArray, wS, shift):
		import numpy as np;
		import math;
		aCX, aCY = self.filterMaxInWindow(audioArray, wS);
		tempArray = audioArray[shift:];
		audioArray[:len(audioArray)-shift] = tempArray;
		bCX, bCY = self.filterMaxInWindow(audioArray, wS);
		cCX = (aCX + bCX)/2;
		cCY = (aCY + bCY)/2;
		return cCX, cCY;
