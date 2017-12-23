#instructions:
#currently  (11/27/2017) the set up works this way:
#(see instructions.txt located in the same directory as this program)

#CONCERNS
#This one works correctly
#only concern is the sort order
#also expiration or active column includes No warranty data
#also moves file to footprints server

#To Do:
#todo:
#Think of finding out something in Kace that to get a list of all of the available databases...maybe emailthe Kace guy.
# I also added some other databases as they appear to have been added in....I will ask which of these need to stay
#the following org11 and org12 passwords don't seem to work...not 100% sure if it was the pasword...i can check...but I think that's what it wsa.
    #cblPathInfo = ("CBLPath",'R10','ORG10')
    #escLabInfo = ("ESCLab",'R11','ORG11')
    #smlInfo = ("SML",'R12','ORG12')    

#Important notes:
# 12/16/2017: I removed the database SonicCorpSOEInfo from consideration as it appears to have been taken out of Kace
# I also added some other databases as they appear to have been added in....I will ask which of these need to stay
import csv
import datetime
import time
import re

#new
#import win32wnet
import shutil
import os

import mysql.connector
#from python_mysql_dbconfig import read_db_config


#finished 11/27/2107 8:40am...works good...in everything.

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
dellTableList = []
footprintsExportList = []
def storeCSVAsList(fileName,outputList):
    del outputList[:]
    with open(fileName,'r') as f:
        csv_f = csv.reader(f)
        for row in csv_f:
#            oneRowList = row[:]
            outputList.append(row)

def writeTestListToCSV(listToWrite, outputFile):
    with open(outputFile,"w", newline = '') as csv_file2:
        writer = csv.writer(csv_file2, delimiter=',')
        for line in listToWrite:
            writer.writerow(line)   

def findInVendorOrFFTables(stringInput, totalList, approvedList, mode):
    """
    This function assumes that totalList and approvedList are in synch with each other
    if something is found in one of the lists in the totalList table then we will use the
    entry in approvedList which is in the same index as totalList.
    If something is found in the first list then it will return the corresponding one in the "approved" list.
    If it's not found then it will return an empty string.

    Also if mode = "exact" then we search for an exact match
    if mode = "contains" then we search if stringInput contains any of the strings in totalList
    If incorrect mode is specified then it returns ""
    """
    totalListTemp = []
    approvedListTemp = []
    approvedEntry = ""
    totalListTemp = list(totalList)
    approvedListTemp = list(approvedList)
    substringPosition = -1


    if mode.lower() == "exact":
        if mode.lower() == "exact":
            for j in range(0,len(totalListTemp)):
                for k in range(0,len(totalListTemp[j])):
                    if stringInput.lower() == totalListTemp[j][k].lower():
                        return approvedList[j]
            return ""

    elif mode.lower() == "contains":
        for j in range(0,len(totalListTemp)):
            for k in range(0,len(totalListTemp[j])):
                substringPosition = stringInput.lower().find(totalListTemp[j][k].lower())
                if substringPosition != -1:
                    return approvedList[j]
        return ""

    else:
        return ""
    
#///////////////////////////////////////////////////////////////////////////

    

vendorNameToUse = ""

