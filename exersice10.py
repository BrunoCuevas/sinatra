#!/home/charizard/anaconda3/bin/ipython3
import numpy as np;
import matplotlib.pyplot as plt;
import sinatraFrontEnd as sFE;
import sinatraAudio as sA;
import sinatraIO as sIO;
import sinatraTokkenSystem as sTS;
import sys;
inpath = sys.argv[1];
outpath1 = sys.argv[2];
outpath2 = sys.argv[3];
reader = sIO.sinatraIO(inpath);
tokkenSystem = sTS.sinatraTokkenSystem('abc');
tokkenSystem.createDictionary();
worker = sFE.sinatraFrontEnd(tokkenSystem);
#worker.loadNoiseClass('XNM');
reader.readTable();
for audio in reader:
	if audio == 0:
		break;
	else:
		worker.gatherTrainData(audio);
worker.trainModel();
worker.saveModel(outpath1, outpath2);
