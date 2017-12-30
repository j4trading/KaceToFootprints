#TO DO....
#APPEARS TO WORK FINE NOW 12/28/17

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

#///////////////////////////////////////////////////////////////////////////

def storeCSVAsList(fileName,outputList):
    del outputList[:]
    with open(fileName,'r') as f:
        csv_f = csv.reader(f)
        for row in csv_f:
#            oneRowList = row[:]
            outputList.append(row)

#///////////////////////////////////////////////////////////////////////////

def writeTestListToCSV(listToWrite, outputFile):
    with open(outputFile,"w", newline = '') as csv_file2:
        writer = csv.writer(csv_file2, delimiter=',')
        for line in listToWrite:
            writer.writerow(line)   

#///////////////////////////////////////////////////////////////////////////

def processVendorHalf():
    """
At the point before callign this function the program takes the kace extract and uses purchasehistory csv which ssociates
asset tag numbers to form factors...the form factor information is included into the details column.
This function will take vendor (whther it be in the vendor column or already in thet details column) and make sure that it be put in the beginning of the details column
It also makes sure that any vendor that it puts in the details column that it be approved by the vendor list in this program
"""
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

    #we want to sort vendorList because for each entry in the vendorList we want to compare with progressively larger strings.
    #The reason is that if Dell Inc. exists in the footprints extract..we want ot replace that and not Dell.
    for index1 in range(0,len(vendorList)):
        vendorList[index1] = sorted(vendorList[index1], key=lambda zz: len(zz), reverse=True)

    for i in range(0,len(footprintsExportList)):   #main loop for entire function
        stringInVendorColumn = footprintsExportList[i][vendorFootprintsColumn]
        stringInDetailsColumn = footprintsExportList[i][formFactorFootprintsColumn]

        #Set emptiness variable

        if footprintsExportList[i][vendorFootprintsColumn] == "":
            vendorColumnNotEmpty = 0
        else:
            vendorColumnNotEmpty = 1
        if footprintsExportList[i][formFactorFootprintsColumn] == "":
            ffColumnNotEmpty = 0
        else:
            ffColumnNotEmpty = 1

        #see if vendor column contains anything in the vendor list and set appropriate variables accordingly
        if vendorColumnNotEmpty != 0:
            for j in range(0,len(vendorList)):
                for k in range(0,len(vendorList[j])):
                    substringPosition = stringInVendorColumn.lower().find(vendorList[j][k].lower())
                    if substringPosition != -1:
                        vendorCFoundInList = 1
                        vendorInListOuterIndex = j
                        vendorInListInnerIndex = k
                        break
                if substringPosition != -1:
                    break
        #see if details contains anything in the vendor list
        if ffColumnNotEmpty != 0:
            for j in range(0,len(vendorList)):
                for k in range(0,len(vendorList[j])):
                    substringPosition = stringInDetailsColumn.lower().find(vendorList[j][k].lower())
                    if substringPosition != -1:
                        ffCFoundInList = 1
                        ffInListOuterIndex = j
                        ffInListInnerIndex = k
                        break
                if substringPosition != -1:
                    break

        if vendorColumnNotEmpty == 0 and ffColumnNotEmpty == 0:
            pass        #do nothing....we need to exit the function

        elif vendorColumnNotEmpty ==0 and ffColumnNotEmpty != 0:
            if ffCFoundInList == 0:
                pass    #do nothing....we need to exit the function
            else:
                replaceVendorStrings(vendorApprovedList[ffInListOuterIndex], vendorList[ffInListOuterIndex][ffInListInnerIndex], i)

        elif vendorColumnNotEmpty !=0 and ffColumnNotEmpty == 0:
            if vendorCFoundInList == 0:
                footprintsExportList[i][formFactorFootprintsColumn] = stringInVendorColumn
            else:
                footprintsExportList[i][formFactorFootprintsColumn] = vendorApprovedList[vendorInListOuterIndex]
    
        elif vendorColumnNotEmpty !=0 and ffColumnNotEmpty != 0:
            if vendorCFoundInList == 0 and ffCFoundInList == 0:
                pass    #do nothing...we need to exit the function
            elif vendorCFoundInList != 0 and ffCFoundInList == 0:
                replaceVendorStrings(vendorApprovedList[vendorInListOuterIndex], "", i)
            elif vendorCFoundInList == 0 and ffCFoundInList != 0:
                replaceVendorStrings(vendorApprovedList[ffInListOuterIndex], vendorList[ffInListOuterIndex][ffInListInnerIndex], i)
            elif vendorCFoundInList != 0 and ffCFoundInList != 0:
                replaceVendorStrings(vendorApprovedList[vendorInListOuterIndex], vendorList[ffInListOuterIndex][ffInListInnerIndex], i)


