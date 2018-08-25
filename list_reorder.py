from datetime import datetime


weekday = datetime.today().weekday()
current_hour = int((datetime.now().strftime('%H')))
business_hours = False
holidays = ["09-03-18", "11-22-18", "12-25-18"]
today = (datetime.now().strftime('%m-%d-%y'))

# Determine if current day/time is during business hours.
if weekday < 5:
    if 6 < current_hour < 18:
        if not today in holidays:
            business_hours = True

print(business_hours)

