
#----------------------------------------Decision Tree-------------------------------------------------------------------
from math import *

#Taking Input from the user for about the depth of the tree
height=input("Enter the height of the tree you want to make: ")


#----------------dividing the input rows into the column---------------------------
# the input dataset is in the form of csv ,

rows = []  # number of rows in the file
with open('C:\AML\programming assignment\datasets\\new data\805337709_T_New2.txt') as file:
    rows=file.readlines();


#Dividing the dataset into single rows of string
data=[]  # is the List of List
for singlerow in rows:
    columns=singlerow.split(",") #  I have taken the rows as a string and then splitting them
    finalcolumnList=[] #storing each element to finalList
    type(columns)
    for column in columns:
        if '\n' in column:
            column=column.rstrip('\n') # stripping the \n component
        finalcolumnList.append(column)
    data.append(finalcolumnList)




#-----------------------------entropy-------------------------------------
result=[]
def entropy(dataset):

    #calling the below function to get the number of unque dataset
     result=countingUniqueClassValuesOfNodes(dataset)
     oneCount=result[0]
     zeroCount=result[1]
     totalrecords=zeroCount+oneCount
     if(totalrecords==0):
         return 0
     entr=0.0
    #to avaod log(0) error, when zeroCount = 0 , I will do the operation for oneCount
     if(zeroCount==0):
         entr=-(oneCount/totalrecords)*log2(oneCount/totalrecords)
        #to avaod log(0) error, when oneCount = 0 , I will do the operation for zeroCount
     elif (oneCount==0):
         entr=-(zeroCount/totalrecords)*log2(zeroCount/totalrecords)
     else:
        entr=-((zeroCount/totalrecords)*log2(zeroCount/totalrecords))-((oneCount/totalrecords)*log2(oneCount/totalrecords))
     return entr


#---------counting the unique 0s and 1s in the intermediate dataset
def countingUniqueClassValuesOfNodes(dataset):
    zeroCount=0;oneCount=0;
    arrContainingZeroCountsAndOneCounts=[]
    for row in dataset:
        if row[9]=="Yes(Ontime)":
            oneCount=oneCount+1
        elif row[9]=="No(Delayed)":
            zeroCount=zeroCount+1

    arrContainingZeroCountsAndOneCounts.append(oneCount)
    arrContainingZeroCountsAndOneCounts.append(zeroCount)
    return arrContainingZeroCountsAndOneCounts



#----------------splitting the parent dataset into to child datasets
def SplitDataSet(rows, columnIndex, columnValue):
   splitLambdaFunction=None
   if isinstance(columnValue,int) or isinstance(columnValue,float): # check if the value is a number i.e int or float
      splitLambdaFunction=lambda row:row[columnIndex]>=columnValue
   else:
      splitLambdaFunction=lambda row:row[columnIndex]==columnValue

    # if columnValue in ('0','1','2','3','4','5','6','7','8','9'):
    #     columnValue=int(columnValue)
    # if isinstance(columnValue,int):
    #     splitLambdaFunction=lambda row:int(row[columnIndex])>=columnValue
    # else:
    #     splitLambdaFunction=lambda row:row[columnIndex]>=columnValue
   # Divide the rows into two sets and return them
   childSet1=[row for row in rows if splitLambdaFunction(row)]
   childSet2=[row for row in rows if not splitLambdaFunction(row)]
   return (childSet1,childSet2)


#-----logic to select the node on which the true SubBranch and false subBranch will be divided
# or if it is the last node the value of count of unique 1s and 0s are stored in the array result
#it is class , the reason for choosing it as a class , we need to use the property of Evaluation like  columnIndex,columnValue,results,trueBranch,falseBranch in drawing tree
class nodeEvaluation:
  def __init__(self, columnIndex=9, columnValue=None, results=None, trueBranch=None, falseBranch=None):
    self.columnIndex=columnIndex
    self.columnValue=columnValue
    self.results=results # if it is the last node the value of count of unique 1s and 0s are stored in the array result
    self.trueBranch=trueBranch
    self.falseBranch=falseBranch



COUNTING_DEPTH_OF_CURRENT_NODE=0  # the counter for calculating the depth of the tree

