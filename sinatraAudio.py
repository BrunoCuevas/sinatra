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
	def includeCoocurrenceInfo(self, cooc, tokkenSystem):
		import sinatraCoocurrence as sC;
		coocurrator = sC.sinatraCoocurrence(tokkenSystem);
		self.__cooc = coocurrator.calculateCooc(cooc);
		return 1;
	def isCoocDefined(self):
		if self.__cooc == None:
			return False;
		else:
			return True;
	def getCoocurrenceInfo(self):
		return self.__cooc;
