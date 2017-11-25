#CONCERNS
#This one works correctly
#only concern is the sort order
#also expiration or active column includes No warranty data
#also moves file to footprints server

import csv
import datetime
import time

#new
#import win32wnet
import shutil
import os

import mysql.connector
#from python_mysql_dbconfig import read_db_config

#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
# 10/05/2017
# This program queries the KACE server
# It queries all the databases which we use that's on it and writes the results out to 1 file
# It makes sure that the data on that file is formatted in the column order according to the order and format desired by Footprints.
# Then it calls a batch file which will copy the file to the footprints server.
# Requirements for it to work:
#   1. The batch file needs to be in the same directory as this program file.  That directory can be anywhere

#-----------------------------------------------------------------------------------------------------
#October 18 or so I changed the SQL so that chassis type is taken from the KACE server. and put into the "details" column
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------


#-----------------------------------------------
# Constants and Data Structures
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
sonicCorpSoeInfo = ("Sonic Corp SOE", 'R9', 'ORG9')

#Tuple element indices
organizationName = 0
dbUserName = 1
db = 2

organizationColumn = 8    #Column number where we will put organization name within the footprints csv file

listOfOrgs = []

#note that deafaultInfo stuff is not included here
listOfOrgs.append(aelInfo)
listOfOrgs.append(cplInfo)
listOfOrgs.append(cpeInfo)
listOfOrgs.append(checkInInfo)
listOfOrgs.append(pliInfo)
listOfOrgs.append(palInfo)
listOfOrgs.append(srlInfo)
listOfOrgs.append(sonicCorpSoeInfo)

headerTuple = ('Asset #','Serial Number','Vendor','Desktop Model','Location','Details','IP Address','Operating System','Configuration ID','Invoice Date','Warranty Expiry Date','Warranty Expired','PO #','Invoice #','Cost Centre','Purchase Price','Purchasing Approved','Status')

#--------------------------------------------------------------
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
                rowAsList[organizationColumn] = listOfOrgs[i][organizationName]
                rowTuple = tuple(rowAsList)
                writer2.writerow(rowTuple)
                row = cursor.fetchone()
    finally:
        cnx.close()

#------------------------------------------------------------------
#------------------------------------------------------------------
# MOVE FILE OVER
os.system('CSVFileMover.bat')

#------------------------------------------------------------------
#------------------------------------------------------------------        
