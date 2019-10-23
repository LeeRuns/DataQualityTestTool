from backendClasses.DQTestToolHelper import DQTestToolHelper
#from DataQualityTestTool.db import get_db
#from db import get_db
import sys
from DQTestTool import *
#from __init__ import *
import sqlite3
#inputes: dataRecordsFilePath,trainedModelFilePath,knownFaultsFilePath,constraintDiscoveryMethod
constraintDiscoveryMethod=sys.argv[4]


db=sqlite3.connect("/home/hajar/instance/dq.sqlite")
dQTestToolHelper=DQTestToolHelper()
datasetId=dQTestToolHelper.importData(db,dataRecordsFilePath=sys.argv[1],trainedModelFilePath=sys.argv[2],knownFaultsFilePath=sys.argv[3])
#
numberOfSuspiciousDataFrame=pd.read_sql(sql="select count(*) from dataRecords_"+datasetId+ " where status like 'suspicious'",con=db)
numberOfSuspicious=numberOfSuspiciousDataFrame[numberOfSuspiciousDataFrame.columns.values[0]].values[0]
suspiciousDataFrame=pd.read_sql(sql="select * from dataRecords_"+datasetId+" where status like 'suspicious'", con=db)
dataFrame=pd.read_sql(sql="SELECT * FROM dataRecords_"+datasetId, con=db)    
AFdataFrameOld=pd.DataFrame(columns=[dataFrame.columns.values[0]])
truePositiveRateGroup=0.0
#
faultyRecordFrame,normalRecordFrame,invalidityScoresPerFeature,invalidityScores,faultyThreshold,bestModelFileName,yhatWithInvalidityScores,XWithInvalidityScores,mse_attributes,faultyTimeseriesIndexes,normalTimeseriesIndexes,dataFramePreprocessed,dataFrameTimeseries,y=dQTestToolHelper.constraintDiscoveryAndFaultDetection(db,datasetId,dataFrame,constraintDiscoveryMethod,AFdataFrameOld,suspiciousDataFrame,truePositiveRateGroup)    

faultyRecordFrame.to_sql('faultyRecordFrame_'+datasetId, con=db, if_exists='replace', index=False)
db.execute("Update dataRecords_"+datasetId+" set status='suspicious' where  "+dataFrame.columns.values[0]+" in (select "+dataFrame.columns.values[0]+ " from faultyRecordFrame_"+datasetId+")")
db.execute("Drop table faultyRecordFrame_"+datasetId) 


for i in range(10):
    #
    numberOfSuspiciousDataFrame=pd.read_sql(sql="select count(*) from dataRecords_"+datasetId+ " where status like 'suspicious'",con=db)
    numberOfSuspicious=numberOfSuspiciousDataFrame[numberOfSuspiciousDataFrame.columns.values[0]].values[0]
    suspiciousDataFrame=pd.read_sql(sql="select * from dataRecords_"+datasetId+" where status like 'suspicious'", con=db)
    dataFrame=pd.read_sql(sql="SELECT * FROM dataRecords_"+datasetId, con=db)    
    AFdataFrameOld=pd.read_sql(sql="select distinct "+dataFrame.columns.values[0]+" from actualFaults_"+datasetId, con=db)
    truePositiveRateGroup=0.0
    #

    db.execute("Update dataRecords_"+datasetId+" set status='actualFaults' where status like 'suspicious' and  "+dataFrame.columns.values[0]+" in (select * from knownFaults_"+datasetId+")")

    db.execute("Update dataRecords_"+datasetId+" set status='valid' where status like 'suspicious'  and "+dataFrame.columns.values[0]+" not in (select * from knownFaults_"+datasetId+")")
    
    #
    if constraintDiscoveryMethod=="LSTMAutoencoder":
        print ("faultyTimeseriesIndexes")
        print(faultyTimeseriesIndexes)
        for i in faultyTimeseriesIndexes[0]:
            print("***************")
            print(dataFrameTimeseries)
            print(i)
            print(dataFrameTimeseries.loc[dataFrameTimeseries['timeseriesId'] == i])
            (dataFrameTimeseries.loc[dataFrameTimeseries['timeseriesId'] == i]).to_sql('faultyTimeseries_i', con=db, if_exists='replace', index=False)
            print("select * from faultyTimeseries_i left join knownFaults_"+datasetId+ " on faultyTimeseries_i."+dataFrame.columns.values[0]+"=knownFaults_"+datasetId+"."+dataFrame.columns.values[0])
            faultyRecordsInTimeseries_i=pd.read_sql(sql="select * from faultyTimeseries_i join knownFaults_"+datasetId+ " on faultyTimeseries_i."+dataFrame.columns.values[0]+"=knownFaults_"+datasetId+"."+dataFrame.columns.values[0], con=db)
            print("faultyRecordsInTimeseries_i")
            print(faultyRecordsInTimeseries_i)
            if (len(faultyRecordsInTimeseries_i)>0):
                truePositiveRateGroup=truePositiveRateGroup+1.0
            db.execute("Drop table faultyTimeseries_i")
        print("truePositiveRateGroup")
        print(truePositiveRateGroup)
        truePositiveRateGroup=truePositiveRateGroup/float(len(faultyTimeseriesIndexes[0]))
    #

    faultyRecordFrame,normalRecordFrame,invalidityScoresPerFeature,invalidityScores,faultyThreshold,bestModelFileName,yhatWithInvalidityScores,XWithInvalidityScores,mse_attributes,faultyTimeseriesIndexes,normalTimeseriesIndexes,dataFramePreprocessed,dataFrameTimeseries,y=dQTestToolHelper.constraintDiscoveryAndFaultDetection(db,datasetId,dataFrame,constraintDiscoveryMethod,AFdataFrameOld,suspiciousDataFrame,truePositiveRateGroup)    
    faultyRecordFrame.to_sql('faultyRecordFrame_'+datasetId, con=db, if_exists='replace', index=False)
    db.execute("Update dataRecords_"+datasetId+" set status='suspicious' where  "+dataFrame.columns.values[0]+" in (select "+dataFrame.columns.values[0]+ " from faultyRecordFrame_"+datasetId+")")
    db.execute("Drop table faultyRecordFrame_"+datasetId) 

print (pd.read_sql(sql="select * from scores where dataset_id like '"+datasetId+"'", con=db))

scores=pd.read_sql(sql="select * from scores", con=db)
with open("results/scores.csv", 'w') as f:
    scores.to_csv(f)

