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
    
#abc444

    

vendorNameToUse = ""
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
                    
#                x        
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
                            
#///////////////////////////////////////////////////////////////////////////                            
                                                        
def processModelNameColumn_2():
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

#*******
'''
    vendorStringToReplace = ""
    vendorStringToUse = ""
    stringInVendorColumn = footprintsExportList[i][vendorFootprintsColumn]
    stringInDetailsColumn = footprintsExportList[i][formFactorFootprintsColumn]
    for i in range(0,len(footprintsExportList)):
        if len(stringInDetailsColumn) == 0 and len(stringInVendorColumn) == 0:
            pass #do nothing
        if len(stringInDetailsColumn) == 0 and len(stringInVendorColumn) != 0:
            SEARCH VENDOR (stringInVendorColumn) IN TABLE AND GET vendorStringToUse
            just simply do footprintsExportList[i][formFactorFootprintsColumn] = stringInVendorColumn
        if len(stringInDetailsColumn) != 0 and len(stringInVendorColumn) == 0:
            pass #do nothing
        if len(stringInDetailsColumn) != 0 and len(stringInVendorColumn) != 0:        
            SEARCH VENDOR TABLE FOR STUFF LIKE IN stringInDetailsColumn
            Then equate vendorStringToReplace to the entry you found
            Then set vendorStringToUse to the entry of that table
            Then call replace function using those 2 strings alogn with the i
            
'''

'''
    This function just runs through all of the possibilities and details what to do in each of those cases;
    Like what to do if length ofdetails column contents is 0 and vendorcolumn contents is not...etc...
'''
    vendorStringToReplace = ""
    vendorStringToUse = ""
    stringInVendorColumn = ""
    stringInDetailsColumn = ""
    substringPosition = ""
    substringLength = 0
    for i in range(0,len(footprintsExportList)):
        stringInVendorColumn = footprintsExportList[i][vendorFootprintsColumn]
        stringInDetailsColumn = footprintsExportList[i][formFactorFootprintsColumn]
        substringPosition = ""
        substringLength = 0
        
        if len(stringInDetailsColumn) == 0 and len(stringInVendorColumn) == 0:
            pass #do nothing
        
        elif len(stringInDetailsColumn) == 0 and len(stringInVendorColumn) != 0:
#           SEARCH VENDOR (stringInVendorColumn) IN vendorTABLE AND GET vendorStringToUse
            for j in range(0,len(vendorList)):
                for k in range(0,len(vendorList[j])):
                    substringPosition = stringInVendorColumn.lower().find(vendorList[j][k].lower())
                    if substringPosition != -1:
                        vendorStringToUse = vendorList[j][k]
                        break
                if substringPosition != -1:
                   break
                
            if substringPosition == -1:
                #Case where vendor column didn't contain any of the vendors we're looking for
                footprintsExportList[i][formFactorFootprintsColumn] = vendorStringToUse
            else:
                #Case where vendor column did have searched for vendor.
                footprintsExportList[i][formFactorFootprintsColumn] = vendorApprovedList[j]

        elif len(stringInDetailsColumn) != 0 and len(stringInVendorColumn) == 0:
            pass #do nothing

        elif len(stringInDetailsColumn) != 0 and len(stringInVendorColumn) != 0:
#            SEARCH VENDOR TABLE FOR STUFF LIKE IN stringInDetailsColumn
#            Then equate vendorStringToReplace to the entry you found
#            Then set vendorStringToUse to the entry of that table
#            Then call replace function using those 2 strings alogn with the i
            substringPosition = -1
            tempVendorEntry = ""
            for j in range(0,len(vendorList)):
                for k in range(0,len(vendorList[j])):
                    substringPosition = stringInDetailsColumn.lower().find(vendorList[j][k].lower())
                    if substringPosition != -1:
                        vendorStringToReplace = vendorList[j][k]
                        vendorStringToUse = vendorApprovedList[j]
                        break
                if substringPosition != -1:
                    break
            #Case where details column contains a vendor string in our table/list
            if substringPosition != -1:
                CALL REPLACE FUNCTION

            #Case where details column doesn't contain a vendor string in our list
            else:
                pass      #leave alone
