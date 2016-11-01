#!/usr/bin/python3
class sinatraMainClass:
	def __init__(self):
		self.__className = 'sinatraMainClass';
		self.__version = 1.0;
	def getVersion(self):
		print(self.__version);
	def __repr__(self):
		return "sinatra - {0}".format(self.__className);
