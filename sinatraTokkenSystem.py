#!/home/charizard/anaconda3/bin
import sinatraMainClass as sMC;
class sinatraTokkenSystem(sMC.sinatraMainClass):
	def __init__(self, stringCharacters):
		self.__character = [];
		self.__name = 'sinatraTokkenSystem';
		for iter in range(len(stringCharacters)):
			self.__character.append(stringCharacters[iter]);	
	def getSymbols(self):
		return self.__character;
