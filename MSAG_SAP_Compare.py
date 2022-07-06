import arcpy
import csv

structures = "C:\Users\chris.robinson\Desktop\Site_Address_Points"
structureFields = [ "add_number", "st_predir","st_name","st_postyp","st_posdir", "ESN"]

msag = "C:\Users\chris.robinson\Desktop\SecondRun_Final.gdb\MSAG"
msagFields = ["dir", "street", "low", "high", "o_e","community", "esn"]

csvfile = "C:\Users\chris.robinson\Desktop\MSAG_Compare.csv"

myfile = csv.writer(open(csvfile, "wb"))  

print "Building MSAG List"
msagDict = {}
##msagDict Structures {"W MAIN ST":[[LOW,HIGH,oE],[LOW,HIGH,oE]]}
with arcpy.da.SearchCursor(msag, msagFields) as msagSearchCursor:
    for row in msagSearchCursor:
        roadName = str(str(row[msagFields.index("dir")]) + " " + str(row[msagFields.index("street")]))
        oE = row[msagFields.index("o_e")]
        try:
            LOW = (int(row[msagFields.index("low")]))
        except:
            LOW = None
        try:
            HIGH = (int(row[msagFields.index("high")]))
        except:
            HIGH = None
        if roadName in msagDict:
            msagDict[roadName].append([LOW, HIGH, oE])
        else:
            msagDict[roadName] = []
            msagDict[roadName].append([LOW, HIGH, oE])

print "Scanning Structures"
totalStructures = arcpy.GetCount_management(structures).getOutput(0)
with arcpy.da.SearchCursor(structures, structureFields) as structuresSearchCursor:
    unmatchedAddresses = []
    for currentStructure in structuresSearchCursor:
        currentStructureRoadName = (str(currentStructure[structureFields.index("st_predir")]) + " " + str(currentStructure[structureFields.index("st_name")]) + " " + str(currentStructure[structureFields.index("st_postyp")]))
        currentStructureNumber = currentStructure[structureFields.index("add_number")]
        try:
            currentStructureNumber = int(currentStructureNumber)
            if currentStructureNumber % 2 == 0:
                currentStructureNumberEO = "EVEN"
            else:
                currentStructureNumberEO = "ODD"            
        except:
            currentStructureNumber = None
            currentStructureNumberEO = None
        if currentStructureNumber == None:
            continue
        addressFound = False      
        if currentStructureRoadName in msagDict:            
            for msagRow in msagDict[currentStructureRoadName]:
                if (currentStructureNumber >= msagRow[0] and currentStructureNumber <= msagRow[1]):
                    if (msagRow[2] == "BOTH") or (msagRow[2] == currentStructureNumberEO):
                        addressFound = True                        
                        break
        if not addressFound:
            unmatchedAddresses.append((currentStructureNumber,currentStructureRoadName))
    sortedAddresses = sorted(unmatchedAddresses,key=lambda x:(x[1],x[0]))
	
with open(csvfile, "wb") as myfile:
	wr = csv.writer(myfile)
	for address in sortedAddresses:
		wr.writerow([str(address[0]) + " " + address[1]])
        

print "Done"
