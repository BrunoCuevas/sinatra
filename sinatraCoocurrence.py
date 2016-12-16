#!/home/charizard/anaconda3/bin/ipython3
import sinatraMainClass as sMC;
class sinatraCoocurrence(sMC.sinatraMainClass):
	def __init__(self, system):
		import sinatraTokkenSystem;
		import numpy as np;
		self.__name = 'sinatraCoocurrence';
		if type(system) == sinatraTokkenSystem:
			self.__system = system;
			self.__coocMatrix = np.zerosi((system.size, system.size));
			self.__symbols = system.getSymbols();
	def getSystem(self):
		return self.__system.getName();
	def calculateCooc(self,ocArray):
		dictioSymbol = {};
		for iter in range(len(ocArray)):
			if ocArray[iter] in self.__symbols:
				if ocArray[iter] in dictioSymbol.keys():
					dictioSymbol[str(ocArray[iter])] = dictioSymbol[str(ocArray[iter])] + 1;
				else:
					dictioSymbol[str(ocArray[iter])] = 1;
			else:
				print("print : character {0}  out of the symbol system we are using".format(str(ocArray[iter])));
		matrix = np.zeros((len(dictioSymbol.keys()), len(dictioSymbol.keys())));
		for iter1 in sorted(dictioSymbol.keys()):
			for iter2 in sorted(dictioSymbol.keys()):
				matrix[iter1,iter2]= dictioSymbol[iter1]*dictioSymbol[iter2];
		self.__Cooc = matrix;
		return 1;
	