#///////////////////////////////////////////////////////////////////////////
'''
def processModelNameColumn():
    #abc123
    vendorNameInKace = ""
    somethingInVendorColumnFlag = 0
    substringLength = 0
    substringPosition = 0
    detailsInKace = ""
    tempList = []
    tempList.clear()
    vendorInDetailsModifiedFlag = 0
    vendorInVendorList = ""         #will remain "" if vendor in kace not found in our vendor list.
    for i in range(0,len(footprintsExportList)):
        detailsInKace = footprintsExportList[i][formFactorFootprintsColumn]
        if len(footprintsExportList[i][vendorFootprintsColumn]) != 0:
            vendorNameInKace = footprintsExportList[i][vendorFootprintsColumn]
            somethingInVendorColumnFlag = 1
            vendorInVendorList = findInVendorOrFFTables(vendorNameInKace,vendorList,approvedVendorList,"exact")
        if somethingInVendorColumnFlag == 0:
            if len(detailsInKace) == 0:
                pass #do nothing
            else:
                vendorInVendorList = findInVendorOrFFTables(detailsInKace,vendorList,approvedVendorList,"contains") == ""
                if vendorInVendorList == "":
                    pass #do nothing
                else:
                    putVendorIntoDetails(vendorInVendorList)
                    stick vendorinvendorlist into details of footprintsexport
                    first if any of those in vendorlist ar ein there and take them out.

        else:
            if len(detailsInKace) != 0:

                for j in range(0,len(vendorList)):
                    for k in range(0,len(vendorList[j])):
                        substringPosition = vendorNameInKace.lower().find(vendorList[j][k].lower())
                        if substringPosition != -1:
                            break
                    if substringPosition != -1:
                        break
                    

                if substringPosition != -1:
                    substringPosition2 = 0
                    substringLength2 = 0
                    for j in range(0,len(vendorList)):
                        for k in range(0,len(vendorList[j])):
                            substringPosition2 = detailsInKace.lower().find(vendorList[j][k].lower())
                            if substringPosition2 != -1:
                                substringLength2 = len(vendorList[j][k])
                                break
                        if substringPosition2 != -1:
                            break

                    if substringPosition2 != -1:
                        #SUBSTITUTE STUFF IN (by taking out vendor out of the details and putting into the beginning.
                        putVendorIntoDetails(vendorList[j][k],i,j,k,substringPosition2)
                    else:
                        putVendorIntoDetails(vendorList[j][k],i,j,k,substringPosition2)
                else:
                    pass
'''
#///////////////////////////////////////////////////////////////////////////
def processVendorHalf():
    print("here 2") #debug
    vendorColumnNotEmpty = 0
    ffColumnNotEmpty = 0
    vendorCFoundInList = 0
    ffCFoundInList = 0
    vendorInListOuterIndex = 0
    ffInListOuterIndex = 0
    vendorInListInnerIndex = 0
    ffInListInnerIndex = 0    
    substringPositiont = -1
    stringInVendorColumn = ""
    stringInDetailsColumn = ""


    for i in range(0,len(footprintsExportList)):   #main loop for entire function
        #debug
        #print("here 3") 

        stringInVendorColumn = footprintsExportList[i][vendorFootprintsColumn]
        stringInDetailsColumn = footprintsExportList[i][formFactorFootprintsColumn]
        #print(stringInVendorColumn) #debug
        #print(stringInDetailsColumn) #debug

        #Set emptiness variable
        if footprintsExportList[i][vendorFootprintsColumn] == "":
            vendorColumnNotEmpty = 0
        if footprintsExportList[i][formFactorFootprintsColumn] == "":
            ffColumnNotEmpty = 0

        #see if vendor column contains anything in the vendor list and set appropriate variables accordingly
        if vendorColumnNotEmpty != 0:
            print("a1")#debug
            for j in range(0,len(vendorList)):
                for k in range(0,len(vendorList[j])):
                    substringPosition = stringInVendorColumn.lower().find(vendorList[j][k].lower())
                    if substringPosition != -1:
                        vendorCFoundInList = 1
                        vendorInListOuterIndex = j
                        vendorInListInnerIndex = k
                        print("a3")#debug
                        break
                if substringPosition != -1:
                    break
        #see if details contains anything in the vendor list
        if ffColumnNotEmpty != 0:
            print("a2")#debug
            for j in range(0,len(vendorList)):
                for k in range(0,len(vendorList[j])):
                    substringPosition = stringInDetailsColumn.lower().find(vendorList[j][k].lower())
                    if substringPosition != -1:
                        ffCFoundInList = 1
                        ffInListOuterIndex = j
                        ffInListInnerIndex = k
                        print("a4")#debug
                        break
                if substringPosition != -1:
                    break

        if vendorColumnNotEmpty == 0 and ffColumnNotEmpty == 0:
            print("a5")#debug
            pass        #do nothing....we need to exit the function

        elif vendorColumnNotEmpty ==0 and ffColumnNotEmpty != 0:
            if ffCFoundInList == 0:
                print("a6")#debug
                pass    #do nothing....we need to exit the function
            else:
                replaceVendorStrings(vendorApprovedList[ffInListOuterIndex], vendorList[ffInListOuterIndex][ffInListInnerIndex], i)
                print("a7")#debug

        elif vendorColumnNotEmpty !=0 and ffColumnNotEmpty == 0:
            if vendorCFoundInList == 0:
                footprintsExportList[i][formFactorFootprintsColumn] = stringInVendorColumn
                print("I made it here 1") #debug
            else:
                footprintsExportList[i][formFactorFootprintsColumn] = vendorApprovedList[vendorInListOuterIndex]
                print("here 5") #debug

    
        elif vendorColumnNotEmpty !=0 and ffColumnNotEmpty != 0:
            if vendorCFoundInList == 0 and ffCFoundInList == 0:
                print("a8")#debug
                pass    #do nothing...we need to exit the function
            elif vendorCFoundInList != 0 and ffCFoundInList == 0:
                print("a9")#debug
                replaceVendorStrings(vendorApprovedList[vendorInListOuterIndex], "", i)
            elif vendorCFoundInList == 0 and ffCFoundInList != 0:
                print("a10")#debug
                replaceVendorStrings(vendorApprovedList[ffInListOuterIndex], vendorList[ffInListOuterIndex][ffInListInnerIndex], i)
            elif vendorCFoundInList != 0 and ffCFoundInList != 0:
                print("a11")#debug
                replaceVendorStrings(vendorApprovedList[vendorInListOuterIndex], vendorList[ffInListOuterIndex][ffInListInnerIndex], i)

