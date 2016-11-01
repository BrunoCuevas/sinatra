import   sinatraIO as sIO;
import  sinatraFrontEnd as sFE;
path = '/home/charizard/Documents/LRS/Dataset/tablaNombres.csv';
reader = sIO.sinatraIO(path);
feWorker = sFE.sinatraFrontEnd();
reader.readTable();
result = feWorker.segmentate(reader);