#///////////////////////////////////////////////////////////////////////////

def processFFHalf():
  """
At the point before callign this function the program takes the kace extract and uses purchasehistory csv which ssociates
asset tag numbers to form factors...the form factor information is included into the details column.
This function will take form factor info (which may already be thet details column) and make sure that it be put in the end of the details column
It also makeks sure that if it putst form factor that for each possible form facator that it only be exactly as in the "approved table"
"""
  
    ffColumnNotEmpty = 0
    ffCFoundInList = 0
    ffInListOuterIndex = 0
    ffInListInnerIndex = 0    
    substringPosition = -1
    stringInDetailsColumn = ""

    #we want to sort ffList because for each entry in the ffList we want to compare with progressively larger strings.
    #The reason is that if Dell Inc. exists in the footprints extract..we want ot replace that and not Dell.
    for index1 in range(0,len(ffList)):
        ffList[index1] = sorted(ffList[index1], key=lambda zz: len(zz), reverse=True)

    for i in range(0,len(footprintsExportList)):   #main loop for entire function
        stringInDetailsColumn = footprintsExportList[i][formFactorFootprintsColumn]
        ffColumnNotEmpty = 0
        ffCFoundInList = 0
        ffInListOuterIndex = 0
        ffInListInnerIndex = 0    
        substringPosition = -1

        #If nothing in details/form factor column do nothing
        if footprintsExportList[i][formFactorFootprintsColumn] == "":
            pass            #do nothing

        else:
            #Check if something in details/form factor column found in ffList...if it is then place approved list's version in colum
            #if not...then leave alone
            for j in range(0,len(ffList)):
                for k in range(0,len(ffList[j])):
                    substringPosition = stringInDetailsColumn.lower().find(ffList[j][k].lower())
                    if substringPosition != -1:
                        ffCFoundInList = 1
                        ffInListOuterIndex = j
                        ffInListInnerIndex = k
                        break
                    else:
                        ffCFoundInList = 0
                if substringPosition != -1:
                    break

            if ffCFoundInList == 0:
                pass  #do nothing
            else:
                replaceFFStrings(ffApprovedList[ffInListOuterIndex],ffList[ffInListOuterIndex][ffInListInnerIndex],i)

#///////////////////////////////////////////////////////////////////////////

