''''
		GCal.py
		
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
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
    
    This file is based on calendarExample.py from Google Inc. in the GData
    Python API <http://code.google.com/p/gdata-python-client/downloads/list>.
''''


try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import string
import time

import datetime
import pytz
from pytz import timezone


class GCal:

	def __init__(self, email, password):
		"""Creates a CalendarService and provides ClientLogin auth details to it.
		The email and password are required arguments for ClientLogin.  The 
		CalendarService automatically sets the service to be 'cl', as is 
		appropriate for calendar.  The 'source' defined below is an arbitrary 
		string, but should be used to reference your name or the name of your
		organization, the app name and version, with '-' between each of the three
		values.  The account_type is specified to authenticate either 
		Google Accounts or Google Apps accounts.  See gdata.service or 
		http://code.google.com/apis/accounts/AuthForInstalledApps.html for more
		info on ClientLogin.  NOTE: ClientLogin should only be used for installed 
		applications and not for multi-user web applications."""

		self.cal_client = gdata.calendar.service.CalendarService()
		self.cal_client.email = email
		self.cal_client.password = password
		self.cal_client.source = 'Google-Calendar_Python_Sample-1.0'
		self.cal_client.ProgrammaticLogin()

	def InsertEvent(self, title='Tennis with Beth', 
			content='Meet for a quick lesson', where='On the courts',
			start_time=None, end_time=None, recurrence_data=None, calendar='/calendar/feeds/default/private/full'):
		#start_time and end_time in datetime
		"""Inserts a basic event using either start_time/end_time definitions
		or gd:recurrence RFC2445 icalendar syntax.  Specifying both types of
		dates is not valid.  Note how some members of the CalendarEventEntry
		class use arrays and others do not.  Members which are allowed to occur
		more than once in the calendar or GData "kinds" specifications are stored
		as arrays.  Even for these elements, Google Calendar may limit the number
		stored to 1.  The general motto to use when working with the Calendar data
		API is that functionality not available through the GUI will not be 
		available through the API.  Please see the GData Event "kind" document:
		http://code.google.com/apis/gdata/elements.html#gdEventKind
		for more information"""
	


		if recurrence_data is not None:
			# Set a recurring event
			event.recurrence = gdata.calendar.Recurrence(text=recurrence_data)
	
		cal_tz = timezone(self.getTimeZone())
		fmt = '%Y-%m-%dT%H:%M:%S.000Z'
		
		#Give timezone
		start_time = cal_tz.localize(start_time)
		end_time = cal_tz.localize(end_time)
		
		#Convert to UTC +0
		start_time = start_time.astimezone(pytz.utc)
		end_time = end_time.astimezone(pytz.utc)
		
		#Convert to strings
		start_time = start_time.strftime(fmt)
		end_time = end_time.strftime(fmt)
	
		event = gdata.calendar.CalendarEventEntry()
		event.title = atom.Title(text=title)
		event.content = atom.Content(text=content)
		event.where.append(gdata.calendar.Where(value_string=where))	
		event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
	
		try:
			new_event = self.cal_client.InsertEvent(event, calendar)
		except:
			return -1
			#Todo error...

		return 1
		
	def getTimeZone(self):
		feed = self.cal_client.GetCalendarEventFeed()
		#print feed.timezone
		return feed.timezone.value


