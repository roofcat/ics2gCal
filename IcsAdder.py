from icalendar import Calendar
import datetime
import GCal

class IcsAdder:
	
	def __init__(self, icsFeed, icsId, gCal, addTo, addedEventsFile, addedEventsList):
		self.iCal = Calendar.from_string(icsFeed)
		self.gCal = gCal
		self.addTo = addTo
		self.icsId = icsId
		self.addedEventsFile = addedEventsFile
		self.addedEventsList = addedEventsList
		self.addedEvents = 0
	
	def getNumAddedEvents(self):
		return self.addedEvents
		
	def addEvents(self):
		self.addedEvents = 0
		for event in self.iCal.walk('vevent'):
			
			#Check if event is allready added
			added = False
			for entry in self.addedEventsList:
				if entry[0] == self.icsId and entry[1] == event.decoded('uid'):
					added = True
				
			if added == False:	
				title = event.decoded('summary')
				content = event.decoded('description')
				location = event.decoded('location')
				start_time = event.decoded('dtstart')
				end_time = event.decoded('dtend')
				
				contentArray = content.split("\n")
				newContent = ""
				for line in contentArray:
					if line.find("http://www.tripit.com") == -1 and line != ' ' and line != '':
						newContent = newContent + line + "\n"
				content = newContent
				content = content.replace('\n','\n\n')
				content = content.replace(';','\n')
				
				add = True
				state = None
				try:
					start_time.date()
				except:
					add = False
			
				if add == True:
					self.addedEvents = self.addedEvents + 1
					state = self.gCal.InsertEvent(title, content, location, start_time, end_time, None, self.addTo)
				
				if state == 1 or add == False:
					self.addedEventsFile.write( str(self.icsId) + " " + event.decoded('uid') + "\n" )