def replaceVendorStrings(stringToUse, stringToReplace, footprintsListIndex):
    '''
    This function puts stringToUse  at the beginning of the string.
    If stringToReplace exists in the string then it will take it out before adding in stringToUse
    It is mindful of including a space to separate it and what word woudl be after it
    If what is after it is a whitespace then it won't add a space there.
    Regular expressions are used as it's the only way to replace strings in a case insensitive way
    '''
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

            #This section takes out "stringToReplace" from the details/form factor column
            #But it first calculates what space needs to be taken out which would accompany the word
            #tempStringReplace holds stringToReplace plus a possible space before or after
            #Then the section below with redata uses regular expressions to take out that sub string without being case sensitive.
            tempStringReplace = stringToReplace
            if substringPosition == 0 and len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) == len(stringToReplace):   #stringToReplace is the only string there
                tempStringReplace = stringToReplace
            if substringPosition == 0 and len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) > len(stringToReplace): #stringToReplace is not the only string..also it's at the beginning
                if footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][len(stringToReplace)].isspace():
                    tempStringReplace = stringToReplace + " "
                else:
                    tempStringReplace = stringToReplace
            if substringPosition != 0 and len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) > substringPosition + len(stringToReplace): #stringToReplace is not the only string..and it's neither at the beginning nor end..somewhere in the middle

                if footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][substringPosition - 1].isspace() and footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][substringPosition + len(stringToReplace)].isspace():
                    tempStringReplace = stringToReplace + " "
                else:
                    tempStringReplace = stringToReplace
            if substringPosition != 0 and (len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) - 1 == substringPosition + len(stringToReplace)): #stringToReplace is not the only string..also it's at the end
                if footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][substringPosition - 1].isspace():
                    tempStringReplace = " " + stringToReplace
                else:
                    tempStringReplace = stringToReplace
            #This part does the actual removing of the substring...uses case insesitive regular expressions
            redata = re.compile(re.escape(tempStringReplace), re.IGNORECASE)
            footprintsTemp = redata.sub('', footprintsTemp,count=1)
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsTemp

        # This section adds the vendor name at he beginning keepign in mind if a space needs to accompany that.
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

            #This section takes out "stringToReplace" from the details/form factor column
            #But it first calculates what space needs to be taken out which would accompany the word
            #tempStringReplace holds stringToReplace plus a possible space before or after
            #Then the section below with redata uses regular expressions to take out that sub string without being case sensitive.
            tempStringReplace = stringToReplace
            if substringPosition == 0 and len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) == len(stringToReplace):   #stringToReplace is the only string there
                tempStringReplace = stringToReplace
            if substringPosition == 0 and len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) > len(stringToReplace): #stringToReplace is not the only string..also it's at the beginning
                if footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][len(stringToReplace)].isspace():
                    tempStringReplace = stringToReplace + " "
                else:
                    tempStringReplace = stringToReplace
            if substringPosition != 0 and len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) > substringPosition + len(stringToReplace): #stringToReplace is not the only string..and it's neither at the beginning nor end
                if footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][substringPosition - 1].isspace() and footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][substringPosition + len(stringToReplace)].isspace():
                    tempStringReplace = stringToReplace + " "
                else:
                    tempStringReplace = stringToReplace
            if substringPosition != 0 and (len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) - 1 == substringPosition + len(stringToReplace)): #stringToReplace is not the only string..also it's at the end
                if footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][substringPosition - 1].isspace():
                    tempStringReplace = " " + stringToReplace
                else:
                    tempStringReplace = stringToReplace
            #This part does the actual removing of the substring...uses case insesitive regular expressions
                    
            redata = re.compile(re.escape(tempStringReplace), re.IGNORECASE)
            footprintsTemp = redata.sub('', footprintsTemp,count=1)
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsTemp
#            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn].replace((stringToReplace), '', 1)

        # This section adds the form factor info at the end keepign in mind if a space needs to accompany that.
        if len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) == 0:
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToUse
            tempString = ""
        elif footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][-1].isspace():
            tempString = stringToUse
        else:
            tempString = " " + stringToUse
        footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] + tempString

#///////////////////////////////////////////////////////////////////////////

#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
#-------------------------------------------------------------------------
# ----------------Constants and Data Structures--------------------------

dellTableList = []

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

#---------------------------------------------------------------------------

kaceIpAddress = "10.148.1.18"
kacePassword = 'cpl123'

#---------------------------------------------------------------------------

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


