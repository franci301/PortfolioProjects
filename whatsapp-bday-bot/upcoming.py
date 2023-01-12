import logic
import datetime
def checkUpcoming():
	currentBirthdays = []
	allDates = logic.search_all()
	for i in range(len(allDates)):
		if(datetime.date.today().strftime('%d %B') in (allDates[i]['DOB'])):
			currentBirthdays.append([allDates[i]['name'],allDates[i]['DOB']])
	return currentBirthdays