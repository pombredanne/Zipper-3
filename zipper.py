#!/usr/bin/python

import os,time,sys

StartGB = 1
EndGB = 100
StartZIP = 1
EndZIP = 10

ZipWith = "|gzip"
SourceFile = "/dev/zero"

UnitSize = "M"

#####

def writeCSV(s,f):
	sys.stdout.write(s)
	fi = open(f, "a+")
	fi.write(s)
	fi.close()

TimeTable = []
StorageTable = []
for t in range(0, (EndGB - StartGB + 1)):
	TimeTable.append([])
	StorageTable.append([])

for size in range(StartGB, EndGB+1):
	for times in range(StartZIP, EndZIP+1):
		FileName = str(size) + UnitSize + "." + str(times) + "T.gz"
		command = "head -c " + str(size) + UnitSize + " " + SourceFile
		command = command + (ZipWith * times)
		command = command + ">" + FileName
		print(command)
		init = time.time()
		os.system(command)
		end = time.time()
		print(" Took: " + str(end - init) + " seconds")
		print(" Size: " + str(os.path.getsize(FileName)) + " bytes")
		TimeTable[size - StartGB].append(end - init)
		StorageTable[size - StartGB].append(os.path.getsize(FileName))

os.system("rm -vfR *.gz > /dev/null 2> /dev/null")

print("Generating Storage CSV File...")
open("size.csv", "w+").close()

writeCSV("X", "size.csv")
for size in range(StartZIP, EndZIP + 1):
	writeCSV("," + str(size) + " Layers", "size.csv")
writeCSV("\n", "size.csv")
InitialLayer = StartGB
for size in StorageTable:
	writeCSV(str(InitialLayer) + " " + UnitSize + "B", "size.csv")
	InitialLayer = InitialLayer + 1
	for layer in size:
		writeCSV("," + str(layer), "size.csv")
	writeCSV("\n", "size.csv")
sys.stdout.flush()

print("Generating Time CSV File...")
open("time.csv", "w+").close()

writeCSV("X", "time.csv")
for size in range(StartZIP, EndZIP + 1):
	writeCSV("," + str(size) + " Layers", "time.csv")
writeCSV("\n", "time.csv")
InitialLayer = StartGB
for size in TimeTable:
	writeCSV(str(InitialLayer) + " " + UnitSize + "B", "time.csv")
	InitialLayer = InitialLayer + 1
	for layer in size:
		writeCSV("," + str(layer), "time.csv")
	writeCSV("\n", "time.csv")
sys.stdout.flush()