#---------------------------------------------------------------------------
footprintsExportList = []
#Footprints Exports Spreadsheet Column Numbers for footprintsExportList which is a list of lists each of which hold the output of the kace sql query
assetNumberFootprintsColumn = 0
serviceTagFootprintsColumn = 1
vendorFootprintsColumn = 2
desktopModelFootprintsColumn = 3
formFactorFootprintsColumn = 5      #Column with form factor...we will obtain this bylooking up the service tag number inthe dell provided csv file and looking in its form factor column
organizationFootprintsColumn = 8    #Column number where we will put organization name within the footprints csv file



#---------------------------------------------------------------------------

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
#we want to sort vendorList because for each entry in the vendorList we want to compare with progressively larger strings.
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
#Australia-formatted form factors:

#This set of lists assumes that first list (list of lists  and the second one...the approvedList are in synch with each other
#    if something is found in one of the lists in the first table then we will use the
#    entry in approvedList which is in the same index of the first one
#    for small entries like aio...I'm using a space in front like ' aio' because since that text is so small it could be found in other contexts as substrings within the details/form factor column
ffList =[
[' aio','all-in-one','allinone','all in one'],
['medium form factor','medium form',' mff','medium-form-factor'],
['microtower','micro tower','micro-tower','micro form factor','micro-form-factor'],
['mini tower', 'minitower', 'mini-tower'],
['small form factor','small form','sff','small-form factor','small-form-factor'],
['ultra small',' usff','ultra-small'],
[' CMT'],
[' MT'],
[' USDT', 'ultra-slim-desktop','ultra-slim desktop','ultra slim desktop'],
['thin client','thinclient','thin-client'],
]
#we want to sort ffList because for each entry in the ffList we want to compare with progressively larger strings.
#The reason is that if Dell Inc. exists in the footprints extract..we want ot replace that and not Dell.
for index1 in range(0,len(ffList)):
    ffList[index1] = sorted(ffList[index1], key=lambda zz: len(zz), reverse=True)

ffApprovedList = [
'AIO',
'MFF',
'Micro',
'Mini',
'SFF',
'USFF',
'CMT',
'MT',
'USDT',
'Thin Client',
]

#--------------------------------------------------------------

#--------------------------------------------------------------
#--------------------------------------------------------------
#SQL query
# Some of this below is only in there because it mimics what the Kace server sql wizard creates.
# Mainly I'm referring to the \t\t characters below.  I don't know what that does.
stemp1="SELECT ASSET.NAME AS ASSET_NAME,"
stemp2=""
stemp3="MACHINE.BIOS_SERIAL_NUMBER,"
stemp4="        CS_MANUFACTURER, "
stemp5="        CS_MODEL, "
stemp6="        ASSET_LOCATION.NAME AS LOCATION, "
stemp6b=" MACHINE.CHASSIS_TYPE as DETAILS, "
stemp7=""
stemp8="        MACHINE.IP,"
stemp9="        OS_NAME, "
stemp9b=" '' as CONFIGURATIONID, "
stemp9c=" '' as INVOICEDATE, "
stemp10=""
stemp11="#     DELL_WARRANTY.START_DATE, #DELL_WARRANTY.END_DATE,"
stemp12="#     DELL_WARRANTY.ENTITLEMENT_TYPE,DELL_WARRANTY.ITEM_NUMBER, DELL_WARRANTY.SERVICE_LEVEL_CODE, "
stemp13="#     DELL_WARRANTY.SERVICE_LEVEL_GROUP, DELL_WARRANTY.SERVICE_PROVIDER, "
stemp14="#     DELL_WARRANTY.SERVICE_LEVEL_DESCRIPTION,"
stemp15=""
stemp16=""
stemp17="MAX(DELL_WARRANTY.END_DATE), case when DW.ENDDATE < curdate() then 'Expired' when DW.ENDDATE IS NULL then 'No Warranty' else 'Active' end as DW_EXPIRED, "

stemp17a=" '' as PONumber, "
stemp17b=" '' as InvoiceNumber, "
stemp17c=" '' as CostCentre, "
stemp17d=" '' as PurchasePrice, "
stemp17e=" '' as PurchasingApproved, "
stemp17f=" '' as Status "

