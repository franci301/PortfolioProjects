from datetime import datetime
from datetime import date
from dateutil import relativedelta
import re

def calculate_age(birthday):
	dob = birthday[1]
	today = datetime.today().strftime('%d %B %Y')
	start = datetime.strptime(dob, "%d %B %Y")
	end =   datetime.strptime(today, "%d %B %Y")
	# Get the interval between two dates
	diff = relativedelta.relativedelta(end, start)
	#  option to display months and days too
	return diff.years
