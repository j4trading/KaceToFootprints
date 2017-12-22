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

def processModelName():
    #abc123
    vendorName = ""
    somethingInVendorColumnFlag = 0
    for i in range(0,len(footprintsExportList)):

        if len(footprintsExportList[i][vendorFootprintsColumn]) != 0:
            vendorName = footprintsExportList[i][vendorFootprintsColumn]
            
#        else theres nothing in the vendor column then:
#            the do nothing

        if somethingInVendorColumnFlag == 1:
            for j in range(0,len(vendorTuple)):
                for k in range(0,len(vendorTuple(j))):
                    i=1
                    i+=1

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
vendorTuple = (
("Dell","Dell Inc.","Dell"), 
("HP","Hewlett-Packard","Hewlett Packard","HP"), 
("Innotek","innotek","Innotek"), 
("Lenovo","LENOVO"), 
("Microsoft","Microsoft Corporation","Microsoft"), 
("Touch Dynamic","Touch Dynamic Inc.","Touch Dynamic"), 
("Vmware","VMware"," Inc.","Vmware"), 
("Apple","Apple"), 
("IBM","IBM"), 
("Samsung","Samsung"), 
("Wacom","Wacom"), 
("Acer","Acer"), 
("Micro-Star","Micro-Star","Micro-Star International"), 
("MSI","MSI"), 
("Sony","Sony"), 
("Toshiba","Toshiba"), 
("Barracuda","Barracude","Barracuda"), 
("BlueCoat","BlueCoat"), 

)


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
with open('Footprints Export_Output.csv', "w", newline = '') as csv_file:  #debug
	writer2 = csv.writer(csv_file, delimiter=',')  #debug
	writer2.writerow(headerTuple)

for i in range(len(listOfOrgs)):
    print(listOfOrgs[i]) #debug	
    try:
        cnx = mysql.connector.connect(user=listOfOrgs[i][dbUserName], password = kacePassword,
                                    host=kaceIpAddress
                                    , database=listOfOrgs[i][db])
        cursor = cnx.cursor()
        cursor.execute(stotaltemp)
    
        rowAsList = []   #This list is needed because we needed to modify the tuple that sql outputs as a row, but tuples cannot be modified whereas lists can
        with open('Footprints Export_Output.csv', "a", newline = '') as csv_file:
            writer2 = csv.writer(csv_file, delimiter=',')  #debug
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
#        footprintsExportList[i].append("nope")        #debug
        continue
    for j in range(1,len(dellTableList)):
        dellServiceTag = dellTableList[j][dellServiceTagsColumn]
        if dellServiceTag.find(",") != -1:              #this small section is for case where Dell service tag data consists of multiple service tags
            tempList = dellServiceTag.split(',')            #make a list to iterate through the multiple service tags
            for k in range(0,len(tempList)):
                if not(tempList[k].isspace() or tempList[k] == "" or tempList[k] == '0' or tempList[k].strip() == '0'):     #ignore if only consists combination of whitespace and 1 zero
                    if tempList[k].lower() == footprintsServiceTag.lower():
 #                       footprintsExportList[i].append(j)    #debug
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


writeTestListToCSV(footprintsExportList,'Footprints Export_Output.csv')

#------------------------------------------------------------------
#------------------------------------------------------------------
# MOVE FILE OVER
#os.system('CSVFileMover.bat')

#------------------------------------------------------------------
#------------------------------------------------------------------        

