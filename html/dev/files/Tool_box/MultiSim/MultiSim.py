#!/usr/bin/python

import string
import re
import sys
import os

def createTrack (profilFileName):
    with open(profilFileName,  'a') as profilFile:
            profilFile.write(raw_input("Track name : ")+'\n')
            profilFile.write(raw_input("Inactive inputs (ex : O_stress,AA_starvation,TLR4) : ")+'\n')
            profilFile.write(raw_input("Active inputs (ex : Inflamation,DAN_damage) : ")+'\n')
            profilFile.write(raw_input("Custom rate nodes (ex : u:node1:0.15,u:node2:0.1,d:node2:0.1)  : ")+'\n')
            profilFile.write(raw_input("Custom state nodes ( ex : node1:0.1,node2:0.4) : ") +'\n')
            profilFile.write(raw_input("Outputs (ex : BECN1,Ulk_C,PIK3C3) : ")+'\n')
  
######################################################################  

def createProfil (configFileName):
    choice = raw_input("No profil file was given. Do you wish to create a new profil file ? (y/n)")
    if choice == "n":
        print("Quitting...")
        exit(-3)
    else :
        name = raw_input("Base name of the profil file (no path) : ")
        dirName = os.path.dirname(configFileName)
        if dirName != "" :
            profileFileName = os.path.dirname(configFileName)+name
        else :
            profileFileName = name
        createTrack(profileFileName)
        return  profileFileName

######################################################################  
        
def displayTracks (profilFileName):
    with open(profilFileName,  'r') as profilFile:
        profilFileLines = profilFile.readlines()
    print("Existing tracks :")
    i = 0
    while i < len(profilFileLines):
        print(str((i/6)+1) + ")" + profilFileLines[i].rstrip())
        i = i+6

######################################################################  
        
def deleteTrack(profilFileName):
    displayTracks(profilFileName)
    trackNumbers = raw_input("Select single (ex : 1) or multiple tracks to be deleted (ex : 1,2,3) :").split(',')
    
    with open(profilFileName,  'r') as profilFile:
        profilFileLines = profilFile.readlines()
    
    trackNumbers = [ (int(trackNumber)-1)*5 for trackNumber in trackNumbers ]
    trackNumbers = [ (x,x+1,x+2,x+3, x+4) for x in trackNumbers ]
    trackNumbers = [ x for sublist in trackNumbers for x in sublist ]
    
    with open(profilFileName,  'w') as profilFile:
        i = 0
        while i < len(profilFileLines):
            if i not in trackNumbers:
                profilFile.write(profilFileLines[i])
            i = i+1
    print(sum(1 for line in open(profilFileName)))
    if sum(1 for line in open(profilFileName)) < 2:
        print("All tracks have been erased. Consider creating new tracks to start simulations.")
        commandLine = "rm "+profilFileName
        os.system(commandLine)
        
#######################################################################

def createConfigFiles(configFileName, profilFileName,  mutationFileName): 
    displayTracks(profilFileName)
    
    with open(profilFileName,  'r') as profilFile:
        profilFileLines = profilFile.readlines()
    
    with open(configFileName,  'r') as cfgFile:
        cfgFileLines = cfgFile.readlines()
    
    selectedTracks = raw_input("Select tracks to use(ex : 1,3,5,6) : ").split(',')
    selectedTracks = [(int(number)-1)*6 for number in selectedTracks]
    
    configFileList = []
    
    if mutationFileName != "":
        with open(mutationFileName,  'r') as mutationFile:
            mutationFileLines = mutationFile.readlines()
            mutationTable = [mutationFileLine.rstrip().split(',') for mutationFileLine in mutationFileLines] 
            #print(mutationTable)
            mutationTable = [ [mutation.split(':') for mutation in mutationGroup] for mutationGroup in mutationTable]
            #print(mutationTable)
    
    for track in selectedTracks:
        
        trackName = profilFileLines[track].rstrip()
        inactiveInputs = profilFileLines[track+1].rstrip().split(',') 
        activeInputs = profilFileLines[track+2].rstrip().split(',') 
        customRates = profilFileLines[track+3].rstrip().split(',') 
        customRates = [ customRate.split(':') for customRate in customRates ]
        customStates = profilFileLines[track+4].rstrip().split(',')
        customStates = [ customState.split(':')  for customState in customStates ]
        outputs = profilFileLines[track+5].rstrip().split(',') 
        
        ratesTable = []
        internalTable = []
        parametersTable = []
        
        for cfgFileLine in cfgFileLines:
            if cfgFileLine[0] == '$':
                ratesTable.append(cfgFileLine)
            elif re.search('istate=0',  cfgFileLine):
                internalTable.append(re.sub('istate=0',  'is_internal=1',  cfgFileLine))
            else:
                parametersTable.append(cfgFileLine)
          