#the below function is constructing the nodes of the tree
#this is a recursive function which the major function like entropy calculation and calculate the max gain
# this will also build the tree nodes upto till the hieght taken as input from the user
def constructNodes(data, depthOfTree=COUNTING_DEPTH_OF_CURRENT_NODE):

    childSet1=[] # childSet1
    childSet2=[] # childSet2
    maxGain=0.0
    bestNode=None # best node on which the tree should be divided
    bestSubtrees=None # it is List/Array of two trees; the tree with false branch and the tree with true branch

    # iterating from the column1 to last column

    # we are iterating columnwise , that means first all the values of column1 will be traversed and pointer will move to the next column
    #for columnPosition in range(1, 7):
    for columnPosition in range(0, 9):
        # now for each column , we are taking the values it has in each row and splitting the dataset
        for eachrow in data:
            childSet1,childSet2=SplitDataSet(data, columnPosition, eachrow[columnPosition]) # splitting the dataset which takes the parent dataset ,the columnPosition and the value of the index
            # print("number of childSet1",len(childSet1))
            # print("number of childSet2",len((childSet2)))

            parentNodeEntropy=entropy(data) # calculating the entropy of Parent node
            totalNumberOfRecordsInParentNode=len(data) # calculating the total number of Records in parent node

            child1Entropy = entropy(childSet1) #calculating the entropy of child1 node
            totalNumberOfRecordsInChild1=len(childSet1) # calculating the total number of Records in child1 node


            child2Entropy= entropy(childSet2)#calculating the entropy of child2 node
            totalNumberOfRecordsInChild2=len(childSet1)#calculating the entropy of child2 node

            #the below equation is the average entropy of the child nodes
            averageEntropyOfChildNodes=(((totalNumberOfRecordsInChild1/totalNumberOfRecordsInParentNode)*child1Entropy)+((totalNumberOfRecordsInChild2/totalNumberOfRecordsInParentNode)*child2Entropy))

            #getting entropy of parensts and average entropy of chils gives me the information gain
            IGain=parentNodeEntropy-averageEntropyOfChildNodes

            #select the maximum information gain of all the gains calculated recursively
            if(IGain>maxGain):
                maxGain=IGain
                bestNode=(columnPosition, eachrow[columnPosition])
                bestSubtrees=(childSet1,childSet2)

    #print(maxGain)

    global COUNTING_DEPTH_OF_CURRENT_NODE  # way of using the global variable in a local function

    #if maxGain is greater than 0 and the counter for depth is greater than height , then perform
    if(maxGain>0) and (COUNTING_DEPTH_OF_CURRENT_NODE<int(height)):
        COUNTING_DEPTH_OF_CURRENT_NODE= COUNTING_DEPTH_OF_CURRENT_NODE + 1          # in creasing the counter for depth
        trueSubTree=constructNodes(bestSubtrees[0], COUNTING_DEPTH_OF_CURRENT_NODE) # recursilvely call the tree for child node 1
        falseSubTree=constructNodes(bestSubtrees[1], COUNTING_DEPTH_OF_CURRENT_NODE) # recursilvely call the tree for child node2
        # print("depth",DEPTHOFTREE)
        #print("bestnode",bestNode[0])

        #this will return the nodeEvaluation with columnIndex,columnValue
        return nodeEvaluation(columnIndex=bestNode[0], columnValue=bestNode[1], trueBranch=trueSubTree, falseBranch=falseSubTree)
    else:
        return nodeEvaluation(results=countingUniqueClassValuesOfNodes(data))

# print(len(data))
# print(data)

decisionTree=constructNodes(data)




#to display the tree in the output console of python
def showTree(tree, tabspace=''):
   # Is this a leaf node?
    if tree.results!=None:
        print(str(tree.results))
    else:
        print("column[",str(tree.columnIndex),"]"+':Value['+str(tree)+"]?")
        # Print the branches
        print(tabspace + 'CHILDSET1->', end=" ")
        showTree(tree.trueBranch, tabspace + '  ')
        print(tabspace + 'CHILDSET2->', end=" ")
        showTree(tree.falseBranch, tabspace + '  ')

showTree(decisionTree)


#------------logic to draw the tree--------------------------------

# logic for building the width of tree
def widthOfNode(decisionTree):
  if decisionTree.trueBranch==None and decisionTree.falseBranch==None: return 1
  return widthOfNode(decisionTree.trueBranch) + widthOfNode(decisionTree.falseBranch)


#logic for building the depth of the tree
def getdepth(decisionTree):
  if decisionTree.trueBranch==None and decisionTree.falseBranch==None: return 0
  return max(getdepth(decisionTree.trueBranch),getdepth(decisionTree.falseBranch))+1


