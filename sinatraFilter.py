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
