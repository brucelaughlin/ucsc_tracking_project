# Generate config files for Opendrift Runs

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import argparse
import shutil
import os
from pathlib import Path
import numpy as np

config_template_file = "/home/blaughli/tracking_project/practice/experiments/testing/memory_tests_v3/config_template.config.yaml"

cwd = os.getcwd() 



his_file_name_pre = "wc15n_"

experimentDir_pre="memory_test"

#projectionDirectories=["WC15N_HADTV"]
projectionDirectories=["WC15N_GFDLTV"]
#projectionDirectories=["WC15N_GFDLTV" "WC15N_HADTV" "WC15N_IPSLTV"]

baseInputDir_pre="/data/blaughli/jerome_projections/"
#baseInputDir=baseInputDir_pre/projectionDirectories[projectionNumber]

baseOutputDir="/data/blaughli/tracking_project_output_projections/memory_tests/"
#baseOutputDir="/data/blaughli/tracking_project_output_projections"


#experimentDir=experimentDir_pre_projectionDirectories[projectionNumber]
#outputDir=baseOutputDir/experimentDir


#echo "InputDir: baseInputDir
#echo "OutputDir: outputDir

driftDays=150

dtCalc=60
#dtCalc=1440

dtSave=1440

bufferLength=100

maxNodes=12

seedSpacing=2


#numRunsPerJobList=[5,10,15,20,30,35,40]
numRunsPerJobList=[1,5,10]

#numRunsPerJobList=[5,6,10,15,20,35,40]
#numRunsPerJobList=(15 20 25 30 35 40)
#numRunsPerJobList=(4 5 6 7 8 9 10)
#nSeedList=[40]

#nSeedList=[20,30,40]
nSeedList=[100,20,10]

#for projectionNumber in range(len(projectionDirectories)):

#-------------------------------------
# INDENT HERE ------------------------
#-------------------------------------

# testing
projectionNumber=0

baseInputDir = baseInputDir_pre + projectionDirectories[projectionNumber]

modelDirList= os.listdir(path=baseInputDir)
modelDirList.sort()    

modelDirList = [baseInputDir + "/" + item for item in modelDirList]

for hh in range(len(numRunsPerJobList)):
    for kk in range(len(nSeedList)):