#///////////////////////////////////////////////////////////////////////////
def replaceVendorStrings(stringToUse, strintToReplace, footprintsListIndex):
    '''
    This function forsees that in the details column of the footprints output (formFactorFootprintsColumn) we want the vendor to be first
    This function looks for stringToReplace.  If it finds it in the footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] cell then it takes it out, and then places stringToUse in the beginning of thta cell.
    It is mindful of taking out any spaces that would need to be taken out before or after it.
    positionOfSubstringToReplace is the position within the destionaion of the stringToReplace
    It returns a 0 if unsuccessful and a 1 if successful.
    '''
    substringPosition = 0
    substringLength = 0
    footprintsDetails = footprintsExportList[i][formFactorFootprintsColumn]

'''
    case 1: DESTINATION IS EMPTY STRING
        TRIVIAL
    case 1.5: details has nothing to replace
        Nonsensical...function would not have been called in that case.  But if it were it woudl have probably been called with stringToReplace = ""
    case 1.6: case where stringToReplace = ""...Good to handle this case in case function end user uses it as such
    case 1.7: case where stringToUse = "".....same as case for where stringToReplace == ""
    case 1.8: case where stringToReplace != "" but it is not found in nonempty destination cell
    case 2: place in beginning
    caae 2.5: details only has stringToReplace and nothing else
    case 3: place in middle
    case 4: place at end (not there is other stuff besides the string to replace)

    First see if destination cell is empty or not...if it is then just stick stringToUSe in
    Next look for stringToReplace.
    Use Find function to take note if it in the beginning, middle, or end.  Also use it to store substringPosition and substringLength.
    Decide what adjacent characters you'd also want to remove and add those to modify substringPosition and substringLength.'
'''

    #see if details/form factor column is empty
    #handles case 1 listed above
    if len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) == 0:
        footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = substringToUse
        return 1


    #handles case 1.7 listed above and thus case 1.6
    elif len(stringToUse) == 0:
        return 1

    #because of previous "returns" this case is where both stringToReplace and stringToUse are not ""...also details/form factor column is not empty
    elif len(stringToReplace) != 0 and len(stringToUse) != 0 and len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) != 0:
        substringPosition = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn].find(strintToReplace)
        #the following handles case 1.8
        if substringPosition == -1:
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToUse + " " + footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]

        #case 2.5
        elif substringPosition == 0 and len(footprintsDetails) == len(stringToReplace):
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToUse

        #handles case 2
        elif substringPosition == 0 and len(footprintsDetails) > len(stringToReplace):
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn].replace((stringToReplace), '', 1)
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToReplace + footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]

        #handles case 4
        elif substringPosition + len(stringToReplace) == len(footprintsDetails) and substringPosition != 0:
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn].replace((stringToReplace), '', 1)
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]

        #handles case 3
        elif substringPosition + len(stringToReplace) != len(footprintsDetails) and substringPosition != 0:
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn].replace((stringToReplace), '', 1)
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]
            
    return 1        
                
        

#///////////////////////////////////////////////////////////////////////////                            
def putVendorIntoDetails(vendorToUse,footprintsRow, vendorListRow, entryInVendorListRow,substringPosition):
    """
    This will put the vendorToUse in the details column of the spreadsheet depending on how the various states in that details cell
    It will first find whatever was already in there based on i,j,k and it will take it out
    If substringPosition == -1 then it won't try to substitute anything out and it will merely put it in the front.
    If it wasn't in there then it won't take it out.
    """
   