# importing and using the PIL library
from PIL import Image,ImageDraw
def drawDecisionTree(decisionTree, jpeg='localformydata.jpg'):
  widthofPicture= widthOfNode(decisionTree) * 200
  heightofPicture=getdepth(decisionTree)*200+120

  img=Image.new('RGB',(widthofPicture,heightofPicture),(0,255,255))
  draw=ImageDraw.Draw(img)

  drawnode(draw,decisionTree,widthofPicture/2,20)
  img.save(jpeg,'JPEG')

def drawnode(draw,decisionTree,x,y):
  if decisionTree.results==None:
    # with of tree
    w1= widthOfNode(decisionTree.falseBranch) * 70
    w2= widthOfNode(decisionTree.trueBranch) * 70

    # total space required by this node
    left=x-(w1+w2)/2
    right=x+(w1+w2)/2

    # the conditional string
    draw.text((x-20,y-10),'Column['+str(decisionTree.columnIndex)+']:Value['+str(decisionTree.columnValue)+']',(0,0,0))

    # Draw links to the branches
    draw.line((x,y,left+w1/2,y+100),fill=(0,0,222))
    draw.line((x,y,right-w2/2,y+100),fill=(0,0,222))

    # Draw the branch nodes in which the trueBranch of nodeEvaluation is kept at left
    #and the falsBranch is kept at right

    drawnode(draw,decisionTree.trueBranch,left+w1/2,y+100)
    drawnode(draw,decisionTree.falseBranch,right-w2/2,y+100)
  else:
    txt=' \n'.join(['%s'% decisionTree.results])
    draw.text((x-20,y),txt,(0,0,0))


drawDecisionTree(decisionTree, jpeg='decisionTreePictureformyData.jpg')


#-----------------------------building a classifier code ---------------------


def callClassifer(singlerowOfTestData,decisionTree):

  # in the python class of NodeEvaluation ,the result property will be filled only when  it has reached leaf else it has None as value
  # if the  result value is not None then perform next condition
  if decisionTree.results!=None:
      if decisionTree.results[0]> decisionTree.results[1]:
          return "OnTime"                                                                            # if the number of 1s in the leaf node is greater than the number of 0 , return 1
      elif decisionTree.results[1]> decisionTree.results[0]:
          return "Delayed"                                                                             # if the number of 0s in the leaf node is greater than the number of 1 , return 0

      # elif decisionTree.results[1]==decisionTree.results[0]:
      #     arrayContainingprediction.append(1);
      #     return 'cannot classify'

  else:
    valueOftheColumnIndex=singlerowOfTestData[decisionTree.columnIndex]                             # valueOftheColumnIndex is the value of Testdata coulmn which is the particular coulmn of the decision tree
    branch=None
    if isinstance(valueOftheColumnIndex,int):                                                       #if the value is an Integer
      if valueOftheColumnIndex>=decisionTree.columnValue: branch=decisionTree.trueBranch            #traversing the tree on the basis of condition ; here true condtion
      else: branch=decisionTree.falseBranch                                                         #false condition
    else:                                                                                           #if the value is a string: like the values in the last column line 'data_1'
      if valueOftheColumnIndex>=decisionTree.columnValue: branch=decisionTree.trueBranch            # traversal on true
      else: branch=decisionTree.falseBranch                                                         # traversing on false
    return callClassifer(singlerowOfTestData,branch) # recursively call the classifier


#print(callClassifer(["result","2","3","2","2","3","1","data_277"],decisionTree)) for test purpose




#-------------logic for loading the test data -------------------

# the input dataset is in the form of csv ,
with open("C:\AML\programming assignment\datasets\\new data\\testdata - Copy2.txt") as file:
    testRows=file.readlines();

# logic for splitting the each row of data set
arrayContainingTrueClassValueofTestData=[]      #array to  iteratively store the real classs value of test data
print(testRows[0:3])
testData=[]
for singleTestRow in testRows:
    testColumns=singleTestRow.split(",")
    finalTestcolumnList=[]
    type(testColumns)
    indexCounter=0
    for singleTestcolumn in testColumns:
        if indexCounter==9:
            print((singleTestcolumn))
            if(singleTestcolumn=="Yes(Ontime)"):
                arrayContainingTrueClassValueofTestData.append("OnTime")
            else:
                arrayContainingTrueClassValueofTestData.append("Delayed")
            singleTestcolumn= "Result"
            finalTestcolumnList.append(singleTestcolumn)
        # if '\n' in singleTestcolumn:
        #     singleTestcolumn=singleTestcolumn.rstrip('\n')
        #     finalTestcolumnList.append(singleTestcolumn)
        else:
            finalTestcolumnList.append(singleTestcolumn)
        indexCounter+=1
    testData.append(finalTestcolumnList)


