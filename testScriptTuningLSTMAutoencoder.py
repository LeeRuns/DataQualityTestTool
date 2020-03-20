from backendClasses.DQTestToolHelper import DQTestToolHelper
#from DataQualityTestTool.db import get_db
#from db import get_db
import sys
from DQTestTool import *
#from __init__ import *
import sqlite3
#inputes: dataRecordsFilePath,trainedModelFilePath,knownFaultsFilePath,constraintDiscoveryMethod
constraintDiscoveryMethod=sys.argv[4]


db=sqlite3.connect("/s/bach/h/proj/etl/shlok/Spring_20_Test/instance/dq.sqlite")
dQTestToolHelper=DQTestToolHelper()
datasetId=dQTestToolHelper.importData(db,dataRecordsFilePath=sys.argv[1],trainedModelFilePath=sys.argv[2],knownFaultsFilePath=sys.argv[3])
#
hyperParameters={}
numberOfSuspiciousDataFrame=pd.read_sql(sql="select count(*) from dataRecords_"+datasetId+ " where status like 'suspicious'",con=db)
numberOfSuspicious=numberOfSuspiciousDataFrame[numberOfSuspiciousDataFrame.columns.values[0]].values[0]
suspiciousDataFrame=pd.read_sql(sql="select * from dataRecords_"+datasetId+" where status like 'suspicious'", con=db)
dataFrame=pd.read_sql(sql="SELECT * FROM dataRecords_"+datasetId, con=db)    
AFdataFrameOld=pd.DataFrame(columns=[dataFrame.columns.values[0]])

#
<<<<<<< HEAD
=======
faultyRecordFrame,normalRecordFrame,invalidityScoresPerFeature,invalidityScores,faultyThreshold,yhatWithInvalidityScores,XWithInvalidityScores,mse_attributes,faultyTimeseriesIndexes,normalTimeseriesIndexes,dataFramePreprocessed,dataFrameTimeseries,y=dQTestToolHelper.constraintDiscoveryAndFaultDetection(db,datasetId,dataFrame,constraintDiscoveryMethod,AFdataFrameOld,suspiciousDataFrame,hyperParameters,win_size=10)    
>>>>>>> 4efccf566823310666ae3b3a8f9dbbfaaca731b7

window_size = [10, 20, 30, 40, 50]

for w_size in window_size:
    print(w_size)
    print("************************************************************************************************************")
    faultyRecordFrame,normalRecordFrame,invalidityScoresPerFeature,invalidityScores,faultyThreshold,yhatWithInvalidityScores,XWithInvalidityScores,mse_attributes,faultyTimeseriesIndexes,normalTimeseriesIndexes,dataFramePreprocessed,dataFrameTimeseries,y=dQTestToolHelper.constraintDiscoveryAndFaultDetection(db,datasetId,dataFrame,constraintDiscoveryMethod,AFdataFrameOld,suspiciousDataFrame,truePositiveRateGroup,hyperParameters,win_size=w_size)    

"""faultyRecordFrame.to_sql('faultyRecordFrame_'+datasetId, con=db, if_exists='replace', index=False)
db.execute("Update dataRecords_"+datasetId+" set status='suspicious' where  "+dataFrame.columns.values[0]+" in (select "+dataFrame.columns.values[0]+ " from faultyRecordFrame_"+datasetId+")")
db.execute("Drop table faultyRecordFrame_"+datasetId)"""

print (pd.read_sql(sql="select * from scores where dataset_id like '"+datasetId+"'", con=db))


