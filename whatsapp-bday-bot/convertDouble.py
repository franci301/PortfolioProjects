import re
def convertBoth(data):
	index = re.search(r"\d",data)
	tempDob = data[index.start():].strip()
	dob = tempDob.split('/')[0]
	name = data[:index.start()].strip()
	toEdit = tempDob.split('/')[1]
	index2 = re.search(r"\d",toEdit)
	newName = toEdit[:index2.start()-1].strip()
	newDOB = toEdit[index2.start():].strip()
	return name,dob,newName,newDOB