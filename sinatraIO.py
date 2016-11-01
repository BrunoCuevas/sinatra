#!/usr/bin/python3
import sinatraMainClass as sMC;
class sinatraIO(sMC.sinatraMainClass):
	# This class needs:
	#	1-A way to control that tables that we read contain
	#	the standard header
	#	2-A change in the iterator. We don't want to keep files in memory
	#	since we might be working with a big bunch of information.
	def __init__(self, input):
		from os.path import dirname;
		self._sinatraMainClass__className = 'sinatraIO';
		self.__input = input;
		self.__path = dirname(self.__input);
	def getInput(self):
		return self.__input;
	def getPath(self):
		return self.__path;
	def readTable(self):
		from os import listdir;
		from os.path import isfile, join, splitext;
		from scipy.io.wavfile import read;
		import pandas as pd;
		fileDictionary = {};
		freqDictionary = {};
		classDictionary = {};
		filesTable = pd.read_csv(self.__input, delimiter=",");
		print ("reading table {0}".format(self.__input));
		for index, row in filesTable.iterrows():
			iterFile = row['file'];
			if iterFile in listdir(self.__path):
				if isfile(join(self.__path,iterFile)):
					iterFileName, iterFileExtension = splitext(iterFile);
					if iterFileExtension == '.wav':
						freqDictionary[iterFileName], fileDictionary[iterFileName] = read(self.__path + '/' + iterFile);
						classDictionary[iterFileName] = row['class'];
				else:
					print("\tpath no file for {0}".format(iterFile));
		self.__audio = fileDictionary;
		self.__freq  = freqDictionary;
		self.__class = classDictionary;
		print("task completed");
		return 1;

	def nextAudio(self):
		import sinatraAudio as sA;
		name2purge = sorted(self.__audio.keys());
		name2purge = name2purge.pop();
		audio2purge = self.__audio.pop(name2purge);
		freq2purge = self.__freq.pop(name2purge);
		class2purge = self.__class.pop(name2purge);
		return sA.sinatraAudio(name2purge, class2purge, audio2purge, freq2purge);
