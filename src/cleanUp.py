# ##########################################################################
# 
#   Copyright (C) 2021-2023 stinger81
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   stinger81 - GitHub
#
# ##########################################################################

import os
import time
import shutil
from platform import uname

# directory setup
cleanUpDirName = "cleanUp" # name of the directory to clean up desktop into

exceptionFile = "\\Users\\user\\Download\\Desktop-CLean-Up-Tool\\src\\exceptions.txt" # file containing exceptions

path = "\\Users\\user\\Desktop" # path to the folder to be cleaned up

cleanUpPath = os.path.join(path, cleanUpDirName) # path to the folder to store the cleaned up files

forceIgnore = ["desktop.ini", "Thumbs.db"] # do not remove files can damage the OS


def updateDirOS(inPath:str):
    """
    Update file dir to currnet os
    :param: inPath
    :return: outPath: updated path
    """
    if inPath[0] == "\\":
        outPath = os.path.join(os.sep,*inPath.split("\\")) 
    else:
        outPath = os.path.join(*inPath.split("\\"))
    return outPath
            
def updateToWSL(inpath:str):
    """
    Update the path to WSL
    :param: inpath: path to the dir to build tree from
    :return: outpath: updated path
    """
    outpath = os.sep+"mnt"+os.sep+"c"+inpath
    return outpath

def buildTree(path,level = 0, prevDir = False):
    """
    Recursive functions to build a tree of the files in the directory
    :param: path: path to the dir to build tree from
    :param: level: level of the tree
    :return: string of the tree
    """
    tree = ""
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path,file)):
            if level == 0:
                tree += "\t"*(level)+ file+"\n"
            elif prevDir:
                tree += "\t"*(level-1)+"|-> "+ file+"\n"
                prevDir = False
            else:
                tree += "\t"*(level)+ file+"\n"
            tree += buildTree(os.path.join(path,file),level+1, prevDir=True)
        else:
            if prevDir:
                tree += "\t"*(level-1)+"|-> "+ file+"\n"
                prevDir = False
            else:
                tree += "\t"*(level)+ file+"\n"
    return tree

def updateTree(path):
    """
    Update the tree of the files in the directory
    :param: path: path to the dir to build tree from
    :return: None
    """
    with open(os.path.join(path, "tree.txt"), "w") as f:
        f.write("UPDATED: "+time.strftime("%Y-%m-%d %H:%M:%S")+"\n")
        f.write("TREE:\n")
        f.write(buildTree(path))
        f.close()

def ignoreList():
    """
    Build ignore list
    :param: path: None
    :return: list: exceptions
    """
    exceptions = [cleanUpDirName] # list of exceptions
    ignoreExtensions = []
    # build list of exceptions
    for i in forceIgnore:
        exceptions.append(i)
    with open(exceptionFile, "r") as f:
        for line in f:
            if line[0] == "#":
                continue
            elif line.strip()[-1] == "/":
                exceptions.append(line.strip()[:-1])
            elif line[0] == "*":
                ignoreExtensions.append(line.strip()[1:])
            else:
                exceptions.append(line.strip())
    print("Ignore File(s)/Directory(s): " + str(exceptions))
    print("Ignore Extension(s): "+str(ignoreExtensions))
    return exceptions, ignoreExtensions


if __name__ == "__main__":
    # updates paths from \\ to proper divider for OS
    exceptionFile = updateDirOS(exceptionFile)
    path = updateDirOS(path)
    cleanUpPath = os.path.join(path, cleanUpDirName) # path to the folder to store the cleaned up files

    # WSL support
    if 'microsoft-standard' in uname().release:
        print("WSL Detected - Switching to mnt//c//")
        exceptionFile = updateToWSL(exceptionFile)
        path = updateToWSL(path)
        cleanUpPath = updateToWSL(cleanUpPath)

    
    exceptions,ignoreExtensions  = ignoreList()

    # Check that there are files to clean up
    lenPath = len(os.listdir(path))
    for i in os.listdir(path):
        if i in exceptions:
            lenPath -= 1
        elif os.path.splitext(i)[1] in ignoreExtensions:
            lenPath -= 1
    if lenPath != 0:
        if not os.path.isdir(cleanUpPath):
            print("MKDIR: Making Directory for Clean Up")
            os.makedirs(cleanUpPath)
    else:
        print("INFO: Zero(0) Files Detected to Clean Up")
        print("EXITING WITH CODE 0") # Normal Safe Exit
        exit() # End Program

    # add a date based folder to clean into
    dateFolder = os.path.join(cleanUpPath, time.strftime("%Y_%m_%d_%H_%M_%S"))
    if not os.path.isdir(dateFolder):
        print("MKDIR: Making Directory for Session")
        os.makedirs(dateFolder)
    else:
        print("MKDIR ERROR: Directory Already Exist")
        print("INFO: Updating Tree")
        updateTree(dateFolder)
        print("INFO: Tree update complete")
        print("EXITING WITH CODE 0") # Normal Safe Exit
        exit()

    files = os.listdir(path)
    total = len(files)
    # loop to move files
    for i in range(len(os.listdir(path))):
        if files[i] in exceptions:
            print("SKIPPING: " + str(i+1) + " of " + str(total)+" Skipped File: "+files[i]+" in exception list")
        elif os.path.isdir(os.path.join(path,files[i])):
            shutil.move(os.path.join(path,files[i]), os.path.join(dateFolder,files[i]))
            print("DIRECTORY MOVED: " + str(i+1) + " of " + str(total)+" Current File: " + files[i])
        else:
            if os.path.splitext(files[i])[1] in ignoreExtensions:
                print("SKIPPING: " + str(i+1) + " of " + str(total)+" Skipped File: "+ files[i]+" file type in exception list")
            else:
                os.rename(os.path.join(path, files[i]), os.path.join(dateFolder, files[i]))
                print("FILE MOVED: " + str(i+1) + " of " + str(total)+" Current File: " + files[i])

    # build list of file in cleanUpPath
    updateTree(cleanUpPath)

else:
    print("ERROR: Not Main file")
    print("NOTE: To run automated sequence run;")
    print("__file__: " + __file__)