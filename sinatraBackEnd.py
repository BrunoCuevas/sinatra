#!/home/charizard/anaconda3/bin/ipython3
import sinatraMainClass as sMC;
class sinatraBackEnd (sMC.sinatraMainClass):
	def __init__(self,system):
		import sinatraTokkenSystem as sTS;
		import numpy as np;
		if type(system) == sTS.sinatraTokkenSystem:
			self.__system = system;
			self.__trainingRows  = np.zeros((1,len(system.getSymbols())**2));
			self.__trainingClass = np.zeros(1);
		else:
			print("error. System provided is not a sinatraTokkenSystem instance");
	def gatherTrainData(self, aD):
		import sinatraTokkenSystem as sTs;
		import numpy as np;
		class_ = aD.getlClass();
		row_ = aD.getCoocurrenceInfo();
		tempClass = self.__trainingClass;
		tempRows = self.__trainingRows;
		lenClass = len(tempClass);
		self.__trainingClass = np.zeros(lenClass + 1);
		self.__trainingRows = np.zeros((lenClass + 1, len(row_)));
		self.__trainingClass[:lenClass] = tempClass;
		self.__trainingClass[lenClass]=class_;
		self.__trainingRows[:lenClass,:] = tempRows;
		self.__trainingRows[lenClass,:] = row_;
		return 1;
	def trainModel(self):
		from sklearn import linear_model;
		print("creating lR");
		lR = linear_model.LogisticRegression(C=1e5, max_iter=1000);
		print("starting training");
		lR.fit(self.__trainingRows, self.__trainingClass);
		print("training finished");
		self.__lR = lR;
		return 1;
	def saveModel(self,filename):
		from sklearn.externals import joblib;
		from sklearn.linear_model import LogisticRegression;
		if type(self.__lR) == LogisticRegression:
			joblib.dump(self.__lR, filename);
			return 1;
		else:
			return 0;
	def loadModel(self,filename):
		from sklearn.externals import joblib;
		from sklearn.linear_model import LogisticRegression;
		lR = joblib.load(filename);
		if type(lR) == LogisticRegression:
			self.__lR = lR;
			return 1;
		else:
			return 0;
	def writeTrainData(self, filename):
		import numpy as np;
		f = open(filename,'w+');
		head="";
		for iter in range(len(self.__trainingRows[0,:])):
			head = head + "s{0}".format(iter);
		head = head + "class";	
		f.write(str(head));
		f.close();
		f.open(filename,'ab');
		for iter in range(len(self.__trainingRows)):
			row2write = np.zeros(len(self.__trainingRow[0,:]));
			row2write[:len(self.__trainingRow[0,:])] = self.__trainingRows[iter];
			row2write[len(self.__trainingRow[0,:])] = self.__trainingClass[iter];
			np.savetxt(f,row2write.reshape(1,-1),fmt="%8.4f",delimiter="\t");
		f.close();
		return 1;

		
		