## testing
#hh=0
#kk=0

    #-------------------------------------
    # INDENT HERE ------------------------
    #-------------------------------------

            #-------------------------------------
            # INDENT HERE ------------------------
            #-------------------------------------

        numRunsPerJob=numRunsPerJobList[hh]
        nSeed=nSeedList[kk]
        #experimentDir="${experimentDir_pre}_nRunsPerNode_$(printf %02d ${numRunsPerJob})_nSeed_$(printf %02d ${nSeed})"
        experimentDir = "{a}_nRunsPerNode_{b:02d}_nSeed_{c:02d}".format(a=experimentDir_pre, b=numRunsPerJob, c=nSeed)
        outputDir=baseOutputDir + experimentDir

        

        ## -------------------------------------------------------------------
        ## Perhaps this should not be in the config creation script....
        path = Path(outputDir + "/z_logs")
        path.mkdir(parents=True, exist_ok=True)
        
        path = Path(outputDir + "/z_slurmOut")
        path.mkdir(parents=True, exist_ok=True)
        
        path = Path(outputDir + "/z_config_files")
        path.mkdir(parents=True, exist_ok=True)
        config_dir = str(path)
        ## -------------------------------------------------------------------


        dayNudgeRun=nSeed*seedSpacing
        dayNudgeJob=dayNudgeRun*numRunsPerJob

        # Had not been allowing enough his files to be read by readers. Will also need more than 2 readers if Mesoscale can handle bigger jobs.
        numYearsJob=np.ceil(dayNudgeJob/365)+1
        #numYearsJob=np.round(dayNudgeJob/365)+2



        #printf '%s\n' modelDirList[@]


        daysPerYearList=[]
        for ii in range(len(modelDirList)):
            #runYearList= os.listdir(path=baseInputDir+"/" + modelDirList[ii])
            runYearList= os.listdir(path=modelDirList[ii])
            runYearList.sort()
            runYearList = [item for item in runYearList if item[0:len(his_file_name_pre)] == his_file_name_pre]
            daysPerYearList.append(len(runYearList))



        cumulativeDaysYearList=[]
        totalDays=0
        for ii in range(len(daysPerYearList)):
            day_sum=0
            totalDays = totalDays + daysPerYearList[ii]
            for jj in range(ii+1):
                day_sum = day_sum + daysPerYearList[jj]
            cumulativeDaysYearList.append(day_sum)



        lastSeedDay = totalDays-driftDays

        numRuns=round((totalDays + (dayNudgeRun-1))/dayNudgeRun)
        #numRuns=(totalDays + (dayNudgeRun-1))/dayNudgeRun
        #echo "numRuns"
        numJobs=round((totalDays + (dayNudgeJob-1))/dayNudgeJob)
        #numJobs=(( (totalDays + (dayNudgeJob-1))/dayNudgeJob ))
        #echo "numJobs"


        dayNudge=0
        #dayNudge=8034


        runYear=0

        #nodesIdle=0

        #for ii in range(numJobs):
        for ii in range(1):  # FOR TESTING - JUST RUN ONCE

            #-------------------------------------
            # INDENT HERE ------------------------
            #-------------------------------------

            #ii = 0 # Testing

            dayNudge = ii*dayNudgeJob

            if (dayNudge > cumulativeDaysYearList[runYear]):
                for gg in range(runYear, len(modelDirList)):
                    if (dayNudge > cumulativeDaysYearList[gg]):
                        runYear=((runYear+1))
                    else:
                        break

            startNudgeList=[]
            for jj in range(numRunsPerJob):
                currentNudge = dayNudge + dayNudgeRun*jj
                if (currentNudge + dayNudgeRun - seedSpacing) > lastSeedDay:
                    break
                startNudgeList.append(currentNudge)

            if len(startNudgeList) == 0:
                break


            runYear0=0
            for cumulativeDays in cumulativeDaysYearList:

                if startNudgeList[0] > cumulativeDays:
                    runYear0=runYear0 + 1
                else:
                    break

            runYear=runYear0

            singleDirSwitchList=[]
            jobDirList=[]
            for nudge in startNudgeList:
                if runYear < len(modelDirList):
                    if nudge > cumulativeDaysYearList[runYear]:
                        runYear = runYear+1
                    #print(runYear)
                if runYear+1 == len(modelDirList):
                    singleDirSwitchList.append(1)
                else:
                    singleDirSwitchList.append(0)
                #print(nudge)
                jobDirList.append(modelDirList[runYear])

            #print(jobDirList)
            #print(singleDirSwitchList)



            logString="$(printf %02d ${dtCalc})_$(printf %04d ${dtSave})_$(printf %03d ${bufferLength})_$(printf %02d ${nSeed})_$(printf %02d ${nRuns})_$(printf %06d ${ii})"
            
            #config_file_name = "config_file_nRunsPerNode_{a:02d}_nSeed_{b:02d}_{c:03d}.config.yaml".format(a=numRunsPerJob, b=nSeed, c=ii)
            config_file_name = "nRunsPerNode_{a:02d}_nSeed_{b:02d}_{c:03d}.config.yaml".format(a=numRunsPerJob, b=nSeed, c=ii)

            config_file = config_dir + "/" + config_file_name

#            print(config_file)

            shutil.copyfile(config_template_file, config_file)
                    
            cd = {}

            cd["runCalc"] = dtCalc
            cd["runSave"] = dtSave
            cd["bufferLength"] = bufferLength
            cd["numberOfSeeds"]= nSeed 

            cd["jobDirList"] = jobDirList
            cd["dirListTotal"] = modelDirList 
            
            cd["startNudgeList"] = startNudgeList
            cd["outputDir"] = outputDir


            with open(config_file, 'w') as outfile:
                yaml.dump(cd, outfile, default_flow_style=False)



