import DirectoryHandling as dh
# from  DirectoryHandling import dirHandling as dh
import numpy as np
import pandas as pd
import shutil as sh
import os

# csvFile = pd.read_csv("File_Extensions.csv")
# image_ext = pd.Series(csvFile['image'])
# word_ext = csvFile['word']
# exe_ext = csvFile['executable']
# excel_ext = csvFile['excel']
# pdf_ext = pd.Series(csvFile['pdf'])
# # pdf_ext = pdf_ext.replace(to_replace= np.nan , value='')
# valid_files = {'pdf': pdf_ext,
#                 "word": word_ext
#               }
# csvFile = pd.read_csv("File_Extensions.csv")
# cols = np.array(csvFile.columns)
# print(cols)
#
# files_ext_df = pd.DataFrame(csvFile, columns=cols)
# files_ext_df = files_ext_df.replace(to_replace=np.nan, value='')
# print(files_ext_df.head())
# for col in cols:
#     for ext in files_ext_df[col]:
#         if ext == '':
#             continue
#         print(ext, col)
#
"""testin to get all files from a directory in a list"""

# path = 'D:/Bahria/fyp project works/testFiles'
files = []
# r=root, d=directories, f = files

#########################################
testDH = dh.dirHandling()

username = input('Enter Username: ')
rootDir = testDH.getRootDir(userName=username) #call this function on succesfull login
print(rootDir)
while(True):
    print(testDH.getAllFolders())
    ifUpload = input('Want to upload files? (y/n) ')
    if ifUpload == 'y':
        path = input('Enter path to upload files from:\n')

        testDH.bulkUpload(path)
        # for r, d, f in os.walk(path):
        #     for file in f:
        #         files.append(os.path.join(r, file))
        #         # files.append(file)
        #     break
        # for f in files:
        #     print(f)

        # for file in files:
        #     print(testDH.uploadFile(file))
    folder = input('which folder you want to preview files from? ')

    """ to preview files or directories from root folder pass (.) in path """

    print('files: ',testDH.getAllFilesInAFolder_deep(folder=folder))
    print('dirs: ',testDH.getAllFoldersInAFolder_deep(folder=folder))
    isExit = input('Continue? (y/n): ')
    if isExit == 'n':
        break

# div = testDH.getFolderName('.txt')
# print(div)
# #
# # file = 'D:\\Bahria\\fyp project works\\notes.txt'
#
# ext = os.path.splitext(file)[1]
# print(ext)
# file = 'C:\\Users\sajja\\OneDrive\\Pictures\\Screenshots\\Capture.jpg'
# print(testDH.uploadFile(file))
#########################################


#
# path = dh.getCurrentDirectory() + '\\Dynamic Folder\\nestedFolder'
# # path = dh.getCurrentDirectory() + '\\root'
#
# # dh.createFolder(path)
#
# dh.copy2(file)
#
# print(path)
# print(dh.getRootDir())
# print(dh.isFile(path))