#///////////////////////////////////////////////////////////////////////////
            for j in range(0,len(vendorList)):
                for k in range(1,len(vendorList
#        else theres nothing in the vendor column then:
#            the do nothing

        if somethingInVendorColumnFlag != 0:
            for j in range(0,len(vendorList)):
                for k in range(1,len(vendorList(j))):       #here we're searching whatever is in the vendor list column and replace it withsomething from our vendor List table
                    substringPosition = vendorNameInKace.lower().find(vendorList(j)(k).lower())
                    if substringPosition != -1:
                        vendorNameToUse = vendorList[j][0]
                        footprintsExportList[i][vendorFootprintsColumn] = vendorNameToUse
                        
                
                        detailsInKace = footprintsExportList[i][formFactorFootprintsColumn]
                        substringPosition = 0
                        substringPosition = detailsInKace.lower().find(vendorList[j][k].lower())
                        if substringPosition != -1:
                            substringLength = len(vendorList[j][k])
                            for m in range(0,len(detailsInKace)):
                                tempList[m] = detailsInKace[m]
                            for m in range(0,substringLength):
                                tempList.pop(m + substringPosition)
                            if (substringPosition + substringLength) < len(detailsInKace):      #take out teh space that would follow what we took out but not if what we took out was at the very end.  And we use detailsInKace because tempList presents as it is after changing it.
                                if tempList[substringPosition + substringLength] == " ":
                                    tempList.pop(substringPosition + substringLength)
                            for m in range(0,len(vendorList[j][0]):
                                tempList.insert(0,vendorList[j][0][m])
                            if len(tempList) > len(vendorList[j][0]):               #here add a space after the vendor prepend if needed...but not if we're at the end of the string.
                                if tempList[len(vendorList[j][0])] != " ":
                                    tempList.insert(len(vendorList[j][0])," ")

                            tempString = ‘’.join(str(element) for element in tempList)
                            footprintsExportList[i][formFactorFootprintsColumn] = tempString
                            vendorInDetailsModifiedFlag = 1
                            break

                if vendorInDetailsModifiedFlag == 1:
                    break
                
            #for the case where what was in the Vendor column was not found anywhere in the details column...we do the following:
            vendorFoundInVendorListFlag = 0
            for j in range(0,len(vendorList)):
                for k in range(1,len(vendorList(j))):
                    substringPosition = vendorNameInKace.lower().find(vendorList[j][k].lower())
                    if substringPosition != -1:
                        vendorFoundInVendorListFlag = 1
                        if len(footprintsExportList[i][formFactorFootprintsColumn]) == 0:
                            
                        vendorNameToUse = vendorList[j][0]
                        
                    else: #substringPosition 
                        somethingInVendorColumnFlag = 0

def putModelNameInDetailsColumn():
    substringFoundFlag = 0
    footprintsValue = ""
    substringLength = 0
    for i in range(0,len(footprintsExportList)):
        footprintsValue = footprintsExportList[i][formFactorFootprintsColumn]        
        for j in range(0,len(vendorList)):
            for k in range(1,len(vendorList[j])):
                substringPosition = footprintsValue.find(vendorList[j][k])
                if substringPosition != -1:
                    substringFoundFlag = 1
                    tempString = ""
                    substringLength = len(vendorList[j][k])
                    for l in range(0,substringPosition)):
                        tempString[l] = footprintsValue[l]
                    stringIndex = 0
                    for m in range(subtringPosition,substringPosition + substringLength):
                        tempString[m] = vendorList[j][k][stringIndex]
                        stringIndex += 1
                    for n in range(substringPosition + substringLength, len(footprintsValue)):
                        tempString[n] = footprintsValue[n]
                    footprintsExportList[i][formFactorFootprintsColumn] = tempString
                    break
            if substringFoundFlag != 0:
                break
                
                                         

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------

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
vendorList =
[
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

#we want to sort these because for each entry in the vendorList we want to compare with progressively larger strings.
#The reason is that if Dell Inc. exists in the footprints extract..we want ot replace that and not Dell.
for index1 in range(0,len(vendorList)):
    tempList = []
    tempList.clear()
    vendorList[index1] = sorted(vendorList[index1], key=lambda zz: len(zz), reverse=True)
    

storeCSVAsList("Footprints Export_Output.csv",footprintsExportList)
footprintsServiceTag = ""
dellSericeTag = ""
writeTestListToCSV(footprintsExportList,'Footprints Export_Output.csv')
