import sinatraMainClass as sMC;
class sinatraFrontEnd(sMC.sinatraMainClass):
	def __init__(self):
		self._sinatraMainClass__className = 'sinatraAudio';
	def gatherSilenceDataFETraining(self, sAI):
		#
		#	The purpose of this method is to difference silence from sound
		#	in order to split in a scientific way the audio, to perform
		#	further analysis over data. This method also should allow us to
		#	gather some data (cadence time).
		# sAI : Sinatra Audio Instance
		if sAI is sinatraAudio:
			print ("\tprocessing {0}".format(sAI.getName));
	def trainSilenceFE(self):
		pass;
	def gatherFeaturesDataFE(self):
		pass;
	def segmentate(self, sAI):
		#
		#	The purpose of this method is not but to find the frequence of
		#	accent in words. We all know that French words have always the
		#	accent in the last syllable, meanwhile it can be found in different
		#	places in spanish or english. The way to find this should be easy.
		#		1 - Clean the sound. We guess that high frequency
		#			sounds are not important for the accent. So,
		#			we need to perform a fourier transform, remove
		#			the high frequency terms, and come back to period through
		#			an inverse fourier transform.
		#		2 - Perform the derivatives of the amplitude. This is not a
		#			a trivial problem, since the spectrum is not regular, and
		#			differents minimums and maximums can be found. An approach
		#			could be to split the sound in intervals and perform the
		#			derivatives only with the maximum values of each interval.
		#		3 - It should be possible to rebuild the frequency of the
		#			accents from some fourier transform or alike.
		#
		#
		#	coeffCleaning : treshold under which fourier transformed frequencies
		#					are removed
		#	wS	: window-size
		import sinatraIO;

		import numpy as np;
		coeffCleaning = 3;
		wS = 750;
		rowL = 10000;
		aD = sAI.nextAudio();
		aD = aD.getAudio();
		splitNumber = int(len(aD)/wS);
		aDTransformed = np.fft.fft(aD);
		meanADTransformed = np.mean(np.absolute(aDTransformed));
		aDTransformed[aDTransformed < coeffCleaning*meanADTransformed] = 0;
		aDTransformed[20000:] = 0;
		aDClean = np.fft.ifft(aDTransformed);
		aDClean = np.real(aDClean);
		aCY = np.zeros(splitNumber); aCX = np.zeros(splitNumber);
		fD = np.zeros(splitNumber-2); sD = np.zeros(splitNumber-2);
		for splitIter in range(splitNumber):
			aCX[splitIter] = (splitIter - 0.5)*wS;
			aCY[splitIter] = max(aDClean[(wS*(splitIter)):(wS*(splitIter+1))]);
		aCY = aCY * 2;
		for derIter in range(1, splitNumber-2):
			fD[derIter] = (aCY[derIter+1]-aCY[derIter-1])/2;
			sD[derIter] = (1/4)*(aCY[derIter + 1] + aCY[derIter - 1] - 2*aCY[derIter]);
		statusMin = 0;
		statusMax = 0;
		cutPoints = [0, 0];
		rowControl = 1;
		matrixX = np.zeros(rowL);
		for sIter in range(2, splitNumber-3):
			if (fD[sIter]*fD[sIter+1]) < 0:
				if 0.5*(sD[sIter]+sD[sIter + 1]) > 0:
					cutPoints[statusMin]=aCX[sIter];
					statusMin = statusMin + 1;
				else:
					statusMax = 1;
			if (statusMin == 2) and (statusMax == 1):
				statusMin = 1;
				statusMax = 0;
				rowX = np.zeros(rowL);
				tokkenL = int(cutPoints[1]-cutPoints[0] + 1);
				if (tokkenL > 1000) and (tokkenL < 10000):
					rowX[1:tokkenL] = aDClean[int(cutPoints[0]):int(cutPoints[1])];
					rowControl = rowControl + 1;
					tempMatrixX = matrixX;
					matrixX = np.zeros((rowControl, rowL))
					matrixX[0:(rowControl - 1), :] = tempMatrixX;
					matrixX[(rowControl - 1), :] = rowX;
				cutPoints[0] = cutPoints[1];
		return matrixX;
