vendorList = [
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

print(vendorList)
