'''
		IcsAdder.py
		
		Copyright 2010 Pål Levold		
		
    This file is part of ics2gCal.

    ics2gCal is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ics2gCal is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ics2gCal.  If not, see <http://www.gnu.org/licenses/>.
'''


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