#####Parsing bien degueu pour creer les fichiers de config
        
        j=0
        while j < len(parametersTable):
            if re.search('sample_count',  parametersTable[j]):
                parametersTable[j] = re.sub('500000',  '50000',  parametersTable[j])
            elif re.search('max_time',  parametersTable[j]):
                parametersTable[j] = re.sub('5',  '100',  parametersTable[j])
            elif re.search('time_tick',  parametersTable[j]):
                parametersTable[j] = re.sub('0[.]01',  '0.1',  parametersTable[j])
            elif re.search('thread_count',  parametersTable[j]):
                parametersTable[j] = re.sub('4',  '8',  parametersTable[j])
            elif re.search('statdist_traj_count',  parametersTable[j]):
                parametersTable[j] = re.sub('100',  '0',  parametersTable[j])
            j = j+1
            
        j=0
        while j < len(internalTable):
            for output in outputs:
                pattern = "^"+output+"[.]"
                if  re.search(pattern,  internalTable[j]):
                    internalTable[j] = re.sub('=1',  '=0',  internalTable[j])
            j = j+1
            
        j = 0
        if customRates != [['']]:
            while j < len(ratesTable):
                for customRate in customRates:
                    if re.match("[$]"+customRate[0]+"_"+customRate[1],  ratesTable[j]):
                        ratesTable[j] = re.sub("=1",  "="+customRate[2],  ratesTable[j])
                j = j+1
         
        if mutationFileName == "" :            
            newCfgFileName = re.sub("[.]cfg", "", configFileName) + "_" + trackName + ".cfg"
            configFileList.append(newCfgFileName)
            with open(newCfgFileName,  'w') as newCfgFile:
                for rate in ratesTable:
                    newCfgFile.write(rate)
                newCfgFile.write('\n')
                for inputNode in activeInputs:
                    if inputNode != "":
                        newCfgFile.write(inputNode+".istate=1;\n")
                for inputNode in inactiveInputs:
                    if inputNode != "":
                        newCfgFile.write(inputNode+".istate=0;\n")
                for customState in customStates:
                    if customState != ['']:
                        newCfgFile.write("["+customState[0]+"]"+".istate="+str(1-float(customState[1]))+"[0],"+customState[1]+"[1];\n")
                newCfgFile.write('\n')
                for internal in internalTable:
                    newCfgFile.write(internal)
                for parameter in parametersTable:
                    newCfgFile.write(parameter)
                    
        else :
            for mutationGroup in mutationTable:

                tempRatesTable = list(ratesTable)
                tempActiveInputs = list(activeInputs)
                tempInactiveInputs = list(inactiveInputs)
                
                for mutation in mutationGroup :
                    if mutation[0] == 'u' :
                        tempActiveInputs.append(mutation[1])
                        i = 0
                        while i < len(tempRatesTable) :
                            if re.match("[$]d_"+mutation[1],  tempRatesTable[i]):
                                tempRatesTable[i] = re.sub("=.+",  "=0;",  tempRatesTable[i])
                            i = i+1
                            
                    else : 
                        tempInactiveInputs.append(mutation[1])
                        i = 0
                        while i < len(tempRatesTable) :
                            if re.match("[$]u"+"_"+mutation[1],  tempRatesTable[i]):
                                tempRatesTable[i] = re.sub("=.+",  "=0;",  tempRatesTable[i])
                            i = i+1
                
                newCfgFileName = re.sub("[.]cfg", "", configFileName) + "_" + trackName + "_"  + '_'.join([ '_'.join(mutation) for mutation in mutationGroup]) + ".cfg"
                configFileList.append(newCfgFileName)
                with open(newCfgFileName,  'w') as newCfgFile:
                    for rate in tempRatesTable:
                        newCfgFile.write(rate)
                    newCfgFile.write('\n')
                    for inputNode in tempActiveInputs:
                        if inputNode != "":
                            newCfgFile.write(inputNode+".istate=1;\n")
                    for inputNode in tempInactiveInputs:
                        if inputNode != "":
                            newCfgFile.write(inputNode+".istate=0;\n")
                    for customState in customStates:
                        if customState != [''] and customState[0] not in tempInactiveInputs and customState[0] not in tempActiveInputs :
                            print(customState[0])
                            newCfgFile.write("["+customState[0]+"]"+".istate="+str(1-float(customState[1]))+"[0],"+customState[1]+"[1];\n")
                    newCfgFile.write('\n')
                    for internal in internalTable:
                        newCfgFile.write(internal)
                    for parameter in parametersTable:
                        newCfgFile.write(parameter)
                
                
    return configFileList
    