stemp33=""
stemp34="FROM MACHINE "
stemp35=""
stemp36=""
stemp37=""
stemp38="LEFT OUTER JOIN DELL_WARRANTY ON MACHINE.BIOS_SERIAL_NUMBER = DELL_WARRANTY.SERVICE_TAG "
stemp39=""
stemp40=" left join (select max(END_DATE) ENDDATE, SERVICE_TAG as TAG, SERVICE_LEVEL_CODE as SVCCODE "
stemp41=" from             DELL_WARRANTY DW group by SERVICE_TAG, SERVICE_LEVEL_CODE) "
stemp42=" DW \t\ton DW.TAG = DELL_WARRANTY.SERVICE_TAG and DW.SVCCODE = DELL_WARRANTY.SERVICE_LEVEL_CODE \t\t\tand DW.ENDDATE = DELL_WARRANTY.END_DATE "
stemp43=""
stemp44=""
stemp45="LEFT JOIN MACHINE_LABEL_JT ON (MACHINE_LABEL_JT.MACHINE_ID = MACHINE.ID)  "
stemp46="LEFT JOIN LABEL ON (LABEL.ID = MACHINE_LABEL_JT.LABEL_ID) "
stemp47="LEFT JOIN ASSET ON ASSET.MAPPED_ID = MACHINE.ID AND ASSET.ASSET_TYPE_ID=5 "
stemp48="LEFT JOIN ASSET ASSET_LOCATION ON ASSET_LOCATION.ID = ASSET.LOCATION_ID   "
stemp49=""
stemp50=""
stemp51=" LEFT JOIN (select @limitct :=0) T on 1=1 "
stemp52=" WHERE ((DELL_WARRANTY.SERVICE_LEVEL_DESCRIPTION LIKE '%Onsite%') OR (DELL_WARRANTY.SERVICE_LEVEL_DESCRIPTION LIKE '%ProSupport%') OR (DELL_WARRANTY.SERVICE_LEVEL_DESCRIPTION IS NULL)) "
stemp53=""
#stemp54=" GROUP BY MACHINE.BIOS_SERIAL_NUMBER ,START_DATE,END_DATE"
stemp54=" GROUP BY MACHINE.BIOS_SERIAL_NUMBER"
stemp55=""
stemp56=" ORDER BY MACHINE.IP "


stotaltemp = stemp1+stemp2+stemp3+stemp4+stemp5+stemp6+stemp6b+stemp8+stemp9+stemp9b+stemp9c+stemp17+stemp17a+stemp17b+stemp17c+stemp17d+stemp17e+stemp17f+stemp34+stemp38+stemp40+stemp41+stemp42+stemp45+stemp46+stemp47+stemp48+stemp50+stemp51+stemp52+stemp54+stemp56

#--------------------------------------------------------------
#--------------------------------------------------------------
#THIS SECTION WRITES THE SQL RESULTS TO THE OUTPUT FILE

#write the header
with open('Footprints Export_Output.csv', "w", newline = '') as csv_file: 
	writer2 = csv.writer(csv_file, delimiter=',')
	writer2.writerow(headerTuple)

for i in range(len(listOfOrgs)):
    try:
        cnx = mysql.connector.connect(user=listOfOrgs[i][dbUserName], password = kacePassword,
                                    host=kaceIpAddress
                                    , database=listOfOrgs[i][db])
        cursor = cnx.cursor()
        cursor.execute(stotaltemp)
    
        rowAsList = []   #This list is needed because we needed to modify the tuple that sql outputs as a row, but tuples cannot be modified whereas lists can
        with open('Footprints Export_Output.csv', "a", newline = '') as csv_file:
            writer2 = csv.writer(csv_file, delimiter=',')  
            row = cursor.fetchone()

            while row is not None:
                rowAsList.clear()
                rowAsList = list(row)
                rowAsList[organizationFootprintsColumn] = listOfOrgs[i][organizationName]
                rowTuple = tuple(rowAsList)
                writer2.writerow(rowTuple)
                row = cursor.fetchone()
    finally:
        cnx.close()

