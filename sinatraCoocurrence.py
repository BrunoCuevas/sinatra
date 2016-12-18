#!/home/charizard/anaconda3/bin/ipython3
import sinatraMainClass as sMC;
class sinatraCoocurrence(sMC.sinatraMainClass):
	def __init__(self, system):
		import sinatraTokkenSystem as sTS;
		import numpy as np;
		self.__name = 'sinatraCoocurrence';
		print(type(system));
		if type(system) == sTS.sinatraTokkenSystem:
			self.__system = system;
			self.__coocMatrix = np.zeros((system.getSize(), system.getSize()));
			self.__symbols = system.getSymbols();
			self.__dictionary = system.getDictionary();
		else:
			print("error : Not a sinatratokkenSystem");
	def getSystem(self):
		return self.__system.getName();
	def calculateCooc(self, ocArray):
		import numpy as np;
		dictioSymbol = self.__dictionary;
		for iter in range(len(ocArray)-1):
			if ocArray[iter] == "-":
				continue;
			else:
				curr=ocArray[iter]
				foll=ocArray[iter+1]
				try :
					dictioSymbol[str(curr) + str(foll)] = dictioSymbol[str(curr) + str(foll)] +1;
				except KeyError:
					print("error. Tokken {0} out of system".format(str(curr)+str(foll)));
		matrixB = np.zeros((len(dictioSymbol.keys()), len(dictioSymbol.keys())));
		iX = 0;
		iY = 0;
		for iter1 in sorted(dictioSymbol.keys()):
			for iter2 in sorted(dictioSymbol.keys()):
				matrixB[iX,iY]= dictioSymbol[iter1]*dictioSymbol[iter2];
				iY = iY + 1;
			iX = iX + 1;
			iY = 0;
		v = np.linalg.eig(matrixB)
		vector = np.zeros((len(v[0])));
		for iter1 in range (len(v[0])):
			vector[iter1]=v[1][iter1][np.argmax(v[0])]

		return vector;

