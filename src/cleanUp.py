import os
import time
import shutil

cleanUpDirName = "cleanUp" # name of the directory to clean up desktop into

exceptionFile = "\\Users\\user\\Download\\Desktop-CLean-Up-Tool\\src\\exceptions.txt" # file containing exceptions

path = "\\Users\\user\\Desktop" # path to the folder to be cleaned up

cleanUpPath = os.path.join(path, cleanUpDirName) # path to the folder to store the cleaned up files

# files to force ignore
forceIgnore = ["desktop.ini", "Thumbs.db"] # do not remove files can damage the OS
exceptions = [cleanUpDirName] # list of exceptions

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
if __name__ == "__main__":
    # build list of exceptions
    for i in forceIgnore:
        exceptions.append(i)
    with open(exceptionFile, "r") as f:
        for line in f:
            if line[0] == "#":
                continue
            exceptions.append(line.strip())
    print("Exceptions: " + str(exceptions))

    # check if cleanUpPath exists
    lenPath = len(os.listdir(path))
    # handles no files to clean up
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

    # date folder
    dateFolder = os.path.join(cleanUpPath, time.strftime("%Y_%m_%d_%H_%M_%S"))
    if not os.path.isdir(dateFolder):
        print("creating date folder")
        os.makedirs(dateFolder)
    else:
        print("date folder already exists")
        print("waiting 1 second")
        time.sleep(1)
        dateFolder = os.path.join(cleanUpPath, time.strftime("%Y_%m_%d_%H_%M_%S"))
        if not os.path.isdir(dateFolder):
            print("creating date folder")
            os.makedirs(dateFolder)
        else:
            print("date folder already exists on try 2 - exiting")
            exit()
    print("date folder: " + dateFolder)

    files = os.listdir(path)
    total = len(files)
    for i in range(len(os.listdir(path))):
        if files[i] in exceptions:
            print("skipping " + files[i]+" in exception list")
            continue
        if os.path.isdir(os.path.join(path,files[i])):
            shutil.move(os.path.join(path,files[i]), os.path.join(dateFolder,files[i]))
        else:
            os.rename(os.path.join(path, files[i]), os.path.join(dateFolder, files[i]))
        print("Files Moved: " + str(i+1) + " of " + str(total)+" Current File: " + files[i])

    # build list of file in cleanUpPath
    updateTree(cleanUpPath)