#///////////////////////////////////////////////////////////////////////////
def replaceVendorStrings(stringToUse, stringToReplace, footprintsListIndex):
    '''
    This function puts stringToUse  at the beginning of the string.
    If stringToReplace exists in the string then it will take it out before adding in stringToUse
    It is mindful of including a space to separate it and what word woudl be after it
    If what is after it is a whitespace then it won't add a space there.
    Regular expressions are used as it's the only way to replace strings in a case insensitive way
    '''
    print("here replacevendorstrings") #debug
    tempString = ""
    footprintsTemp = ""
    if stringToReplace == "":
        if len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) == 0:
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToUse
        else:
            if footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][0].isspace():
                tempString = stringToUse
            else:
                tempString = stringToUse + " "
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = tempString + footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]
                
    elif len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) == 0:
        footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToUse

    else:
        tempString = ""
        substringPosition = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn].upper().find(stringToReplace.upper())
        if substringPosition != -1:
            footprintsTemp = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]
            redata = re.compile(re.escape(stringToReplace), re.IGNORECASE)
            footprintsTemp = redata.sub('', footprintsTemp)
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsTemp
#            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn].replace((stringToReplace), '', 1)

        if len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) == 0:
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToUse
            tempString = ""
        elif footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][0].isspace():
            tempString = stringToUse
        else:
            tempString = stringToUse + " "
        footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = tempString + footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]

                            
#///////////////////////////////////////////////////////////////////////////

def replaceFFStrings(stringToUse, stringToReplace, footprintsListIndex):
    '''
    This function puts stringToUse  at the end of the string.
    If stringToReplace exists in the string then it will take it out before adding in stringToUse
    It is mindful of including a space to separate it and what word woudl be in before it
    If what is before is a whitespace then it won't add a space there.
    Regular expressions are used as it's the only way to replace strings in a case insensitive way
    '''
    tempString = ""
    footprintsTemp = ""
    if stringToReplace == "":
        if len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) == 0:
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToUse
        else:
            if footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][-1].isspace():
                tempString = stringToUse
            else:
                tempString = " " + stringToUse
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] + tempString
                
    elif len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) == 0:
        footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToUse

    else:
        tempString = ""
        substringPosition = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn].upper().find(stringToReplace.upper())
        if substringPosition != -1:
            footprintsTemp = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]
            redata = re.compile(re.escape(stringToReplace), re.IGNORECASE)
            footprintsTemp = redata.sub('', footprintsTemp)
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsTemp
#            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn].replace((stringToReplace), '', 1)

        if len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) == 0:
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToUse
            tempString = ""
        elif footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][-1].isspace():
            tempString = stringToUse
        else:
            tempString = " " + stringToUse
        footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] + tempString



#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
#-------------------------------------------------------------------------
# ----------------Constants and Data Structures--------------------------

# column numbers of the list created from the Dell-provided csv file
dellCompanyNameBillingColumn =   0
dellCompanyNameShippingColumn =  1
dellCustomerNumColumn =          2
dellPONumColumn =                3
dellOrderNumberColumn =          4
dellMasterInvNumColumn =         5
dellInvoiceNumColumn =           6
dellGroupDescColumn =            7
dellProductDescColumn =          8
dellBrandDescColumn =            9
dellItemNumColumn =              10
dellItemLongNameColumn =         11
dellSystemQtyColumn =            12
dellOrderQtyColumn =             13
dellTotalRevRetailUSDColumn =    14
dellTotalRevDiscUSDColumn =      15
dellFreightChargesColumn =       16
dellSalesTaxUSDColumn =          17
dellVatAmtLocalCurrencyColumn =  18
dellOrderStatusDescColumn =      19
dellOrderDateColumn =            20
dellShipByDateColumn =           21
dellShippedDateColumn =          22
dellInvDateColumn =              23
dellServiceTagsColumn =          24




kaceIpAddress = "10.148.1.18"
kacePassword = 'cpl123'

