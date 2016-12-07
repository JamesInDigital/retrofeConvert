#enables utf-8 even though commented out
# -*- coding: utf-8 -*-.
##TODO
##	How to handle ?? and specials during Game Name Set (literal strings?) (may not be necessary, bypassed in MAME set where issue was)
##  Convert "Score" to appropriate Star Rating for Retrofe/Hyperspin
##WISHLIST
## Drag n' Drop xml to UI Automation
## Field check boxes to retain user data
##	ie. Uncheck publisher, or cloneof if user wishes to keep existing data
##  this is more for an "update" when a new gamelist.xml is pulled and the
##  user wishes to take name information into hyperspin format without losing
##  any of their own changes... seems uneeded and complicated
## Automatically put into retrofe structure - probably not a good idea
## as users can customize collection names/structure to a degree 

#import libraries - ElemenTree parses XML data
import xml.etree.ElementTree as ET
import os
import re
import shutil
import time
import sys
os.system('cls') # for windows

#define global variables so that they can be used inside/outside functions?
global currentdir
global xmlfilename
global newfilename
global systemType
global convertedfilename
global enabledfilename
global fixedFilename
global finalFilename
global currentTime

#prompt user for filename and sytem type
xmlfilename = raw_input("Name of your xml file :  ")
#system type defines how the game name data is pulled ie console vs mame
systemType = raw_input("What system is this list for (ex: Nintendo Entertainment System): ")
#these define time and current file directory	
currentTime = time.asctime( time.localtime(time.time()) )
currentdir = os.getcwd()

#these define basic values for the the filename variables created as globals
newfilename = ('New_' + xmlfilename)
convertedfilename = ('Converted_' + newfilename)
enabledfilename = ('Enable_' + convertedfilename)
fixedFilename = ('Fixed_' + enabledfilename)
finalFilename = ('Converted_' + xmlfilename)


#main function which calls all sub functions
def Main():
	fixGameName()
	extractStoryDesc()
	convertGameList()
	removeElements()
	correctAttributes()
	addElements()
	setYes()
	fixYear()
	cleanUp()
	time.sleep(5)
	sys.exit()	

#fixes any issues with the game name by using the full file name in most cases
def fixGameName():
	print "\n\nFixing Game name fields as needed...\n\n"
	#parse xml, find root element
	tree = ET.parse(xmlfilename)
	root = tree.getroot()
	#define new output file to be created
	outfile = open(currentdir + "\\" + 'New_' + xmlfilename, 'w')
	#use the currently open xml file to find the following data
	with open(xmlfilename,'r') as fix:
		for line in fix:
			if "<path>" in line:
				#splits the path element
				path_value = re.split('<|>',line)[2]
				#trims two character extension off of filename
				if '.7z' in path_value:
					new_path = path_value[2:-3]
				#trims three character extension off of filename
				else:
					new_path = path_value[2:-4]
				#replace the line with the new value created
				line = line.replace(path_value, new_path)
			#writes output file and then closes
			outfile.write(line)
		outfile.close()
		print "\nName fields fixing completed.\n"

#extracts the story element as a text file based on the game name		
def extractStoryDesc():
	print "\n\nExtracting Story Files...\n\n"
	storydir = (currentdir +"\\story\\")
	#if the subdirectory 'story' doesn't exist, creates it
	if not os.path.exists('story'):
		os.makedirs('story')
	tree = ET.parse(xmlfilename)
	root = tree.getroot()
	#find the element 'game'
	for game in root.findall('game'):
		#define textstring based on the 'path' element found within 'game'
		storyname = game.find('path').text
		if '.7z' in storyname:
			newstoryname = storyname[2:-3]
		else:
			newstoryname = storyname[2:-4]
		#create variable with the 'desc' field text content
		storytext = game.find('desc').text
		#take textstring and give extension
		storyfile = (newstoryname +"."+"txt")
		#with our new file open write out the contents, close and move to subdir
		with open(storyfile, "w") as text_file:
			text_file.write("%s" % storytext)
			text_file.close()
			shutil.move(os.path.join(currentdir, storyfile), os.path.join(storydir, storyfile))
	print "\nFiles extracted into subfolder 'story' in source directory.\n"


	
#beginning actual data "conversion" formatting
def convertGameList():
	print "\n\nRenaming Fields...\n\n"
	tree = ET.parse(newfilename)
	root = tree.getroot()
	#define out new file
	convertedOutfile = open(currentdir + "\\" + 'Converted_' + newfilename, 'w')
	with open(newfilename,'r') as convert:
		#hacky way of replacing data - find every item in if statment and replace line with new data
		for line in convert:
			if "<gameList>" in line:
				line = line.replace('<gameList>', '<menu>')
			if "<game id=" in line:
				line = line.replace('<game id=', '<game name=')
			#if "source=\"mamedb.com\">" in line:
			#	line = line.replace('source=\"mamedb.com\">', 'index=\"true\">')
			if "<publisher>" in line:
				line = line.replace('<publisher>', '<manufacturer>')
			if "<releasedate>" in line:
				line = line.replace('<releasedate>', '<year>')
			if "<rating>" in line:
				line = line.replace('<rating>', '<score>')
			if "<name>" in line:
				line = line.replace('<name>', '<description>')
			if "</gameList>" in line:
				line = line.replace('</gameList>', '</menu>')
			if "</publisher>" in line:
				line = line.replace('</publisher>', '</manufacturer>')
			if "</releasedate>" in line:
				line = line.replace('</releasedate>', '</year>')
			if "</rating>" in line:
				line = line.replace('</rating>', '</score>')
			if "</name>" in line:
				line = line.replace('</name>', '</description>')
			convertedOutfile.write(line)
	convertedOutfile.close()
	print "\nFields renamed.\n"

