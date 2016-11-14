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
			aCY[fIter] = np.mean(audioArray[(fIter*wS):(fIter+1)*wS]);
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
				mCY[iter] = mCY[iter] + (math.exp(0.65*(preIter - iter))*aCY[preIter]);
			for postIter in range(iter, len(mCY)):
				mCY[iter] = mCY[iter] + (math.exp(0.65*(iter - postIter))*aCY[postIter]);
		return aCX, mCY;
	def entropyInWindow(self, audioArray, wS):
		import numpy as np;
		import math;
		import scipy.stats as ss;
		sample = audioArray[5000:];
		pValues = np.array([0.001, 0.01, 0.1, 0.5, 0.90, 0.99, 0.999]);
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