#-----------------------------------------------------------
#-----------------------------------------------------------
#-----------------------------------------------------------
#This section takes the Kace SQL output and looks for the service tag number in the Dell provided table in order to get the form factor from its row of data.
#If the service tag number in the Kace SQL output is any combination of whitespace and just 1 zero (not necessarily both) but with no other characters then it ignores it
#If the service tag number in the Dell provided table has that same combination then it also ignores it in the program's search for the service tag number.
#If it finds the service tag in the Dell table then it takes the form factor in that row and puts it in the corresponding cell in the Kace SQL output.
#Finally it writes that output to a Footprints csv file.
        
storeCSVAsList('purchaseHistory.csv',dellTableList)
storeCSVAsList("Footprints Export_Output.csv",footprintsExportList)
#writeTestListToCSV(footprintsExportList,'testFootprintsFileBefore.csv')
footprintsServiceTag = ""
dellSericeTag = ""

#debug
foundFlag = 0
tempList = []
for i in range(1,len(footprintsExportList)):
    foundFlag = 0
    footprintsServiceTag = footprintsExportList[i][serviceTagFootprintsColumn]
    if footprintsServiceTag.isspace() or footprintsServiceTag == "" or footprintsServiceTag == '0' or footprintsServiceTag.strip() == '0':    #ignore if only consists combination of whitespace and 1 zero
        continue
    for j in range(1,len(dellTableList)):
        dellServiceTag = dellTableList[j][dellServiceTagsColumn]
        if dellServiceTag.find(",") != -1:              #this small section is for case where Dell service tag data consists of multiple service tags
            tempList = dellServiceTag.split(',')            #make a list to iterate through the multiple service tags
            for k in range(0,len(tempList)):
                if not(tempList[k].isspace() or tempList[k] == "" or tempList[k] == '0' or tempList[k].strip() == '0'):     #ignore if only consists combination of whitespace and 1 zero
                    if tempList[k].lower() == footprintsServiceTag.lower():
                        footprintsExportList[i][formFactorFootprintsColumn] = dellTableList[j][dellItemLongNameColumn]
                        foundFlag = 1
                        break
                else:
                    foundFlag = 0
                    continue
            if foundFlag == 1:      #after the k index for loop we still need to break out of the j index for loop
                break
        else:
            if not(dellServiceTag.isspace() or dellServiceTag == "" or dellServiceTag == '0' or dellServiceTag.strip() == '0'):         #ignore if only consists combination of whitespace and 1 zero
                if dellServiceTag.lower() == footprintsServiceTag.lower():
                    footprintsExportList[i][formFactorFootprintsColumn] = dellTableList[j][dellItemLongNameColumn]
                    foundFlag = 1
                    break
            else:
                foundFlag = 0
                continue
    
    if foundFlag == 0:                  #if the Dell provided spreadsheet doesn't have the form factor information then we will use desktop model that is already in our footprints spreadsheet.
                                        # the reason is that in that case we will have something too generic looking in our footprints form factor column (right now this column is titled "Details")
       footprintsExportList[i][formFactorFootprintsColumn] = footprintsExportList[i][desktopModelFootprintsColumn]


writeTestListToCSV(footprintsExportList,'Footprints Export_Output.csv')   #run it here to see what it looks like before we start the functions that consolidate the makes,models, and form factors all into the details column

#------------------------------------------------------------------

#------------------------------------------------------------------       
#This will take care of the consolidation portion
storeCSVAsList("Footprints Export_Output.csv",footprintsExportList)
processVendorHalf()
processFFHalf()
writeTestListToCSV(footprintsExportList,'Footprints Export_Output_after_consolidation.csv')
#------------------------------------------------------------------
# MOVE FILE OVER
os.system('CSVFileMover.bat')

#------------------------------------------------------------------
#------------------------------------------------------------------        

