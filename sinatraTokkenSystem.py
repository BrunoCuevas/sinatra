#!/home/charizard/anaconda3/bin
import sinatraMainClass as sMC;
class sinatraTokkenSystem(sMC.sinatraMainClass):
	def __init__(self, stringCharacters):
		self._sinatraMainClass__className='sinatraTokkenSystem';
		self.__character = [];
		self.__name = 'sinatraTokkenSystem';
		i = 0;
		for iter in range(len(stringCharacters)):
			self.__character.append(stringCharacters[iter]);
			i = i + 1;
		self.__size = i;
		#print(len(self.__character));
		#self.__len == len(stringCharacters);
	def getSymbols(self):
		return self.__character;
	def getSize(self):
		return self.__size;
	def createDictionary(self):
		dictionary = {};
		for i1 in range(len(self.__character)):
			for i2 in range(len(self.__character)):
				dictionary[str(self.__character[i1])+str(self.__character[i2])] = 0;
		self.__dictionary = dictionary;
		return 1;
	def getDictionary(self):
		return self.__dictionary;
