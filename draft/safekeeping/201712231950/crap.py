import re

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
      
print("---------------------------")
print("---------------------------")
print("---------------------------")
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

stringToReplaceList =  [
'abc 123', 'abc123', '123abc', '123 abc', '123 abc 123',
'123abc 123', '123 abc123', '123abc123', '123abc', '123',
'abc', '',  ' ', ' def', 'def ', ' Def ', 'def']

stringToUseList = ['abc 123','abc123', '123aBc']

footprintsExportList = [
[1, '987',101],
[2, 'abc 123',102],
[3, 'abc def ',103],
[4, '123def ',104],
[5, '123 def',105],
[6, 'abcdef',106],
[7, '123 def 123',107],
[8, '123def 123',108],
[9, '123 def123',109],
[10, '123defabc',110],
[11, 'def 123',111],
[12, 'defabc',112],
[13, '',113],
[14, ' ',114],
[15, ' def',115],
[16, 'def ',116],
[17, 'hi there deF hru',117],
]

footprintsExportListCopy = [
[1, '987',101],
[2, 'abc 123',102],
[3, 'abc def ',103],
[4, '123def ',104],
[5, '123 def',105],
[6, 'abcdef',106],
[7, '123 def 123',107],
[8, '123def 123',108],
[9, '123 def123',109],
[10, '123defabc',110],
[11, 'def 123',111],
[12, 'defabc',112],
[13, '',113],
[14, ' ',114],
[15, ' def',115],
[16, 'def ',116],
[17, 'hi there deF hru',117],
]

formFactorFootprintsColumn = 1

def testIt():
    innerList = []

    
    for i in range(0,len(stringToUseList)):
        for j in range(0,len(stringToReplaceList)):
            for k in range(0,len(footprintsExportList)):
#                print("stringToUse:",stringToUseList[i]," stringToReplace:"+stringToReplaceList[j]," footprintsindex: ",k)  #debug
#                replaceVendorStrings(stringToUseList[i],stringToReplaceList[j],k)
                replaceFFStrings(stringToUseList[i],stringToReplaceList[j],k)
            print("------------------------------------------------")
            print("-----------stringToUse:",stringToUseList[i]+"'  ------------stringToReplace:'"+stringToReplaceList[j]+"'---------------------")
            printList(footprintsExportList)
            del footprintsExportList[:]

            for x in range(0,len(footprintsExportListCopy)):
                del innerList[:]
                for y in range(0,len(footprintsExportListCopy[x])):
                    innerList.append(footprintsExportListCopy[x][y])
                footprintsExportList.append(innerList[:])                     
    
def printList(list):
    for i in range(0,len(list)):
        print(list[i],end=10*" ")
        print(footprintsExportListCopy[i])

def replaceVendorStrings(stringToUse, stringToReplace, footprintsListIndex):
    '''
    This function puts stringToUse  at the beginning of the string.
    If stringToReplace exists in the string then it will take it out before adding in stringToUse
    It is mindful of including a space to separate it and what word woudl be after it
    If what is after it is a whitespace then it won't add a space there.
    Regular expressions are used as it's the only way to replace strings in a case insensitive way
    '''
#    print(footprintsListIndex) #debug
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

def replaceVendorStrings_backup(stringToUse, stringToReplace, footprintsListIndex):
    '''
    This function puts stringToUse  at the beginning of the string.
    If stringToReplace exists in the string then it will take it out before adding in stringToUse
    It is mindful of including a space to separate it and what word woudl be after it
    If what is after it is a whitespace then it won't add a space there.
    '''
    tempString = ""
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
        substringPosition = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn].find(stringToReplace)
        if substringPosition != -1:
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn].replace((stringToReplace), '', 1)

        if len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) == 0:
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToUse
            tempString = ""
        elif footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][0].isspace():
            tempString = stringToUse
        else:
            tempString = stringToUse + " "
        footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = tempString + footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]

def replaceFFStrings_backup(stringToUse, stringToReplace, footprintsListIndex):
    '''
    This function puts stringToUse  at the end of the string.
    If stringToReplace exists in the string then it will take it out before adding in stringToUse
    It is mindful of including a space to separate it and what word woudl be in before it
    If what is before is a whitespace then it won't add a space there.
    '''
    tempString = ""
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
        substringPosition = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn].find(stringToReplace)
        if substringPosition != -1:
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn].replace((stringToReplace), '', 1)

        if len(footprintsExportList[footprintsListIndex][formFactorFootprintsColumn]) == 0:
            footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = stringToUse
            tempString = ""
        elif footprintsExportList[footprintsListIndex][formFactorFootprintsColumn][-1].isspace():
            tempString = stringToUse
        else:
            tempString = " " + stringToUse
        footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] = footprintsExportList[footprintsListIndex][formFactorFootprintsColumn] + tempString
    
                

testIt()
