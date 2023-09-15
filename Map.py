import numpy as np
import matplotlib.pyplot as plt
import os
import networkx as nx
import glob

def extractFortranFunctions(file_path, OriginalNode):

    #extracting the functions and sub routines
    global MasterNodes, MasterEdges, Counter
    
    
  

    # Read the Fortran code from the file
    with open(file_path, 'r') as file:
        code = file.readlines()
        
        for Entry in code:
            ParsedTextAll = Entry.split()
            if len(ParsedTextAll)>0:
                ParsedText = ParsedTextAll[0].upper()    
                AllNodes = list(MasterNodes.keys())
                if ParsedText == "FUNCTION":
                    CurrentFunction = ParsedTextAll[1].split("(")[0].upper()
                    
                    #Check in needs to be a new node
                    if not(CurrentFunction in AllNodes):
                        MasterNodes[CurrentFunction] = Counter 
                        Counter+=1
                                            
                    CurrentNode = MasterNodes[CurrentFunction]
                    PotentialEdge = [OriginalNode, CurrentNode]
                   
                        
    
                    ##Check in needs to be a new ege
                    if not(PotentialEdge in MasterEdges):
                        MasterEdges.append(PotentialEdge)
                    
                elif ParsedText == "CALL":
                    CurrentSubroutine = ParsedTextAll[1].split("(")[0].upper()
                    
                    #Check in needs to be a new node
                    if not(CurrentSubroutine in AllNodes):
                        MasterNodes[CurrentSubroutine] = Counter 
                        Counter+=1
                                            
                    CurrentNode = MasterNodes[CurrentSubroutine]
                    PotentialEdge = [OriginalNode, CurrentNode]
    
                    ##Check in needs to be a new ege
                    if not(PotentialEdge in MasterEdges):
                        MasterEdges.append(PotentialEdge)
                   
   
    return None


def parseFortranFiles(AllFileLocation):
    
    #Create a universal map for the map
    global MasterNodes, MasterEdges, Counter

    MasterNodes = {}
    MasterEdges = []

    #Expecting there to be at most 100000 files
    Counter = 1
    

    AllFunctions = []
    AllSubRoutines = []
    

    #Categorize the different type of files
    f_files = sorted([file for file in AllFileLocation if file.endswith(".f")])
    f90_files = sorted([file for file in AllFileLocation if file.endswith(".f90")])
    

    #Parse through f90 files
    for fileItem in f90_files+f_files:
        FileName = os.path.basename(fileItem)
        FileName = FileName.split(".")[0].upper()
        AllNodes = list(MasterNodes.keys())

        if not(FileName in AllNodes):
            MasterNodes[FileName] = Counter
            MappedCounter = Counter
            Counter+=1
        else:
            MappedCounter = MasterNodes[FileName]
        
       
        extractFortranFunctions(fileItem, MappedCounter)
        
        #print("Master Nodes:", MasterNodes)
        #print("Master Edges:", MasterEdges)
        #input("Waqt here please")


    #print("Pre-Sorted master nodes")
    #print(MasterNodes)
    #MasterNodes = sorted(MasterNodes.items(), key=lambda x:x[1])
    
    #print("Sorted master nodes")
    print(MasterNodes)
    
    #input("We will wait")
    #input("Read to write to a file")
    
    write2JSfile()

    pass




def getAllFiles(Location, Extension=None):
    # Use os.walk to traverse the directory and its subdirectories
    ""
    AllFiles = []
    for root, _, files in os.walk(Location):
        for file in files:
            file_path = os.path.join(root, file)

            AllFiles.append(file_path)
    return AllFiles

def write2JSfile():

    global MasterNodes, MasterEdges
    
    if not(os.path.exists("data2Visualize")):
        os.mkdir("data2Visualize")
    FileName2Save = "data2Visualize/MainFile2Visualize.js"
    os.system("rm %s" %FileName2Save)
    FileNames = glob.glob("data2Visualize/*.js")
    FileNames = [FileItem.split("/")[-1] for FileItem in FileNames]
    with open(FileName2Save, "w+") as f:
        f.write("const networkData = {\n")

        #Theser are the nodes
        f.write("           nodes: [\n")
    
        #Write 
        for key, value in  MasterNodes.items():
            print(key, value)
            # Add nodes
            Text2Write = " "*10+ "{ id :%s, label:\'%s\'},\n" %(value, key) 
            f.write(Text2Write)
        f.write("               ],\n")


        #Theser are the nodes
        f.write("           edges: [\n")
        
        for Entry in MasterEdges:
            # Add nodes
            Start, Stop= Entry
            Text2Write = " "*10+ "{ from :%s, to:%s},\n" %(Start, Stop) 
            f.write(Text2Write)
        f.write("               ]")
        f.write("   }")
        f.close()

   

def RunAnalysis(Location):
    #
    AllFileLocations = getAllFiles(Location)   
    print("All the file locations is given by:", AllFileLocations)
    parseFortranFiles(AllFileLocations)
    
    




#Get the list 

Location = "/media/prajwal/LaCie/Project_Yumi/MIT_SuperCloud_Version/YUMI/YUMI_CODE/source"
#Location = "/Users/prajwalniraula/Desktop/Project_Yumi/MIT_SuperCloud_Version/YUMI/YUMI_CODE/source"
assert os.path.exists(Location), print("The location does not exist.")
RunAnalysis(Location)