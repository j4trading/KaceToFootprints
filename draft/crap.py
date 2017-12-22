string1 = "abcd ecd cd f"
string2 = "cd"
spos = string1.find(string2)
print(spos)
slen = len(string2)
l = list(string1)
print(l)
string3 = ""

if len(string3) == 0:
    templist1 = list(string1)
    tempList3 = list(string3)
    

string1 = string1.replace('cd'+' ','',1)
print("try")
print(string1)

string1 = "abcdef"
string2 = "cd"

#string1 = string[
spos = string1.find(string2)

del l[:]
l = list(string1)
del l[spos:spos+slen-1]
string1 = str(l)
print(string1)

string3 = "abcdefghi"
sreplace = "cde"
string3 = string3.replace(sreplace + 'f',"crap")
print(string3)

string4 = "abcdef"
string5 = "def"
print(len(string4))
print(3 + len(string5))
      
'''
stringToUse = 'abc'
stringToReplace = 'abc 123'
stringToReplace = 'abc123'
stringToReplace = '123abc'
stringToReplace = '123 abc'
stringToReplace = '123 abc 123'
stringToReplace = '123abc 123'
stringToReplace = '123 abc123'
stringToReplace = '123abc123'
stringToReplace = '123abc'
stringToReplace = '123'
stringToReplace = 'abc'
stringToReplace = ''
stringToReplace = ' '
stringToReplace = ' def'
stringToReplace = 'def '
stringToReplace = ' def '

stringToUse = ''
stringToReplace = 'abc 123'
stringToReplace = 'abc123'
stringToReplace = '123abc'
stringToReplace = '123 abc'
stringToReplace = '123 abc 123'
stringToReplace = '123abc 123'
stringToReplace = '123 abc123'
stringToReplace = '123abc123'
stringToReplace = '123abc'
stringToReplace = '123'
stringToReplace = 'abc'
stringToReplace = ''
stringToReplace = ' '
stringToReplace = ' def'
stringToReplace = 'def '
stringToReplace = ' def '

stringToUse = '987'
stringToReplace = 'abc 123'
stringToReplace = 'abc123'
stringToReplace = '123abc'
stringToReplace = '123 abc'
stringToReplace = '123 abc 123'
stringToReplace = '123abc 123'
stringToReplace = '123 abc123'
stringToReplace = '123abc123'
stringToReplace = '123abc'
stringToReplace = '123'
stringToReplace = 'abc'
stringToReplace = ''
stringToReplace = ' '
stringToReplace = ' def'
stringToReplace = 'def '
stringToReplace = ' def '
'''

stringToReplaceList =  ['abc 123', 'abc123' '123abc', '123 abc', '123 abc 123', '123abc 123', '123 abc123', '123abc123', '123abc', '123', 'abc', '',  ' ', ' def', 'def ', ' def ']
stringToUseList = ['abc 123','abc123', '123abc']

footprintsExportList =
[
[1, '987',101],
[2, 'abc 123',102],
[3, 'abc123',103],
[4, '123abc',104],
[5, '123 abc',105],
[6, '123 abc 123',106],
[7, '123abc 123',107],
[8, '123 abc123',108],
[9, '123abc123',109],
[10, '123abc',110],
[11, '123',111],
[12, 'abc',112],
[13, '',113],
[14, ' ',114],
[15, ' def',115],
[16, 'def ',116],
[17, ' def ',117],
]

formFactorFootprintsColumn = 1

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
                

