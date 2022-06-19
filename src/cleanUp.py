# ##########################################################################
# 
#   Copyright (C) 2021-2022 stinger81
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

def updateDirOS(inPath:str):
    """
    Update file dir to currnet os
    :param: inPath
    :return: outpath: updated path
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

def buildTree(path,level = 0):
    """
    Recursive functions to build a tree of the files in the directory
    :param: path: path to the dir to build tree from
    :param: level: level of the tree
    :return: string of the tree
    """
    tree = ""
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path,file)):
            tree += "\t"*level + file+"\n"
            tree += buildTree(os.path.join(path,file),level+1)
        else:
            tree += "\t"*level + file+"\n"
    return tree
def updateTree(path):
    """
    Update the tree of the files in the directory
    :param: path: path to the dir to build tree from
    :return: None
    """
    with open(os.path.join(path, "tree.txt"), "w") as f:
        f.write("Updated: "+time.strftime("%Y-%m-%d %H:%M:%S")+"\n")
        f.write("Tree:\n")
        f.write(buildTree(path))
        f.close()
if __name__ == "__main__":
    # updates paths from \\ to proper divider for OS
    exceptionFile = updateDirOS(exceptionFile)
    path = updateDirOS(path)
    cleanUpPath = os.path.join(path, cleanUpDirName) # path to the folder to store the cleaned up files

    # WSL support
    if 'microsoft-standard' in uname().release:
        print("WSL detected")
        exceptionFile = updateToWSL(exceptionFile)
        path = updateToWSL(path)
        cleanUpPath = updateToWSL(cleanUpPath)

    # files to force ignore
    forceIgnore = ["desktop.ini", "Thumbs.db"] # do not remove files can damage the OS
    exceptions = [cleanUpDirName] # list of exceptions
    # build list of exceptions
    for i in forceIgnore:
        exceptions.append(i)
    with open(exceptionFile, "r") as f:
        for line in f:
            if line[0] == "#":
                continue
            exceptions.append(line.strip())
    print("Exceptions: " + str(exceptions))

    # Check that there are files to clean up
    lenPath = len(os.listdir(path))
    for i in os.listdir(path):
        if i in exceptions:
            lenPath -= 1
    if lenPath != 0:
        if not os.path.isdir(cleanUpPath):
            print("creating clean up path")
            os.makedirs(cleanUpPath)
    else:
        print("no files to clean up")
        print("updating tree")
        updateTree(cleanUpPath)
        exit()

    # add a date based folder to clean into
    dateFolder = os.path.join(cleanUpPath, time.strftime("%Y_%m_%d_%H_%M_%S"))
    if not os.path.isdir(dateFolder):
        print("creating date folder")
        os.makedirs(dateFolder)
    else:
        print("date folder already exists")
        print("updating tree")
        updateTree(dateFolder)
        print("wait 1 second than rerun")
        exit()

    files = os.listdir(path)
    total = len(files)
    # loop to move files
    for i in range(len(os.listdir(path))):
        if files[i] in exceptions:
            print("skipping " + files[i]+" in exception list")
            continue
        if os.path.isdir(os.path.join(path,files[i])):
            shutil.move(os.path.join(path,files[i]), os.path.join(dateFolder,files[i]))
            print("Dir Moved: " + str(i+1) + " of " + str(total)+" Current File: " + files[i])
        else:
            os.rename(os.path.join(path, files[i]), os.path.join(dateFolder, files[i]))
            print("Files Moved: " + str(i+1) + " of " + str(total)+" Current File: " + files[i])

    # build list of file in cleanUpPath
    updateTree(cleanUpPath)

else:
    print("not main file ")
    print("to use full functions please run this file")
    print("__file__: " + __file__)