#############################################################

def PBSProcedure(configFileList):
    i=1
    for configFile in configFileList:
        if os.path.dirname(configFile) != '' :
            os.chdir(os.path.dirname(configFile))
        scriptName = "MaBoSS_simulation_"+str(i)+".sh"
        
        with open(scriptName,  'w') as scriptFile:
            scriptFile.write("#!/bin/bash\n## Torque Configuration\n# resources \n#PBS -l walltime=06:00:00\n#PBS -l mem=24gb\n#PBS -l nodes=1:ppn=8\n#PBS -q batch\n## Command section\ncd $PBS_O_WORKDIR\n \necho Running on host `hostname`\necho Time is `date`\necho Directory is `pwd`\n\n./FormatMaBoSS.pl "+" "+os.path.basename(re.sub("[.]cfg", ".bnd", sys.argv[1]))+" "+os.path.basename(configFile)+" 0.1")
        
        commandLine = "qsub "+scriptName
        os.system(commandLine)
        
        i = i+1
        
############################################################

def  internalLaunchProcedure(configFileList):
    
    for configFile in configFileList:
        if os.path.dirname(configFile) != '' :
            os.chdir(os.path.dirname(configFile))
        commandLine = "./FormatMaBoSS.pl "+" "+os.path.basename(re.sub("[.]cfg", ".bnd", sys.argv[1]))+" "+os.path.basename(configFile)+" 0.1"
        os.system(commandLine)

###############################################################"

if len(sys.argv) != 2 and len(sys.argv) != 3 and  len(sys.argv) != 4:
    print("Requires at least one argument (a config file)")
    exit(-2)
    
configFileName = sys.argv[1]

if len(sys.argv) == 2:
    profilFileName = createProfil(configFileName)
else :
    profilFileName = sys.argv[2]
    
if len(sys.argv) == 4:
    mutationFileName = sys.argv[3]
else :
    mutationFileName = ""
    
choice = "1"
while (choice != "0" ):
    choice = raw_input("generate config files using exiting tracks (0), create a new track (1) or delete a track (2): ")
    if choice == "0" or choice == "1" or choice == "2":
        if choice == "1":
            createTrack(profilFileName)
        if choice == "2":
           deleteTrack(profilFileName)
        if choice == "0":
            if os.path.isfile(profilFileName) :
                configFileList = createConfigFiles(configFileName, profilFileName,  mutationFileName)
            else :
                choice = "1"
                print("The profil file doesn't exist. Creating new track... Please folow instructions")
                createTrack(profilFileName)

while (choice != "y" and choice != "n"):
    choice = raw_input("Launch simulation on cluster ? (y/n)")
    if choice == "y":
        PBSProcedure(configFileList)
    else :
        internalLaunchProcedure(configFileList)

