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
            if footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][0] == " ":
                footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToUse + " " + footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]
            else:
                footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToUse + footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]

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

#---------------------------------------------------------------------------

#///////////////////////////////////////////////////////////////////////////
