from backendClasses.DQTestToolHelper import DQTestToolHelper
#from DataQualityTestTool.db import get_db
#from db import get_db
import sys
from DQTestTool import *
#from __init__ import *
import sqlite3
#inputes: dataRecordsFilePath,trainedModelFilePath,knownFaultsFilePath,constraintDiscoveryMethod
constraintDiscoveryMethod=sys.argv[4]

wsize = None

db=sqlite3.connect("/s/bach/h/proj/etl/shlok/instance/dq.sqlite")
dQTestToolHelper=DQTestToolHelper()
datasetId=dQTestToolHelper.importData(db,dataRecordsFilePath=sys.argv[1],trainedModelFilePath=sys.argv[2],knownFaultsFilePath=sys.argv[3])
#
#hyperParameters={'hidden': [100,100], 'epochs': 5}
win_size=None
hyperParameters={'win_size='+str(win_size)}
numberOfSuspiciousDataFrame=pd.read_sql(sql="select count(*) from dataRecords_"+datasetId+ " where status like 'suspicious'",con=db)
numberOfSuspicious=numberOfSuspiciousDataFrame[numberOfSuspiciousDataFrame.columns.values[0]].values[0]
suspiciousDataFrame=pd.read_sql(sql="select * from dataRecords_"+datasetId+" where status like 'suspicious'", con=db)
dataFrame=pd.read_sql(sql="SELECT * FROM dataRecords_"+datasetId, con=db)    
AFdataFrameOld=pd.DataFrame(columns=[dataFrame.columns.values[0]])

#
faultyRecordFrame,normalRecordFrame,invalidityScoresPerFeature,invalidityScores,faultyThreshold,faultyThresholdRecords,yhatWithInvalidityScores,XWithInvalidityScores,mse_attributes,faultyTimeseriesIndexes,normalTimeseriesIndexes,dataFramePreprocessed,dataFrameTimeseries,y=dQTestToolHelper.constraintDiscoveryAndFaultDetection(db,datasetId,dataFrame,constraintDiscoveryMethod,AFdataFrameOld,suspiciousDataFrame,hyperParameters,win_size=None)    

faultyRecordFrame.to_sql('faultyRecordFrame_'+datasetId, con=db, if_exists='replace', index=False)
db.execute("Update dataRecords_"+datasetId+" set status='suspicious' where  "+dataFrame.columns.values[0]+" in (select "+dataFrame.columns.values[0]+ " from faultyRecordFrame_"+datasetId+")")
db.execute("Drop table faultyRecordFrame_"+datasetId) 


for i in range(0):
    #
    numberOfSuspiciousDataFrame=pd.read_sql(sql="select count(*) from dataRecords_"+datasetId+ " where status like 'suspicious'",con=db)
    numberOfSuspicious=numberOfSuspiciousDataFrame[numberOfSuspiciousDataFrame.columns.values[0]].values[0]
    suspiciousDataFrame=pd.read_sql(sql="select * from dataRecords_"+datasetId+" where status like 'suspicious'", con=db)
    dataFrame=pd.read_sql(sql="SELECT * FROM dataRecords_"+datasetId, con=db)    
    AFdataFrameOld=pd.read_sql(sql="select distinct "+dataFrame.columns.values[0]+" from actualFaults_"+datasetId, con=db)
    #

    db.execute("Update dataRecords_"+datasetId+" set status='actualFaults' where status like 'suspicious' and  "+dataFrame.columns.values[0]+" in (select * from knownFaults_"+datasetId+")")

    db.execute("Update dataRecords_"+datasetId+" set status='valid' where status like 'suspicious'  and "+dataFrame.columns.values[0]+" not in (select * from knownFaults_"+datasetId+")")
    
    #
    """if constraintDiscoveryMethod=="LSTMAutoencoder":
        for i in faultyTimeseriesIndexes[0]:
            (dataFrameTimeseries.loc[dataFrameTimeseries['timeseriesId'] == i]).to_sql('faultyTimeseries_i', con=db, if_exists='replace', index=False)
            faultyRecordsInTimeseries_i=pd.read_sql(sql="select * from faultyTimeseries_i join knownFaults_"+datasetId+ " on faultyTimeseries_i."+dataFrame.columns.values[0]+"=knownFaults_"+datasetId+"."+dataFrame.columns.values[0], con=db)
            if (len(faultyRecordsInTimeseries_i)>0):
                truePositiveRateGroup=truePositiveRateGroup+1.0
            db.execute("Drop table faultyTimeseries_i")
        truePositiveRateGroup=truePositiveRateGroup/float(len(faultyTimeseriesIndexes[0]))"""
    #

<<<<<<< HEAD
    faultyRecordFrame,normalRecordFrame,invalidityScoresPerFeature,invalidityScores,faultyThreshold,yhatWithInvalidityScores,XWithInvalidityScores,mse_attributes,faultyTimeseriesIndexes,normalTimeseriesIndexes,dataFramePreprocessed,dataFrameTimeseries,y=dQTestToolHelper.constraintDiscoveryAndFaultDetection(db,datasetId,dataFrame,constraintDiscoveryMethod,AFdataFrameOld,suspiciousDataFrame,hyperParameters,win_size=wsize)    
=======
    faultyRecordFrame,normalRecordFrame,invalidityScoresPerFeature,invalidityScores,faultyThreshold,faultyThresholdRecords,yhatWithInvalidityScores,XWithInvalidityScores,mse_attributes,faultyTimeseriesIndexes,normalTimeseriesIndexes,dataFramePreprocessed,dataFrameTimeseries,y=dQTestToolHelper.constraintDiscoveryAndFaultDetection(db,datasetId,dataFrame,constraintDiscoveryMethod,AFdataFrameOld,suspiciousDataFrame,hyperParameters,win_size=None)    
>>>>>>> a8257561e97387fa1a8d37c3fcc83f931f2a34d3
    faultyRecordFrame.to_sql('faultyRecordFrame_'+datasetId, con=db, if_exists='replace', index=False)
    db.execute("Update dataRecords_"+datasetId+" set status='suspicious' where  "+dataFrame.columns.values[0]+" in (select "+dataFrame.columns.values[0]+ " from faultyRecordFrame_"+datasetId+")")
    db.execute("Drop table faultyRecordFrame_"+datasetId) 

print (pd.read_sql(sql="select * from scores where dataset_id like '"+datasetId+"'", con=db))

scores=pd.read_sql(sql="select * from scores", con=db)
with open("results/scores.csv", 'w') as f:
    scores.to_csv(f)

