from sklearn import tree
import graphviz 
import pydot
#from io import StringIO
from io import BytesIO as StringIO
import io
import base64
from IPython.display import Image
from graphviz import Source
from sklearn.tree import _tree



class DecisionTree:

    @staticmethod
    def trainTree(trainDataFrame, featuresList, target):
        dt = tree.DecisionTreeClassifier()
        return dt.fit(trainDataFrame[featuresList], trainDataFrame[target])

    
        
    @staticmethod
    def visualizeTree(treeModel, featuresList, targetValues):
        dot_data=tree.export_graphviz(treeModel, out_file=None,
                                      feature_names=featuresList,  
                                      class_names=targetValues,  
                                      filled=True, rounded=True,  
                                      special_characters=True)
        graph = Source(dot_data)
        graph_png=graph.pipe(format='png')
        graph_url=base64.b64encode(graph_png).decode('utf-8')
        return 'data:image/png;base64,{}'.format(graph_url)

       
    @staticmethod
    def tree_to_code(tree, feature_names):
       codelines = []
       tree_ = tree.tree_
       feature_name = [
               feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
               for i in tree_.feature
               ]
       codelines.append("def tree({}):".format(", ".join(feature_names)))
       
       def recurse(node, depth):
           indent = "      " * depth
           if tree_.feature[node] != _tree.TREE_UNDEFINED:
               name = feature_name[node]
               threshold = tree_.threshold[node]
               codelines.append ("{}if {} <= {}:".format(indent, name, threshold))
               recurse(tree_.children_left[node], depth + 1)
               codelines.append("{}else:  # if {} > {}".format(indent, name, threshold))
               recurse(tree_.children_right[node], depth + 1)
           else:
               codelines.append("{}return {}".format(indent, tree_.value[node]))
       recurse(0, 1)
       return codelines
   
    @staticmethod
    def interpretTree(treeCodeLines):
       outStr=""
       lineIndex=-1
       for line in treeCodeLines:
           lineIndex+=1
           if "return [[0." in line:
               pIndex=lineIndex-1
               #print str(pIndex)+":"+treeCodeLines[pIndex]
               if treeCodeLines[pIndex].find('<')>=0:
                   outStr+="Small value of "+ treeCodeLines[pIndex].replace(" if ","").replace("else", "").replace("#","").replace(":","").replace("  ", " ")+" FOR "
               elif treeCodeLines[pIndex].find('>')>=0:
                   outStr+="Large value of "+ treeCodeLines[pIndex].replace(" if ","").replace("else", "").replace("#","").replace(":","").replace("  ", " ")+" FOR "
               j=lineIndex-2
               while j>0:
                    #print str(j)+":"+treeCodeLines[j]
                    if "if " in treeCodeLines[j]:
                        #print "has if"
                        outStr+=treeCodeLines[j].replace(" if ","").replace("else", "").replace("#","").replace(":","").replace("  ", " ") + " AND "
                    elif "return [[" in treeCodeLines[j]:
                        #print "has return"
                        j=j-1                    
                    j=j-1
               outStr=outStr[:-5]
               outStr+="*************"
       return outStr
                    
                    
            

