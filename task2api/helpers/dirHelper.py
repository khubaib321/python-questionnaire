import os
import json
from collections import OrderedDict


def ensureDirectoryExist(relative_path):
    absolutePath = getFullPath(relative_path)
    if not os.path.exists(absolutePath):
        os.makedirs(absolutePath, exist_ok=True)


def getFullPath(relativePath):
    fileDir = os.path.dirname(__file__)
    absolutePath = os.path.join(fileDir, relativePath)
    return absolutePath


def readDataFromJsonFile(relativePath):
    data = {}
    fullPath = getFullPath(relativePath)
    try:
        with open(fullPath, 'r') as file:
            data = json.load(file, object_pairs_hook=OrderedDict)
    except IOError:
        print("Could not open file for reading: '" + relativePath + "'")
    return data


def writeDataToJsonFile(relativePath, data, checkExisting):
    fullPath = getFullPath(relativePath)
    if checkExisting:
        try:
            with open(fullPath, 'r') as file:
                pass
        except IOError:
            print("Could not open file for reading: '" + relativePath + "'")
            return
    try:
        with open(fullPath, 'w') as file:
            file.write(json.dumps(data))
    except IOError:
        print("Could not open file for writing: '" + relativePath + "'")
