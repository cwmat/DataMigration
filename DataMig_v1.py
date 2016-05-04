"""
Repair Broken MXD from Data Migration
POC - chaz.mateer@gmail.com

Python Script that requires the arcpy module.  Created to
walk through a specified directory and its sub-directories.
Searches for ESRI ArcGIS MXD map documents and replaces workspace
paths from a specified path to another.

Variables:
argv[0] = DataMigration_v2.0.py (script name)
argv[1] = *searchDir (root directory that the walk will be initiated at)
argv[2] = *oldDirSeg (path segment that is to be removed)
argv[3] = *newDirSeg (path segment that is to be added)
argv[4] = *textLog (path to a text file that will contain run results)

This version of the script has removed the usage of sys.argv arguements
and has all arguements hard coded.  To run the script simply call it from
the command line as:

> cd path\to\script\directory
> python DataMig_v1.py

"""

# Import modules
import arcpy, os, sys, time, datetime, stat

# Define local variables
searchDir = r"G:\GIS"
oldDirSeg = "P:\\"
newDirSeg = "G:\\"


repairedList = []
mxdList = []

# Start timer
timerStart = time.time()

# Define mxd repair function
def mxdRepair(mxdPath):
	mxd = arcpy.mapping.MapDocument(mxdPath)
	mxd.findAndReplaceWorkspacePaths(oldDirSeg, newDirSeg)
	mxd.save()

# Main function
for (dirPath, dirNames, fileNames) in os.walk(searchDir):
	for fileName in fileNames:
		if dirPath[:11] != r"G:\GIS\DATA":
			if fileName[-4:] == '.mxd':
				fileAtt = os.stat(os.path.join(dirPath, fileName))[0]
				if fileAtt & stat.S_IREAD:
					print os.path.join(dirPath, fileName)
					os.chmod(os.path.join(dirPath, fileName), stat.S_IWRITE)
					mxdRepair(os.path.join(dirPath, fileName))
					os.chmod(os.path.join(dirPath, fileName), stat.S_IREAD)
				else:
					print os.path.join(dirPath, fileName)
					mxdRepair(os.path.join(dirPath, fileName))

# Stop timer
timerStop = time.time()

print "Complete!"
print "Duration: " + str(datetime.timedelta(seconds=timerStop - timerStart))
