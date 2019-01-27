#==============================================================================
# Program: JSON2Links.py
# Purpose: At the time of coding, this short script was designed to extract a
#          list of links of pictures in a shared Google Photos album. A very
#          specific string of text must be copy and pasted from your album
#          to a text file called "pagesource.txt". Results will be printed in
#          shell
#
# Created by Liam Gowan, January 27, 2019
#==============================================================================

import json

pageSource = open("pagesource.txt","r") 
jsonData = json.load(pageSource) #read data in as JSON
for item in jsonData: #print each link
    print(item[1][0])
pageSource.close() 