#defaultInfo = ("Default",'R1','ORG1')
aelInfo = ("AEL",'R2','ORG2')
cplInfo = ("CPL",'R3','ORG3')
cpeInfo = ("CPE",'R4','ORG4')
checkInInfo = ("Check-In",'R5','ORG5')
pliInfo = ("PLI", 'R6', 'ORG6')
palInfo = ("PAL", 'R7', 'ORG7')
srlInfo = ("SRL", 'R8', 'ORG8')
sonicCorpSoeInfo = ("Sonic Corp SOE", 'R9', 'ORG9') #....#12/16/2017...this appears to have been taken out of Kace...I will not append to the list
cblPathInfo = ("CBLPath",'R10','ORG10')
escLabInfo = ("ESCLab",'R11','ORG11')
smlInfo = ("SML",'R12','ORG12')

#Tuple element indices
organizationName = 0
dbUserName = 1
db = 2

#Footprints Exports Spreadsheet Column Numbers
assetNumberFootprintsColumn = 0
serviceTagFootprintsColumn = 1
vendorFootprintsColumn = 2
desktopModelFootprintsColumn = 3
formFactorFootprintsColumn = 5      #Column with form factor...we will obtain this bylooking up the service tag number inthe dell provided csv file and looking in its form factor column
organizationFootprintsColumn = 8    #Column number where we will put organization name within the footprints csv file



listOfOrgs = []
#note that deafaultInfo stuff is not included here
listOfOrgs.append(aelInfo)
listOfOrgs.append(cplInfo)
listOfOrgs.append(cpeInfo)
listOfOrgs.append(checkInInfo)
listOfOrgs.append(pliInfo)
listOfOrgs.append(palInfo)
listOfOrgs.append(srlInfo)
#listOfOrgs.append(sonicCorpSoeInfo)  #12/16/2017...this appears to have been taken out of Kace...I will not append to the list
#listOfOrgs.append(cblPathInfo)
#listOfOrgs.append(escLabInfo)
#listOfOrgs.append(smlInfo)


headerTuple = ('Asset #','Serial Number','Vendor','Desktop Model','Location','Details','IP Address','Operating System','Configuration ID','Invoice Date','Warranty Expiry Date','Warranty Expired','PO #','Invoice #','Cost Centre','Purchase Price','Purchasing Approved','Status')

#--------------------------------------------------------------
#Australia-formatted Names of vendors:

#This set of lists assumes that first list (list of lists  and the second one...the approvedList are in synch with each other
#    if something is found in one of the lists in the first table then we will use the
#    entry in approvedList which is in the same index of the first one
vendorList =[
["Dell Inc.","Dell"],
["Hewlett-Packard","Hewlett Packard","HP"],
["innotek","Innotek"],
["LENOVO","Lenovo"],
["Microsoft Corporation","Microsoft"],
["Touch Dynamic Inc.","Touch Dynamic"],
["VMware","VMware Inc.","Vmware"],
["Apple"],
["IBM"],
["Samsung"],
["Wacom"],
["Acer"],
["Micro-Star","Micro-Star International"],
["MSI"],
["Sony"],
["Toshiba"],
["Barracude","Barracuda"],
["BlueCoat"]
]
#we want to sort these because for each entry in the vendorList we want to compare with progressively larger strings.
#The reason is that if Dell Inc. exists in the footprints extract..we want ot replace that and not Dell.
for index1 in range(0,len(vendorList)):
    vendorList[index1] = sorted(vendorList[index1], key=lambda zz: len(zz), reverse=True)

vendorApprovedList = [
"Dell",
"HP",
"Innotek",
"Lenovo",
"Microsoft",
"Touch Dynamic",
"VMware",
"Apple",
"IBM",
"Samsung",
"Wacom",
"Acer",
"Micro-Star",
"MSI",
"Sony",
"Toshiba",
"Barracuda",
"BlueCoat"
]

#--------------------------------------------------------------
#--------------------------------------------------------------
'''
#we want to sort these because for each entry in the vendorList we want to compare with progressively larger strings.
#The reason is that if Dell Inc. exists in the footprints extract..we want ot replace that and not Dell.
for index1 in range(0,len(vendorList)):
    tempList = []
    tempList.clear()
    vendorList[index1] = sorted(vendorList[index1], key=lambda zz: len(zz), reverse=True)
'''    

'''
storeCSVAsList("Footprints Export_Output.csv",footprintsExportList)
footprintsServiceTag = ""
dellSericeTag = ""
writeTestListToCSV(footprintsExportList,'Footprints Export_Output.csv')
'''
storeCSVAsList("Footprints Export_Output.csv",footprintsExportList)
processVendorHalf()
writeTestListToCSV(footprintsExportList,'Footprints Export_Output_1217.csv')
print("end of program")
