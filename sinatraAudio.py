import sinatraMainClass as sMC;
class sinatraAudio(sMC.sinatraMainClass):
	def __init__(self, name, languageClass, audio, freq):
		self._sinatraMainClass__className = 'sinatraAudio';
		self.__name = name;
		self.__lClass = languageClass;
		self.__audio = audio;
		self.__freq = freq;
		self.__cooc = None;
	def getName(self):
		return (self.__name);
	def getlClass(self):
		return (self.__lClass);
	def getAudio (self):
		return (self.__audio);
	def getFreq (self):
		return (self.__freq);
	def modAudio(self, aD):
		self.__audio = aD;
	def includeCoocurrenceInfo(self, cooc):
		import sinatraCoocurrence as sC;
	def isCoocDefined(self):
		if self.__cooc == None:
			return False;
		else:
			return True;
	def getCoocurrenceInfo(self,cooc):
		return CoocurrenceInfo;
