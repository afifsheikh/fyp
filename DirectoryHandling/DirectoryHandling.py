"""
''''''''''''''''''''''''''''''
to run make changes in main function in the last
''''''''''''''''''''''''''''''
"""

import os
# from builtins import print

import numpy as np
import pandas as pd
import shutil as sh



class dirHandling:

    def __init__(self):
        self.csvFile = pd.read_csv(os.getcwd()+"/DirectoryHandling/File_Extensions.csv")
        self.files_ext_df = pd.DataFrame(self.csvFile)
        self.cols = np.array(self.csvFile.columns)
        self.rootdir = ''

    def setCsvFile(self, file):
        self.csvFile = pd.read_csv(file)
        self.files_ext_df = pd.DataFrame(self.csvFile)
        self.cols = np.array(self.csvFile.columns)

    def getCsvFile(self):
        return self.csvFile

    def createFolder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def getCurrentDirectory(self):
        return os.getcwd()

    def getRootDir(self, userName):
        """also creates the designated root folder with the name of the given username"""
        self.rootdir = os.getcwd() + '/Users/root_' + userName;
        self.createFolder(self.rootdir)
        return self.rootdir

    def isFile(self, path):
        return os.path.exists(path=path)

    def uploadFile(self, file):
        if os.path.isfile(file):
            self.copyFile(file)
            return 'File Uploaded'
        else:
            return 'invalid file'

    def getDestinationPath(self, file):
        ext = os.path.splitext(file)[1].lower()
        folderName = self.getFolderName(ext=ext)
        path = self.rootdir + '/' + folderName
        self.createFolder(path=path)
        return path
    

    def copyFile(self, file):
        ext = os.path.splitext(file)[1].lower()
        fileName = os.path.splitext(file)[0]
        folderName = self.getFolderName(ext=ext)
        path = self.rootdir + '/' + folderName
        self.createFolder(path=path)
        sh.copy2(file, path)

    def getFolderName(self, ext):
        for col in self.cols:
            for e in self.files_ext_df[col]:
                if e == '':
                    continue
                if e == ext:
                    return col
            # print(e, col)
        return 'others'

    def bulkUpload(self, path):
        files = []
        for r, d, f in os.walk(path):
            for file in f:
                files.append(os.path.join(r, file))
            break
        for file in files:
            print(f'{file},{self.uploadFile(file)}')

    def deepBulkUpload(self, path):
        files = []
        for r, d, f in os.walk(path):
            for file in f:
                files.append(os.path.join(r, file))
        for file in files:
            print(f'{file},{self.uploadFile(file)}')

    def getAllFilesInAFolder(self, folder):
        """pass a path to a folder and get a list of all the files in the folder"""
        files = []
        path = self.rootdir + '/'+folder
        if not os.path.exists(path):
            return files
        for r, d, f in os.walk(path):
            for file in f:
                files.append(file)
            break
        return files

    def getAllFilesInAFolder_deep(self, folder):
        """pass a path to a folder and get a list of all the files and sub-files in the folder"""
        files = []
        path = self.rootdir + '/'+folder
        if not os.path.exists(path):
            return files
        for r, d, f in os.walk(path):
            for file in f:
                files.append(file)
        return files

    def getAllFoldersInAFolder(self, folder):
        """pass a path to a folder and get a list of all the folders in the folder"""
        dirs = []
        path = self.rootdir + '/'+folder
        if not os.path.exists(path):
            return dirs
        for r, d, f in os.walk(path):
            for _dir in d:
                dirs.append(_dir)
            break
        return dirs

    def getAllFoldersInAFolder_deep(self, folder):
        """pass a path to a folder and get a list of all the folders and sub-folders in the folder"""
        dirs = []
        path = self.rootdir + '/'+folder
        if not os.path.exists(path):
            return dirs
        for r, d, f in os.walk(path):
            for _dir in d:
                dirs.append(_dir)
        return dirs

    def getAllFolders(self):
        folders = []
        for r, d, f in os.walk(self.rootdir):
            for folder in d:
                dr = r
                dirName = dr.replace(self.rootdir, '').replace('\\','/')
                folders.append(dirName + '/' + folder)
        return folders

    def validateFile(self, file):
        ext = os.path.splitext(file)[1].lower()
        fileName = os.path.splitext(file)[0]
        if os.path.splitext(fileName)[1].lower() == "":
            return True
        return False
        
# def mics(ext):
# 	# print(word_list)
# 	print(ext)
# 	for e in word_list:
# 		if ext.lower() == e:
# 			print('founded', ext)
# 	# for m in word_list:
# 	print(m)
#
# def findExt(ext):
# 	for p in valid_files:
# 		# ext = os.path.splitext(file)[1]
# 		if ext.lower() in valid_files[p]:
# 			print('found', ext, p)
#
# def temp(path):
# 	for f in os.listdir(path):
# 		ext = os.path.splitext(f)[1]
# 		# fileName = os.path.splitext(f)[0]
# 		findExt(ext)
# 		# if ext.lower() not in valid_images:
# 		# 	continue
#
#
#
# def main():
# 	# temp(path)
# 	mics('.doc')
# 	# print(word_ext)
# 	# print(valid_files)
#
# main()
