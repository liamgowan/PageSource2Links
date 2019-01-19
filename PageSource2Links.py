#==============================================================================
# Program: PageSource2Links.py
# Purpose: At the time of coding, this short script was designed to extract a
#          list of links of pictures in a shared Google Photos album. A very
#          specific string of text must be copy and pasted from your album
#          to a text file called "pagesource.txt". Results will be printed in
#          shell
#
# Created by Liam Gowan, January 19, 2019
#==============================================================================

#open text file, initialize array to hold all links
infile = open("pagesource.txt","r")
allLinks = []

print ("Processing...\n\n")

#read lines, extract data
line = infile.readline()
while line != "":
    if("https://lh3.googleusercontent.com" in line): #Assess line validity
        allLinks.append(line[51:223]) #append where the needed text for link is
    line = infile.readline()
infile.close()

#print all results to shell
print("RESULTS: \n")
for i in range(len(allLinks)):
    print (allLinks[i])
