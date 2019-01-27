#==============================================================================
# Program: PictureVerifier.py
# Purpose: Python script prompts user to enter a CSV (containing object ID and
#          image links), and a folder containing "supposedly" corresponding
#          images (idea being that this folder was shared to photo sharing
#          platform). Downloads each image, and compares to "supposedly"
#          #supposedly" corresponding image by calculating differences in
#          histograms. Unfortunately, the quality is degraded after downloading
#          from the web, thus causing images that are the same to have very slight
#          differencs in histograms. Program will show either all differences,
#          outliers (anything higher than mean difference + 1 standard deviation),
#          or anything above a specified threshold.
#
# Created by Liam Gowan, January 27, 2019
#==============================================================================
from PIL import Image
import urllib.request
import requests
import numpy as np
import csv
import os

#downloads image and saves as "testImage.jpg". Saves space by reusing name.
def downloader(imageUrl):
    fileName = "testImage"
    fullFileName = str(fileName) + '.jpg'
    urllib.request.urlretrieve(imageUrl,fullFileName)

#computes difference in histograms for each image
def histoCompare(im1, im2):
    h1 = im1.histogram()
    h2 = im2.histogram()
    sumIm1 = 0.0
    sumIm2 = 0.0
    diff = 0.0
    for i in range(len(h1)):
        sumIm1 += h1[i]
        sumIm2 += h2[i]
        diff += abs(h1[i] - h2[i])
    maxSum = max(sumIm1, sumIm2)
    return(diff/(2*maxSum))

#prints header 
def printHeader():
    print("\nPhoto name" + (" "*16) + "Object ID" + " Difference")
    print("="*25+" "+"="*9+" "+"="*10)

#initialize arrays
ids = []
links = []
reports = []
diffs = []

#prompt user for file/folder names
csvName = input("Enter CSV Name: ")
folderName = input("Enter picture folder name: ")

#open csv and save contents to two separate arrays
with open(csvName) as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    lineCount=0
    for row in csvReader:
        if lineCount>0:
            ids.append(f'{row[0]}')
            links.append(f'{row[1]}')
        lineCount +=1

#prompt user for choice
choice = input("Enter A for all records, O for outliers, or T for above a specified threshold: ")
if(choice=="A" or choice == "T"): #Case: all records or threshold
    if(choice=="T"): #if case=threshold, get threshold value
        threshold = float(input("Enter threshold: "))
    else:            #otherwise just have threshold = 0
        threshold = 0.0
    print("Processing...")
    count=0
    #compare two images, add to reports list if larger than threshold
    for pic in os.listdir(folderName):
        print("Processing image: " + str(count))
        downloader(links[count])
        im1 = Image.open(folderName+"/"+pic)
        im2 = Image.open("testImage.jpg")
        diff = histoCompare(im1,im2)
        if diff >= threshold:
            reports.append("%-25s %-9s %f" % (pic, ids[count],diff))
        count +=1
        
    #print header and all reports above threshold
    printHeader()
    for i in range(len(reports)):
        print(reports[i])

elif(choice=="O"):             #Case: outliers
    print("Processing...")
    count=0
    #compare each image, and append all reports, and all differences
    for pic in os.listdir(folderName):
        print("Processing image: " + str(count))
        downloader(links[count])
        im1 = Image.open(folderName+"/"+pic)
        im2 = Image.open("testImage.jpg")
        diff = histoCompare(im1,im2)
        diffs.append(diff)
        reports.append("%-25s %-9s %f" % (pic, ids[count],diff))
        count +=1

    #calculate average, standard deviation, and upper bound (though only 1 std)
    diffMean=np.mean(diffs)
    diffStd=np.std(diffs)
    upper = diffMean+diffStd

    #print header, and any reports where the difference is greater than upper bound
    printHeader()
    for i in range(len(reports)):
        if(diffs[i]>upper):
            print(reports[i])