#------------logic to iteratively predict the class value of each test data and also store them in an array----------

arrayContainingprediction=[]
for singlerowOfTestData in (testData):
    x=callClassifer(singlerowOfTestData,decisionTree)
    print(singlerowOfTestData,":",x, type(x))
    arrayContainingprediction.append(x)




#logic for finding accuracy
def accuracy(arrayContainingprediction , arrayContainingTrueClassValueofTestData):

    counterOfAccuracy=0
    for i in range(len(arrayContainingprediction)):
        if(arrayContainingprediction[i]==arrayContainingTrueClassValueofTestData[i]):
            counterOfAccuracy+=1

    return counterOfAccuracy/len((arrayContainingTrueClassValueofTestData))

#logic for finding error
def error(arrayContainingprediction , arrayContainingTrueClassValueofTestData):
    counterOfError=0
    for i in range(len(arrayContainingprediction)):
        if(arrayContainingprediction[i]!=arrayContainingTrueClassValueofTestData[i]):
            counterOfError+=1

    return counterOfError/len((arrayContainingTrueClassValueofTestData))

#logic for finding true positive
def calculatingTruePositive(arrayContainingTrueClassValueofTestData, arrayContainingprediction):
    counterTruePositive=0
    for i in range(len(arrayContainingTrueClassValueofTestData)):
        if arrayContainingTrueClassValueofTestData[i]=='OnTime':
             if arrayContainingprediction[i]=='OnTime':
                 counterTruePositive+=1
    return  counterTruePositive

#logic for finding true negative
def calculatingTrueNegative(arrayContainingprediction, arrayContainingTrueClassValueofTestData ):


    counterTrueNegative=0
    for i in range(len(arrayContainingTrueClassValueofTestData)):
        if arrayContainingTrueClassValueofTestData[i]=='Delayed':
             if arrayContainingprediction[i]=='Delayed':
                 counterTrueNegative+=1
    return  counterTrueNegative

#logic for finding false positive
def calculatingFalsePositive(arrayContainingprediction, arrayContainingTrueClassValueofTestData):

    counterFalsePositive=0
    for i in range(len(arrayContainingTrueClassValueofTestData)):
        if arrayContainingTrueClassValueofTestData[i]=='Delayed':
             if arrayContainingprediction[i]=='OnTime':
                 counterFalsePositive+=1
    return  counterFalsePositive


#logic for finding false negative
def calculatingFalseNegative(arrayContainingprediction, arrayContainingTrueClassValueofTestData):
    counterFalseNegative=0
    for i in range(len(arrayContainingTrueClassValueofTestData)):
        if arrayContainingTrueClassValueofTestData[i]=='OnTime':
             if arrayContainingprediction[i]=='Delayed':
                 counterFalseNegative+=1
    return  counterFalseNegative


print("accuracy",accuracy(arrayContainingprediction,arrayContainingTrueClassValueofTestData))
print("errror",error(arrayContainingprediction,arrayContainingTrueClassValueofTestData))
print("TruePositives",calculatingTruePositive(arrayContainingprediction,arrayContainingTrueClassValueofTestData))
print("TrueNegatives",calculatingTrueNegative(arrayContainingprediction,arrayContainingTrueClassValueofTestData))
print("FalsePositives",calculatingFalsePositive(arrayContainingprediction,arrayContainingTrueClassValueofTestData))
print("FalseNegative",calculatingFalseNegative(arrayContainingprediction,arrayContainingTrueClassValueofTestData))

# ontimeprediction=0
# delayprediction=0
# for i in arrayContainingprediction:
#     if i=="OnTime":
#         ontimeprediction+=1
#     if i=="Delayed":
#         delayprediction+=1
#     print(i)
#
# print(ontimeprediction)
# print(ontimeprediction)
#
# trueOntime=0
# trueDelay=0
# for i in arrayContainingTrueClassValueofTestData:
#     if i=="OnTime":
#         trueOntime+=1
#     if i=="Delayed":
#         trueDelay+=1
#     print(i)
#
# print(ontimeprediction)
# print(ontimeprediction)
#
# #
# #
# #
# #
# #
