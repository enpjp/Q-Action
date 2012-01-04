#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import csv
from django.http import HttpResponse
import unicodedata
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from urlparse import urlparse
import hashlib
import re
import datetime
import time
import urllib
import cgi

from datamodels import *


# Download CSV file of the current user set of cards
class download_csv_files(webapp.RequestHandler): 
    def get(self):

## User control -------------------------------------------------------
        user = users.get_current_user()
	#login_url = users.create_login_url(self.request.uri)
	#logout_url = users.create_logout_url(self.request.uri)
        #if user:
	#     user_nickname_or_url = user.nickname()
        #else:
	  #Un-comment  this line to prevent access to the page
         #   self.redirect( '/')


## end user control ---------------------------------------------------------------

	# Create the HttpResponse object with the appropriate CSV header.
	self.response.headers['Content-Type'] = 'text/plain'
	#self.response.headers['Content-Type'] = 'text/csv'
	#self.response.headers['Content-Disposition'] = 'attachment; filename=somefilename3.csv'
	#self.response.out.write(['First row', 'Foo', 'Bar', 'Baz'])
    	 #response = HttpResponse(mimetype='text/csv')
    	 #response['Content-Disposition'] = 'attachment; filename=somefilename.csv'

    	 #writer = csv.writer(response)



	# Now go read the database
	my_query = db.GqlQuery('SELECT * FROM place_address WHERE owner = :1 ORDER BY Cardtitle', user)
	# Need to add a check to make sure at least one page exists here
	count_my_records = 0
	if my_query:
	  # Send a header row with the field names
	  field_dict = card_definitions_v2()
	  all_field_dict = field_dict['all_fields']
	  all_field_dict.sort()
  	  row_values = []
	  # start off with the key_string

	  row_values.append("key_string")	
	  for field_name in all_field_dict:
		row_values.append(field_name)
	  #self.response.out.write(row_values)
	  for value in row_values:
		self.response.out.write(value)	
		self.response.out.write(",")		
	  self.response.out.write("\n")

	  #writer.writerow(row_values)
	  row_values = []
	  # Now we have reset the row values to empty we can proceed..
	  for my_place in my_query:
		count_my_records += 1

		row_values = []
		for field_name in all_field_dict:
			field_name_value = getattr(my_place, field_name,"")
			row_values.append(field_name_value)
	  	#self.response.out.write(row_values)
		for value in row_values:
			self.response.out.write(value)	
			self.response.out.write(",")
		self.response.out.write("\n")
		
		#row_string = ("%s" % row_values).split(",")		
		#self.response.out.write("%s\n" % row_string)



		#writer.writerow(row_values)
	  	row_values = []	
		# Now we have reset the row values to empty we can proceed to the next card in the database



	return 