#removes unneeded elements
def removeElements():
	print "\n\nRemoving unneeded fields...\n\n"
	tree = ET.parse(convertedfilename)
	root = tree.getroot()
	gameElement = tree.findall('game')
	#remove desc as is no longer needed
	for game in gameElement:
		descElement = game.findall('desc')
		for desc in descElement:
			game.remove(desc)
	#remove image element as RetroFe doesn't use it
	for game in gameElement:
		imageElement = game.findall('image')
		for image in imageElement:
			game.remove(image)
	tree.write(convertedfilename)
	print "\nFields removed.\n"

#fixing sub-element attribs of 'game'	
def correctAttributes():
	print "\n\nAdding and Removing Game attributes...\n\n"
	tree = ET.parse(convertedfilename)
	root = tree.getroot()
	#for every game element fill attributes with new data and del source attrib
	for game in root.findall('game'):
		game.set('image', "1")
		game.set('index', "true")
		del game.attrib["source"]
	tree.write(convertedfilename)
	print "\nAttributes complete.\n"

#add new elements needed
def addElements():
	print "\n\nAdding enabled element and setting to yes...\n\n"
	tree = ET.parse(convertedfilename)
	root = tree.getroot()
	#create enabled attribute
	for game in root.findall('game'):
		enabled = ET.SubElement(game, 'enabled')
	#html output method correctly closes elements like html tags <tag></tag>
	tree.write(convertedfilename, method='html')

#hacky way of setting enabled element to yes - Fix this with better method
def setYes():
	enabledOutfile = open(currentdir + "\\" + 'Enable_' + convertedfilename, 'w')
	with open(convertedfilename,'r') as enable:
		for line in enable:
			if "<enabled></enabled></game>" in line:
				line = line.replace('<enabled></enabled></game>', '<enabled>Yes</enabled>\n\t  </game>')
			enabledOutfile.write(line)
		enabledOutfile.close()
		print "\nElement created and set.\n"

#take the long date/year string and properly format
def fixYear():
	print "\n\nCorrecting the Year format...\n\n"
	tree = ET.parse(enabledfilename)
	root = tree.getroot()
	fixedOutfile = open(currentdir + "\\" + 'Fixed_' + enabledfilename, 'w')
	with open(enabledfilename,'r') as fixyear:
		for line in fixyear:
			if "<year>" in line:
				#split the year element
				year_value = re.split('<|>',line)[2]
				#if no value exists move to next entry
				if year_value is '':
					pass
				#if year value is longer than 4 digits ie 1989 format correctly.
				elif len(year_value) > 4:
					fouryear_value = year_value[:4]
					month_value = year_value[4:6]
					day_value = year_value[6:8]
					final_year = (fouryear_value+"/"+month_value+"/"+day_value)
					line = line.replace(year_value, final_year)
				#if year is a four-digit then pass to file
				else:
					fouryear_value = year_value[:4]
					line = line.replace(year_value, fouryear_value)
			fixedOutfile.write(line)
		fixedOutfile.close()
		print "Formatting complete.\n"

#start cleaning up remaining data		
def cleanUp():
	print "\n\nPerforming final cleanup...\n\n"
	finalOutfile = open(currentdir + "\\" + 'Converted_' + xmlfilename, 'w')
	with open(fixedFilename, 'r') as final:
		for line in final:
			#hacky hack hack for inserting some header data identification - not used in prog
			if "<menu>" in line:
				line = line.replace('<menu>', '<menu>\n\t  <header>\n\t\t  <listname>'+systemType+'</listname>\n\t\t  <listconversiondate>'+currentTime+'</listconversiondate>\n\t\t  <converterversion>sselph gamelist.xml to retrofe hyperspin-style.xml GameListConver v0.9 for MAME/Arcade by James Schumacher http://www.jamesindigital.com</converterversion>\n\t  </header>')
			finalOutfile.write(line)
		finalOutfile.close()
	os.remove(fixedFilename)
	os.remove(enabledfilename)
	os.remove(convertedfilename)
	os.remove(newfilename)
	#check systemType for different final cleanup methods
	if not (systemType.lower() == "mame" or systemType.lower() == "arcade" or systemType.lower() == "nintendo ds" or systemType.lower() == "intellivision" or systemType.lower() == "mattel intellivision"):
		final_cleanUp()
	else:
		more_cleanUp()

#final cleanup for arcade style xml data where filename is diff than game title, or game title has special chars
def final_cleanUp():
	tree = ET.parse(finalFilename)
	root = tree.getroot()
	gameElement = tree.findall('game')
	for game in root.findall('game'):
		new_id = game.find('description').text
		del game.attrib["name"]
		game.set('name', new_id)
	for game in gameElement:
		pathElement = game.findall('path')
		for path in pathElement:
			game.remove(path)
	tree.write(finalFilename, method='html')
	os.rename(finalFilename, systemType+'.xml')
	print "\nCleanup complete.\n Let me know if this works for you on the RetroFe Forums."

#cleanup for standard filename/gamename crossover	
def more_cleanUp():
	tree = ET.parse(finalFilename)
	root = tree.getroot()
	gameElement = tree.findall('game')
	for game in root.findall('game'):
		new_id = game.find('path').text
		del game.attrib["name"]
		game.set('name', new_id)
	for game in gameElement:
		pathElement = game.findall('path')
		for path in pathElement:
			game.remove(path)
	tree.write(finalFilename, method='html')
	os.rename(finalFilename, systemType+'.xml')
	print "\nCleanup complete.\n Let me know if this works for you on the RetroFe Forums."
	
Main()