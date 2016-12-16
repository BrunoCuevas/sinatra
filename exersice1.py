import   sinatraIO as sIO;
import  sinatraFrontEnd as sFE;
import numpy as np;
import matplotlib.pyplot as plt;
from sklearn.neural_network import MLPClassifier;
path = '/home/charizard/Documents/LRS/Dataset/tablaNombres.csv';
reader = sIO.sinatraIO(path);
feWorker = sFE.sinatraFrontEnd();
reader.readTable();
#for iter in range(10):

# for z in range(1,10):
# 	audio1 = next(reader);
# 	x = audio1.getAudio();
# 	matrix, testArray, nTokkens = feWorker.segmentate(audio1);
# 	for iter in range(len(testArray)):
# 		y = np.zeros(len(x));
# 		y[testArray[iter,0]:testArray[iter,1]] = x[testArray[iter,0]:testArray[iter,1]];
# 		plt.plot(y, label="x->{0}".format(iter));
# 	plt.show();


#err = feWorker.gatherTrainData(audio1);
err = feWorker.trainModel();
testAudio = next(reader);
for audio1 in reader:
	if audio1 == 0:
		break;
	else:
		err = feWorker.gatherTrainData(audio1);
		print("completed");
data, class_ = feWorker.getTrainData();
nn = MLPClassifier(solver='lbgfs', alpha=1e-5,
hidden_layer_sizes=(10,), random_state=1);
nn.fit(data, class_);
x,y,z = feWorker.segmentate(testAudio);
res = np.zeros(z);
for iter in range(z):
	j = x[iter,:]
	j = j.reshape(1,-1)
	a = nn.predict(j);
	res[iter]=a;
	print("row iter : {0}".format(a));
print("0={0}, 1={1}, 2={2}".format(sum(res==0)/z, sum(res==1)/z, sum(res==2)/z));
