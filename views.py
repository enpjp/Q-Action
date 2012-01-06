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
import unicodedata
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from urlparse import urlparse
import hashlib
import re
import time

from datetime import datetime
from datetime import date
from datetime import timedelta
import urllib
import cgi
# Import from our sub files

from datamodels import *


#What the current maximum number of accounts set this as a global at the head of the page
def max_account_limit():
	return 50

def default_pages():
	return "50"


def set_domain(arg_url):
	#if arg_url.find("q-action")>1:
	#	domain = "https://q-action.appspot.com"
	#elif arg_url.find("q-address")>1:
	#	domain = "https://q-address.appspot.com"
	#elif arg_url.find("8082")>1:
		#domain = "http://192.168.1.13:8082"
	#	domain = "http://localhost:8082"
	#else:
		#domain = "http://192.168.1.13:8082"
	#	domain = "http://localhost:8083"
	domain = arg_url
	return domain

class HomePage(webapp.RequestHandler):
    def get(self):

## User control -------------------------------------------------------
        user = users.get_current_user()
	login_url = "%s" % users.create_login_url(self.request.uri)
	logout_url = "%s" % users.create_logout_url(self.request.uri)
	#login_url.replace("/&/g","&amp;")
	#logout_url.replace("/&/g","fred")
        if user:
 	    #self.response.out.write(""" <div class="login"><!-- login text here here --> You are logged-in as: %s <a href="%s">Logout</a><br></div>  """ % (user.nickname(), logout_url) )
	    logon_message = "You are logged-in as:"
	    user_nickname_or_url = user.nickname()
	    #Need to add this for account control:
	    check_account(self)
        else:
	 # Un-comment  this line to prevent access to the page
         #   self.redirect(users.create_login_url(self.request.uri))
	 # use this line to allow none signed in access
	    logon_message = "You will need to sign in with a valid gmail account to use this software."
	    user_nickname_or_url = """<a class= "login" href="%s">Login or Register</a>""" % login_url

## end user control ---------------------------------------------------------------
	pageTitle= 'Home'

        template_values = {
	#	'my_qr_code': my_qr_code,

		'login_url' : login_url,
		'logout_url' : logout_url,
		'logon_message' : logon_message,
		'user_nickname_or_url' : user_nickname_or_url,


            	'pageTitle': pageTitle,          
        }
	path = os.path.join(os.path.dirname(__file__), 'html/index.html')
        self.response.out.write(template.render(path, template_values))

class InfoPage(webapp.RequestHandler):
    def get(self):

## User control -------------------------------------------------------
        user = users.get_current_user()
	login_url = "%s" % users.create_login_url(self.request.uri)
	logout_url = "%s" % users.create_logout_url(self.request.uri)
        if user:
 	    #self.response.out.write(""" <div class="login"><!-- login text here here --> You are logged-in as: %s <a href="%s">Logout</a><br></div>  """ % (user.nickname(), logout_url) )
	    logon_message = "You are logged-in as:"
	    user_nickname_or_url = user.nickname()
	    #Need to add this for account control:
	    account_info = check_account(self)
        else:
	 # Un-comment  this line to prevent access to the page
         #   self.redirect(users.create_login_url(self.request.uri))
	 # use this line to allow none signed in access
	    logon_message = "You will need to sign in with a valid gmail account to use this software."
	    user_nickname_or_url = """<a class= "login" href="%s">Login or Register</a>""" % login_url
## end user control ---------------------------------------------------------------
	my_url = self.request.url
	my_path = self.request.path
	# trim off the leading slash and info.
	my_clean_path = my_path[6:len(my_path)]	

	pageTitle= my_clean_path[0:(len(my_clean_path))]
	#Set some values that are used in the subscription process
	#Some might be useful on other pages too.
	days_to_end_of_subscription = "0"


	#Is logged in?
	if user:
		
		# get the user id
		user_id = user.user_id()
		login_check = "True"
		#my_cards = place_address.get(db.Key.from_path('place_address',user_id))	
		#page_not_exist(self)
		#if not my_cards:
		#Can't buy anthing until you have created a page
		#	login_check = "False"
		Date_created = account_info['Date_created']
		days_to_end_of_subscription = account_info['days_to_end_of_subscription']
		Date_created_date_string = str(Date_created)
		check_key_annual = hashlib.sha224('Annual subscription %s %s' %(user_id, Date_created_date_string )).hexdigest()
		check_key_basic_plus = hashlib.sha224('Basic Account Plus %s %s' %(user_id, Date_created_date_string )).hexdigest()
		check_key_premium = hashlib.sha224('Premium subscription %s %s' %(user_id, Date_created_date_string)).hexdigest()
	else:
		login_check = "False"
		user_id = False
		check_key_annual = "None"
		check_key_premium = "None"
		check_key_basic_plus = "None"
	

        template_values = {
	#	'my_qr_code': my_qr_code,
		'login_check' : login_check,
		'days_to_end_of_subscription' : int(days_to_end_of_subscription),
		'check_key_annual' : check_key_annual,
		'check_key_basic_plus' : check_key_basic_plus,		
		'check_key_premium' : check_key_premium,
		'login_url' : login_url,
		'logout_url' : logout_url,
		'logon_message' : logon_message,
		'user_nickname_or_url' : user_nickname_or_url,

            	'pageTitle': pageTitle,          
        }

	# We need a white list to control the valid info pages
	valid_list = ["what_can_it_do.html",
	"faq.html",
	"instructions.html",
	"subscribe.html",
	"about.html",
	"account_not_enabled.html",
	"expert.html",
	"download_complete.html",
	"upload_complete.html",
	"expired.html"]
	white_list = set(valid_list)
	path = os.path.join(os.path.dirname(__file__), 'html/%s' % my_clean_path)
	if os.path.exists(path) and my_clean_path in white_list :

        	self.response.out.write(template.render(path, template_values))
	else:
		# go to page not found if code not in the database
		pageTitle= 'Page Not Found'
        	template_values = {
			'pageTitle': pageTitle, 
			'my_url' : my_url,
			'my_path' : my_path,


        	}
		path = os.path.join(os.path.dirname(__file__), 'html/page_not_found.html')
        	self.response.out.write(template.render(path, template_values))


class BuySubscriptionPage(webapp.RequestHandler):
    def get(self):
## User control -------------------------------------------------------
        user = users.get_current_user()
	login_url = "%s" % users.create_login_url(self.request.uri)
	logout_url = "%s" % users.create_logout_url(self.request.uri)
        if user:
 	    #self.response.out.write(""" <div class="login"><!-- login text here here --> You are logged-in as: %s <a href="%s">Logout</a><br></div>  """ % (user.nickname(), logout_url) )
	    logon_message = "You are logged-in as:"
	    user_nickname_or_url = user.nickname()
	    #Need to add this for account control:
	    account_info = check_account(self)
        else:
	 # Un-comment  this line to prevent access to the page
            self.redirect(users.create_login_url(self.request.uri))
	 # use this line to allow none signed in access
	    logon_message = "You will need to sign in with a valid gmail account to use this software."
	    user_nickname_or_url = """<a class= "login" href="%s">Login or Register</a>""" % login_url
## end user control ---------------------------------------------------------------
	# Add the the account records
	#def update_annual_subscription():
	today = datetime.today()
	account_valid = account_info['account_valid']
	suspend_account = account_info['suspend_account']
	Date_created = account_info['Date_created']
	account_user_id = account_info['user_id']
	renewal_date = account_info['renewal_date']
	email = account_info['email']
	#template_values = {
	#	'account_valid' : account_valid,
	#	'suspend_account' : suspend_account,
	#	'Date_created' : Date_created,
	#	'user_id' : account_user_id,
	#	'renewal_date' : renewal_date,
#
	#}
	template_values = account_info
	#Parse the query string...
	my_query = self.request.query
	my_query_urlparse = cgi.parse_qs(my_query)

	if "key_value" in my_query_urlparse:
		key_value = my_query_urlparse["key_value"]

	else:
		key_value = None
	
	# Check the value of the key corresponds to the value of the hashed user key:
	Date_created_date_string = str(Date_created)

	check_key_annual = hashlib.sha224('Annual subscription %s %s' %(account_user_id, Date_created_date_string )).hexdigest()
	check_key_basic_plus = hashlib.sha224('Basic Account Plus %s %s' %(account_user_id, Date_created_date_string )).hexdigest()
	check_key_premium = hashlib.sha224('Premium subscription %s %s' %(account_user_id, Date_created_date_string)).hexdigest()
	try:
		real_key_value = key_value[0]
	except:
		real_key_value = "0"
	if check_key_annual == real_key_value:
		#Add a minimum of one year to the account renewal...
		try:
			if renewal_date < today:
				renewal_date = today
		except:
			renewal_date = today
		subscription_period = timedelta(365)
		renewal_date = renewal_date + subscription_period
		success_message = 'Basic Account'
		#update annual subscription
		template_values.update({'renewal_date': renewal_date})		
		template_values.update({'renewal_confirm_date': today})
		#update_account(self,template_values)
		db.run_in_transaction(update_account,self, template_values)

	elif check_key_basic_plus == real_key_value:
		#Add a minimum of one year to the account renewal...
		if renewal_date < today:
			renewal_date = today
		subscription_period = timedelta(365)
		renewal_date = renewal_date + subscription_period
		success_message = 'Basic Account Plus'
		#update annual subscription page_limit

		template_values.update({'page_limit': "1000"})	
		template_values.update({'renewal_date': renewal_date})		
		template_values.update({'renewal_confirm_date': today})
		#update_account(self,template_values)
		db.run_in_transaction(update_account,self, template_values)


	else:
		success_message = 'Fail'
		


	template_values.update({
				'success_message' : success_message,
				'key_value' : real_key_value ,
				'check_key_annual' : check_key_annual ,
				'renewal_date' : renewal_date,
				'renewal_year' : renewal_date.year,
				'renewal_month' : renewal_date.month,
				'renewal_day' : renewal_date.day,				
			 })


	



	path = os.path.join(os.path.dirname(__file__), 'html/buy_subscription.html')
	self.response.out.write(template.render(path, template_values))






# Create a first landing page to use
class create_landing_page(webapp.RequestHandler):
    def get(self):
## User control -------------------------------------------------------
        user = users.get_current_user()
	login_url = users.create_login_url(self.request.uri)
	logout_url = users.create_logout_url(self.request.uri)
        if user:
 	    #self.response.out.write(""" <div class="login"><!-- login text here here --> You are logged-in as: %s <a href="%s">Logout</a><br></div>  """ % (user.nickname(), logout_url) )
	    logon_message = "You are logged-in as:"
	    user_nickname_or_url = user.nickname()
	    #Need to add this for account control:
	    check_account(self)
        else:
	 # Un-comment  this line to prevent access to the page
            self.redirect(users.create_login_url(self.request.uri))
	 # use this line to allow none signed in access
	    logon_message = "You will need to sign in with a valid gmail account to use this software."
	    user_nickname_or_url = """<a class= "login" href="%s">Login</a>""" % login_url

## end user control ---------------------------------------------------------------
	#Only users with a valid account beyond this point:
	account_info = check_account(self)
	if not account_info:
       		self.redirect( '/info/account_not_enabled.html')
		return
	if account_info['suspend_account']:
		self.redirect( '/info/expired.html')
		return
		
	# Test if user is allowed a new contact set the default to one
	my_query = db.GqlQuery('SELECT * FROM place_address WHERE owner = :1', user)
	number_of_records = my_query.count()
	
	if number_of_records < int(account_info['page_limit']):
		# Create new contact
		Key_Name = hashlib.sha224(os.urandom(20)).hexdigest()
		Key_Name = Key_Name[0:10]
		#Test if key name exists, if it does go home!
		my_test_query = db.GqlQuery('SELECT * FROM place_address WHERE Key_Name = :1', Key_Name)
		if my_test_query.count() > 0:
			self.redirect( '/')

		#If can't create new contact drop out to a can't create error

		#These probably not needed if we set all the record spaces to null

		template_values_fields = {
			'Key_Name' : Key_Name,

        		}
		field_dict = card_definitions_v2()
		all_field_dict = field_dict['all_fields']
		my_new_template = {}
		for field_name in all_field_dict:		
			my_new_template.update({field_name : ""} )
		template_values_fields.update(my_new_template)
		template_values_fields.update( {'CardID' : 'Business'})
		html_template = lookup_html_template('Business')
		list_card_types = card_definitions_v2()
		list_card_types_dict = list_card_types['card_type_dict']
		list_name_dict = list_card_types['card_name_dict']
		list_card_types_as_list = list_card_types_dict.keys()
		list_card_types_as_list.sort()
		make_card_list = []
		for card_type in list_card_types_as_list:
			make_card_list.append([card_type,list_name_dict[card_type]])


		db.run_in_transaction(postContact_V2, self, template_values_fields)
		template_values = get_a_record_from_key(self, Key_Name)
		template_values.update({'make_card_list' : make_card_list })
		field_list = template_values
		template_values.update({'field_list' : field_list})
		#template_values.update({'list_card_types_dict' : list_card_types_dict })
		#list_card_types_dict = card_definitions_v2()
		list_card_types = card_definitions_v2()
		list_card_types_dict = list_card_types['card_type_dict']
		#if list_card_types_dict != None:
		#	list_card_types_dict.sorted()
		#list_card_types_as_list = list_card_types_dict.keys()
		#list_card_types_as_list.sort()
		list_card_types_as_list = list_card_types_dict
		template_values.update(html_template)		
		template_values.update({'list_card_types_dict' : list_card_types_dict })
		template_values.update({'list_card_types_as_list' : list_card_types_as_list })
		#Forward to the edit form
		path = os.path.join(os.path.dirname(__file__), 'html/edit_landing_page.html')
        	self.response.out.write(template.render(path, template_values))
	else:
        	self.redirect( '/')
 

# Create a form to edit an existing landing page
class edit_landing_page_form(webapp.RequestHandler):
    def get(self):
## User control -------------------------------------------------------
        user = users.get_current_user()
	login_url = users.create_login_url(self.request.uri)
	logout_url = users.create_logout_url(self.request.uri)
        if user:
 	    #self.response.out.write(""" <div class="login"><!-- login text here here --> You are logged-in as: %s <a href="%s">Logout</a><br></div>  """ % (user.nickname(), logout_url) )
	    logon_message = "You are logged-in as:"
	    user_nickname_or_url = user.nickname()
	    #Need to add this for account control:
	    check_account(self)
        else:
	 # Un-comment  this line to prevent access to the page
            self.redirect(users.create_login_url(self.request.uri))
	 # use this line to allow none signed in access
	    logon_message = "You will need to sign in with a valid gmail account to use this software."
	    user_nickname_or_url = """<a class= "login" href="%s">Login</a>""" % login_url

## end user control ---------------------------------------------------------------
	account_info = check_account(self)
	# Check to see if None has been returned if so assume account not enabled
	if not account_info:
       		self.redirect( '/info/account_not_enabled.html')
		return
	# Check to see if the account is valid
	if not account_info['account_valid'] :
       		self.redirect( '/info/account_not_enabled.html')
		return
		
	# Test if user is allowed a new card (the default is set ten)
	my_query = db.GqlQuery('SELECT * FROM place_address WHERE owner = :1', user)
	number_of_records = my_query.count()
	count_my_records = number_of_records
	Copy_Card_Key_Name = None
	if number_of_records < int(account_info['page_limit']):
		# Create new contact
		Copy_Card_Key_Name = hashlib.sha224(os.urandom(20)).hexdigest()
		Copy_Card_Key_Name = Copy_Card_Key_Name[0:10]
		#Test if key name exists, if it does go home!
		my_test_query = db.GqlQuery('SELECT * FROM place_address WHERE Key_Name = :1', Copy_Card_Key_Name)
		if my_test_query.count() > 0:
			Copy_Card_Key_Name = None




	#Get the record and assign current values to the form fields
	template_values = get_a_record_from_query(self)
	#All the fields
	field_list = template_values
	CardID = template_values['CardID']
	template_values.update({'field_list' : field_list})
	list_card_types = card_definitions_v2()
	list_card_types_dict = list_card_types['card_type_dict']
	list_name_dict = list_card_types['card_name_dict']
	list_card_types_as_list = list_card_types_dict.keys()
	list_card_types_as_list.sort()
	make_card_list = []
	# Need to check for non existant card types as we may remove card types from the list
	# If a user has a removed card type then we will set it to business
	try:
		current_card_type = list_name_dict[CardID]
	except:
		current_card_type = 'Business'


	for card_type in list_card_types_as_list:
		make_card_list.append([card_type,list_name_dict[card_type]])
	template_values.update({'make_card_list' : make_card_list })	
	template_values.update({'current_card_type' : current_card_type })	
	#'card_type_dict'
##	template_values.update({'list_card_types_dict' : list_card_types_dict })	
##	template_values.update({'card_types_dict' : list_card_types_dict[CardID] })
	template_values.update({'list_card_types_dict' : list_card_types_dict })
	template_values.update({'list_name_dict' : list_name_dict })
	template_values.update({'list_card_types_as_list' : list_card_types_as_list })
	template_values.update({'Copy_Card_Key_Name' : Copy_Card_Key_Name})
	template_values.update({'page_limit' : int(account_info['page_limit'])})	
	template_values.update({'count_my_records' : count_my_records})


	path = os.path.join(os.path.dirname(__file__), 'html/edit_landing_page.html')
        self.response.out.write(template.render(path, template_values))

# Create a work to do page
class work_to_do_page(webapp.RequestHandler):
    def get(self):
## User control -------------------------------------------------------
        user = users.get_current_user()
	login_url = users.create_login_url(self.request.uri)
	logout_url = users.create_logout_url(self.request.uri)
        if user:
 	    #self.response.out.write(""" <div class="login"><!-- login text here here --> You are logged-in as: %s <a href="%s">Logout</a><br></div>  """ % (user.nickname(), logout_url) )
	    logon_message = "You are logged-in as:"
	    user_nickname_or_url = user.nickname()
	    #Need to add this for account control:
	    check_account(self)
        else:
	 # Un-comment  this line to prevent access to the page
            self.redirect(users.create_login_url(self.request.uri))
	 # use this line to allow none signed in access
	    logon_message = "You will need to sign in with a valid gmail account to use this software."
	    user_nickname_or_url = """<a class= "login" href="%s">Login</a>""" % login_url


## end user control ---------------------------------------------------------------



	pageTitle= 'Work To Do'
        template_values = {

		'login_url' : login_url,
		'logout_url' : logout_url,
		'logon_message' : logon_message,
		'user_nickname_or_url' : user_nickname_or_url,

		'pageTitle': pageTitle, 

        }
	path = os.path.join(os.path.dirname(__file__), 'html/work_to_do.html')
        self.response.out.write(template.render(path, template_values))

# Create a page not found
class page_not_found(webapp.RequestHandler):
    def get(self):

	pageTitle= 'Page Not Found'
        template_values = {
		'pageTitle': pageTitle, 

        }
	path = os.path.join(os.path.dirname(__file__), 'html/page_not_found.html')
        self.response.out.write(template.render(path, template_values))

# Create a public landing page
class qr_code_landing_page_v1(webapp.RequestHandler):
    def get(self):

	full_url=self.request.url
	domain = set_domain(full_url)
	my_landing_page_dict_list = []
	template_values = get_a_record_from_path(self)
	if not template_values:	
		page_not_exist(self)
		return
	#Parse the query string...
	my_query = self.request.query
	my_query_urlparse = cgi.parse_qs(my_query)

	if "back_button" in my_query_urlparse:
		back_button_value = my_query_urlparse["back_button"]
		back_button = back_button_value[0]

	else:
		back_button = ""
	# This is set up user scanning while elimiating self scans
	# Will be included on the card list page.

	template_values.update({'back_button' : back_button})


	# Need to incude some action on account status 
	account_status = get_account_record(self, template_values['user_id'])
	# create a value for my place
	my_place = template_values		
	# Add my_place to my_landing_page_dict_list
	#my_landing_page_dict_list.append({'my_place' : "test"} )
	# Add my_landing_page_dict_list to the template	
	#my_template_update ={
	#	'my_landing_page_dict_list': my_landing_page_dict_list
	#	}
	# just added the line below to simplify the template

	#template_values.update(my_template_update)
	#template_values.update({'my_place' : 'test'})
	template_values.update({'domain' : domain})
	template_values.update({'Cardtitle' : template_values['Cardtitle']})	

	# Combines two dictionaries
	template_values.update(account_status)
	if ('%s' % account_status['suspend_account']) == 'True':
		self.redirect( '/info/expired.html')		
	landing_page = template_values['Auto_forward']
	# Test to see if autoforwarding is enabled go there
	if len(landing_page) > 4:
	
		self.redirect( '%s' % landing_page)
	#If not go to the landing page
	else:
		path = os.path.join(os.path.dirname(__file__), 'html/landing.html')
        	self.response.out.write(template.render(path, template_values))


# Create a private landing page
class qr_code_private_page_v1(webapp.RequestHandler):
    def get(self):
## User control -------------------------------------------------------
        user = users.get_current_user()
	login_url = users.create_login_url(self.request.uri)
	logout_url = users.create_logout_url(self.request.uri)
        if user:
 	    #self.response.out.write(""" <div class="login"><!-- login text here here --> You are logged-in as: %s <a href="%s">Logout</a><br></div>  """ % (user.nickname(), logout_url) )
	    logon_message = "You are logged-in as:"
	    user_nickname_or_url = user.nickname()
	    #Need to add this for account control:
	    check_account(self)
        else:
	 # Un-comment  this line to prevent access to the page
            self.redirect(users.create_login_url(self.request.uri))
	 # use this line to allow none signed in access
	    logon_message = "You will need to sign in with a valid gmail account to use this software."
	    user_nickname_or_url = """<a class= "login" href="%s">Login</a>""" % login_url

## end user control ---------------------------------------------------------------

	my_landing_page_dict_list = []
	template_values = get_a_record_from_query(self)
	# create a value for my place
	my_place = template_values		
	# Add my_place to my_landing_page_dict_list
	my_landing_page_dict_list.append(my_place)
	# Add my_landing_page_dict_list to the template	
	my_template_update ={
		'my_landing_page_dict_list': my_landing_page_dict_list
		}
	template_values.update({'my_place': my_place })
	
	template_values.update(my_template_update)
	path = os.path.join(os.path.dirname(__file__), 'html/qr_code_private_page.html')
        self.response.out.write(template.render(path, template_values))




# Create a list of landing pages for my account
class landing_page_list(webapp.RequestHandler):
    def get(self):
## User control -------------------------------------------------------
        user = users.get_current_user()
	login_url = users.create_login_url(self.request.uri)
	logout_url = users.create_logout_url(self.request.uri)
        if user:
 	    #self.response.out.write(""" <div class="login"><!-- login text here here --> You are logged-in as: %s <a href="%s">Logout</a><br></div>  """ % (user.nickname(), logout_url) )
	    logon_message = "You are logged-in as:"
	    user_nickname_or_url = user.nickname()
	    #Need to add this for account control:
	    check_account(self)
        else:
	 # Un-comment  this line to prevent access to the page
            self.redirect(users.create_login_url(self.request.uri))
	 # use this line to allow none signed in access
	    logon_message = "You will need to sign in with a valid gmail account to use this software."
	    user_nickname_or_url = """<a class= "login" href="%s">Login</a>""" % login_url


## end user control ---------------------------------------------------------------
	#If you get here and are not signed in you should be somewhere else!
	if not user:
		self.redirect( '/')
	display_field_in_form = []
	my_card_list = []
	html_template = {}
	my_new_template = {}
	my_landing_page_list = []
	my_landing_page_dict_list = []
	my_landing_page_dict = {}
######### This is really only needed for testing
	full_url=self.request.url
	domain = set_domain(full_url)
############################
	#If you get here and are not signed in you should be somewhere else!
	if not user:
		self.redirect( '/')
	else:
		account_info = check_account(self)
		if not account_info:
			self.redirect( '/info/expired.html')
			return
		if account_info['suspend_account']:
			self.redirect( '/info/expired.html')
			return

	
		my_query = db.GqlQuery('SELECT * FROM place_address WHERE owner = :1 ORDER BY Cardtitle', user)
		# Need to add a check to make sure at least one page exists here
		count_my_records = 0
		if my_query:
		  for my_place in my_query:
			count_my_records += 1
			# Get the values from each card so we can go to the edit page
			my_landing_page_values = []
			my_new_template = {}

			my_card = "/qr_code_private_page.html?key_string=%s&no_scan=True"  %( my_place.Key_Name_String)
			edit_my_card_url = "/edit_landing_page.html?key_string=%s&no_scan=True"  %( my_place.Key_Name_String)
			# Now add the values to the list
			#my_landing_page_list.append(my_landing_page_values)
			field_dict = card_definitions_v2()
			all_field_dict = field_dict['all_fields']

			for field_name in all_field_dict:
				field_name_value = getattr(my_place, field_name,"")
				my_new_template.update({field_name : field_name_value} )
			my_new_template.update({'my_card_url' : my_card} )
			my_new_template.update({'edit_my_card_url' : edit_my_card_url} )	
			my_landing_page_dict = my_new_template
			#my_landing_page_dict_list.append(my_new_template)
			my_landing_page_dict_list.append(my_landing_page_dict)
			card_definitions_data = card_definitions_v2()
			card_types_list_members_dict = card_definitions_data['card_dict_members_list']
			CardID = 'Business'
			CardID = my_new_template['CardID']			
			if CardID not in  card_types_list_members_dict :
				CardID = 'Business'
 			card_types_list_members =  card_types_list_members_dict[CardID]    		
			html_template = lookup_html_template(CardID)
			display_field_in_form = []
			edit_field_in_form = []	
			my_card_list = []		
			display_field_in_form.append(['Card Type', 'CardID' , CardID, 'text'  ])
			# This should give a list of the fields to display
			for field_type in card_types_list_members:

				name_of_field = field_type[0]
				description_of_field = field_type[1]
				value_of_field = my_landing_page_dict[name_of_field]
				text_or_visible = "text"
				display_field_in_form.append([description_of_field, name_of_field , value_of_field, text_or_visible  ])
				edit_field_in_form.append([description_of_field, name_of_field , value_of_field, text_or_visible  ])
			my_card_list.append(display_field_in_form)					
			my_landing_page_list.append([display_field_in_form, my_card])	
		#if ('%s'%account_info['suspend_account']) == 'False':
		#	boolean = True
		#else: 
		#	boolean = False	
		boolean = True	
		pageTitle= 'My List of Landing Pages'

		days_to_end_of_trial = account_info['days_to_end_of_trial']
		days_to_end_of_subscription = account_info['days_to_end_of_subscription']
        	template_values = {
			'boolean' : boolean,
			'pageTitle': pageTitle, 
			'login_url' : login_url,
			'logout_url' : logout_url,
			'logon_message' : logon_message,
			'user_nickname_or_url' : user_nickname_or_url,
			# This is a list of the fields to display
			'my_landing_page_list' : my_landing_page_list,
			'my_card_list' : my_card_list,
			'count_my_records' : count_my_records,
			# Not really needed ..
			'my_landing_page_dict_list' : my_landing_page_dict_list,
			#'page_limit' : account_info['page_limit'],
			'page_limit' : int(account_info['page_limit']),
			'days_to_end_of_trial' : abs(days_to_end_of_trial),
			'days_to_end_of_subscription' : abs(days_to_end_of_subscription),						 

			#'Web_url' : Web_url,

        		}
			# Combines two dictionaries
		template_values.update(html_template)
		template_values.update(account_info)
		template_values.update( { 'my_new_template' : my_new_template })
		# This is the list used to generate the landing pages
		template_values.update({ 'display_field_in_form': display_field_in_form })		
		path = os.path.join(os.path.dirname(__file__), 'html/landing_page_list.html')
        	self.response.out.write(template.render(path, template_values))

#Create an update data post action
class update_contact(webapp.RequestHandler): 
   def post(self): 

	
	
	template_fields = update_contact_get_fields(self)
	db.run_in_transaction(postContact_V2,self, template_fields)

	pageTitle= 'New Card Created'
        template_values = {
	#	'my_qr_code': my_qr_code,
            	'pageTitle': pageTitle,          
        }
	#self.redirect( '/qr_code_private_page.html?key_string=%s' % template_fields['Key_Name'])
	self.redirect( '/edit_landing_page.html?key_string=%s&no_scan=True' % template_fields['Key_Name'])
#		path = os.path.join(os.path.dirname(__file__), 'html/edit_landing_page.html')

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
	#self.response.headers['Content-Type'] = 'text/plain'
	self.response.headers['Content-Type'] = 'text/csv'
	#self.response.headers['Content-Disposition'] = 'attachment; filename=q-action_csv_file.csv'
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

	  row_values.append("'key_string'")	
	  for field_name in all_field_dict:
		row_values.append("'%s'" % field_name)
	  #self.response.out.write(row_values)
	  for value in row_values:
		self.response.out.write(value)	
		self.response.out.write(",")		
	  self.response.out.write("\n")

	  #writer.writerow(row_values)
	  row_values = []
	  
	  # Now we have reset the row values to empty we can proceed..
	  for my_place in my_query:

		#run in transaction mode...		
			row_values = []
			Key_Name_String = getattr(my_place,"Key_Name_String","")
			row_values.append("'%s'" % Key_Name_String)

			for field_name in all_field_dict:
				field_name_value = getattr(my_place, field_name,"")
				row_values.append("'%s'" % field_name_value)
			#self.response.out.write(row_values)
			for value in row_values:
				self.response.out.write(value)	
				self.response.out.write(",")
			self.response.out.write("\n")
			row_values = []	

		# Now we have reset the row values to empty we can proceed to the next card in the database


        #self.redirect( '/info/download_complete.html')
	return 

# Select a file to upload to the database
class ChooseFileToUpload(webapp.RequestHandler):
    def get(self):

	pageTitle= 'Upload CSV File'
        template_values = {
            	'pageTitle': pageTitle, 
        
        }
	path = os.path.join(os.path.dirname(__file__), 'html/choose.html')
        self.response.out.write(template.render(path, template_values))

# Post the CSV file to the database
class PostToDatabase_V1(webapp.RequestHandler): 
   def post(self):
## User control -------------------------------------------------------
        user = users.get_current_user()
	login_url = users.create_login_url(self.request.uri)
	logout_url = users.create_logout_url(self.request.uri)
       	if user:
 	    #self.response.out.write(""" <div class="login"><!-- login text here here --> You are logged-in as: %s <a href="%s">Logout</a><br></div>  """ % (user.nickname(), logout_url) )
	    #logon_message = "You are logged-in as:"
	    	user_nickname_or_url = user.nickname()
       	else:
			
	 # Un-comment  this line to prevent access to the page	
	 # Only use this facility if you are signed in!
		self.redirect(users.create_login_url(self.request.uri))
	 # use this line to allow none signed in access
	     #logon_message = "You will need to sign in with a valid gmail account to use this software."
	     #user_nickname_or_url = """<a class= "login" href="%s">Login</a>""" % login_url
## end user control ---------------------------------------------------------------

	def clean_data(arg_row):
		rowList = []
		#my_row = arg_row.split(",")
		for index, item in enumerate(arg_row):
			#Clean out the non ASCII Characters
			if index == 0:
				item_clean =''.join([x for x in item if ord(x) < 128])
			else:
				item_clean =''.join([x for x in item if ord(x) < 128])	
			rowList.append( item_clean)
	 	return 	rowList
		
	# Create a working list to hold the updated list
	#speciesList =[]
	# Create a list to hold each row of the species list as we read it from the csv file
	#rowList = [0]*6

	# Go get the csv file
     	csvFile=self.request.get('csv')
	#Count the rows. Start at 0 as the first row should be the field names
	row_counter = 0
	header_row = []
	data_row = []
	success_row = []
	template_values = {}
	data_dictionary = {}
     	#fileReader = csv.reader(csvFile.split("\n"))
	#fileReader = csv.reader(csvFile, delimiter=",", quotechar="'")
	#fileReader_dict = csv.DictReader(csvFile, delimiter=",", quotechar="'")
	fileReader_dict = csv.DictReader(csvFile.split("\n"), delimiter=",", quotechar="'",dialect='excel')
	fileReader_dict_copy = csv.DictReader(csvFile.split("\n"), delimiter=",", quotechar="'",dialect='excel')
	data_dictionary.update({'csv_data': fileReader_dict})
	# For some reason it was reading in UTF-7 last night and this morning in ASCII. Not sure what I have done differently
	# unless it was me editing the spreadsheet.
	#fileReader_dict.decode( 'unicode-escape' ).encode( 'ascii' )
	#.decode( 'unicode-escape' ).encode( 'ascii' )
    
	# This functionality has been built into postContact_V3
	# The transactional posting of the data has also been built in
	# The fileReader_dict is a list of dictionaries encoding the csv file
	#for page in fileReader_dict:
	for key, page in enumerate(fileReader_dict):
	#for page in fileReader_dict:
		success_dict = postContact_V3(self,page)
		success_row.append(success_dict)
			#template_values.update( data_dictionary )
			#template_values.update( {'fileReader' : fileReader} )
			# Now we can post the data

	# Display the uploaded cards.....This acts directly on the dictionary so we can use another dictionary to 
	#record the success of the upload.
	template_values.update( {'fileReader_dict' : fileReader_dict_copy} )	
	template_values.update( {'success_row' : success_row } )	
	path = os.path.join(os.path.dirname(__file__), 'html/upload_complete_test.html')
        self.response.out.write(template.render(path, template_values))



# Edit my account details
class my_account(webapp.RequestHandler):
    def get(self):
## User control -------------------------------------------------------
        user = users.get_current_user()
	login_url = users.create_login_url(self.request.uri)
	logout_url = users.create_logout_url(self.request.uri)
        if user:
 	    #self.response.out.write(""" <div class="login"><!-- login text here here --> You are logged-in as: %s <a href="%s">Logout</a><br></div>  """ % (user.nickname(), logout_url) )
	    logon_message = "You are logged-in as:"
	    user_nickname_or_url = user.nickname()
	    #Need to add this for account control:
	    check_account(self)
        else:
	 # Un-comment  this line to prevent access to the page
            self.redirect(users.create_login_url(self.request.uri))
	 # use this line to allow none signed in access
	    logon_message = "You will need to sign in with a valid gmail account to use this software."
	    user_nickname_or_url = """<a class= "login" href="%s">Login</a>""" % login_url

## end user control ---------------------------------------------------------------
	account_info = check_account(self)
	# Check to see if None has been returned if so assume account not enabled
	if not account_info:
       		self.redirect( '/info/account_not_enabled.html')
		return
	# Check to see if the account is valid
	if not account_info['account_valid'] :
       		self.redirect( '/info/account_not_enabled.html')
		return
	template_values = account_info	
	path = os.path.join(os.path.dirname(__file__), 'html/my_account.html')
        self.response.out.write(template.render(path, template_values))

############################################################################################
###########################################################################################
###########################################################################################
## Function definitions
###########################################################################################
###########################################################################################
###########################################################################################




#Create a template value list containing the contents of one record
# Used to display and edit forms
def get_a_record_from_path(self):
	my_url = self.request.url
	my_path = self.request.path
	# trim off the leading slash.
	my_clean_path = my_path[1:len(my_path)]	
	# Sorting out the syntax was a bit of a mission, note the db. and the use of key from path

	#my_key = hashlib.sha224("Nobody inspects the spammish repetition").hexdigest()
	my_key = my_clean_path
	#Need to prevent null keys being a problem
	if len(my_key) < 2:
	 self.redirect( '/')
	
	template_list = get_a_record_from_key(self, my_key)
	return template_list

# Get a record from a query 
def get_a_record_from_query(self):
	my_url = self.request.url
	my_path = self.request.path
	# Need to parse out the query string
	# This means that you will arrive at this page with an URL with a query qualifier
	my_query = self.request.query
	my_query_urlparse = cgi.parse_qs(my_query)
	if "key_string" in my_query_urlparse:
		my_key_value = my_query_urlparse["key_string"]
		my_key = my_key_value[0]
	else:
		my_key = "No Key"

	#Need to prevent null keys being a problem
	if len(my_key) < 2:
	 self.redirect( '/')	
	template_list = get_a_record_from_key(self, my_key)
	#template_list.update({'back_button' : back_button})
	return template_list




# Get a record from a key
def get_a_record_from_key(self, arg_my_key):
## User control -------------------------------------------------------
        user = users.get_current_user()
	login_url = users.create_login_url(self.request.uri)
	logout_url = users.create_logout_url(self.request.uri)
        if user:
 	    #self.response.out.write(""" <div class="login"><!-- login text here here --> You are logged-in as: %s <a href="%s">Logout</a><br></div>  """ % (user.nickname(), logout_url) )
	    logon_message = "You are logged-in as:"
	    user_nickname_or_url = user.nickname()
        else:
	 # Un-comment  this line to prevent access to the page
         #   self.redirect(users.create_login_url(self.request.uri))
	 # use this line to allow none signed in access
	    logon_message = "You will need to sign in with a valid gmail account to use this software."
	    user_nickname_or_url = """<a class= "login" href="%s">Login</a>""" % login_url


## end user control ---------------------------------------------------------------
	# Will need to change the way the record is found
	my_url = self.request.url
	my_path = self.request.path
	my_query = place_address.get(db.Key.from_path('place_address',arg_my_key))	
	#page_not_exist(self)
	if my_query is None:
		#page_not_exist(self)
		return None
	else:
		# this costs us a write to the database
		no_scan_string_dict = increment_page_counter(self,arg_my_key)
		# Go get all the fields
		field_dict = card_definitions_v2()
		all_field_dict = field_dict['all_fields']
		my_new_template = {}
		for field_name in all_field_dict:
			field_name_value = getattr(my_query, field_name,"")
			my_new_template.update({field_name : field_name_value} )	

		# go to contact page
		# Collect up the record parts for assembly into microformats
		First_Name = my_query.First_Name
		Middle_Name = my_query.Middle_Name
		Last_Name = my_query.Last_Name
		#Organisation = my_query.Organisation
		user_id = my_query.user_id

		Web_url = my_query.Web_url
		Text_message = my_query.Text_message
		Text_message = mark_up_coder(my_query.Text_message)
		Auto_forward = my_query.Auto_forward
		Google_analytics = my_query.Google_analytics
		Stat_counter = my_query.Stat_counter
		# Extra fields here:
		CardID = my_query.CardID
		# Build up a title for the page
		First_initial = ""
		Second_initial = ""
		if len(First_Name) >0:
			First_initial = "%s." % First_Name[0]
		if len(Middle_Name) >0:
			Second_initial = "%s." % Middle_Name[0]	
		domain = set_domain(self.request.url)
		Key_Name = arg_my_key
		my_qr_data = "%s/%s"  %( domain,Key_Name)




		# Need to check the status of the associated account
		my_id_to_check = my_query.user_id
		account_details = get_account_record(self, my_id_to_check)
		# If the account is suspended go home
		if account_details['suspend_account']:
			self.redirect( '/')	
	
		my_qr_code = "https://chart.googleapis.com/chart?chs=150x150&amp;cht=qr&amp;chl=%s" % my_qr_data
		edit_my_record = "/edit_landing_page.html?key_string=%s"  %( Key_Name)
			
		zero = 0

		# Get the fields dictionary
		card_definitions_data = card_definitions_v2()
		card_types_list = card_definitions_data['card_dict_members']		
		card_types_dict = card_definitions_data['card_type_dict']
		card_types_list_all = card_definitions_data['card_list_members']
		field_widget = card_definitions_data['field_widget']
		card_name_dict = card_definitions_data['card_name_dict']
		
		all_fields = card_definitions_data['all_fields']
		card_types_list_members_dict = card_definitions_data['card_dict_members_list']
		#CardID = 'Business'
 		#CardID = my_new_template['CardID']
		if CardID not in card_types_list_members_dict  :
			CardID = 'Business'
		
 		#card_types_list_members =  card_types_list_members_dict[CardID]
		CardID_s = "%s" % CardID
		card_types_list_members =  card_types_list_members_dict[CardID] 
		if CardID in card_types_dict:	  			
			fields_to_use = card_types_dict[CardID]
			card_name = card_name_dict[CardID]
		else:
			CardID = 'Business'
			fields_to_use = card_types_dict['Business']
			card_name = 'Business'
		html_template = lookup_html_template(CardID)
		#card_types_list_members = card_types_list_all[CardID]
		#card_types_dict_list_members = card_types_dict_list[CardID]
		#pageTitle= 'Contact Page for %s %s %s' %(First_initial, Second_initial, Last_Name)
		pageTitle = CardID
        	template_values = {
			'Key_Name' : Key_Name,
			'user_id' : user_id,
			'edit_my_record' : edit_my_record,
			'login_url' : login_url,
			'logout_url' : logout_url,
			'logon_message' : logon_message,
			'user_nickname_or_url' : user_nickname_or_url,
			'pageTitle': pageTitle, 
			'my_url' : my_url,
			'my_path' : my_path,
			'Web_url' : Web_url,
			'Text_message' : Text_message,
			'Auto_forward' : Auto_forward,
			'my_qr_code' : my_qr_code,
			'my_qr_data' : my_qr_data,
			'zero' : zero,
			'Google_analytics' : Google_analytics,
			'Stat_counter' : Stat_counter,
			'CardID' : CardID,
			'card_name' : card_name,
			'domain' : domain
    		    	}
		template_values.update(my_new_template)
		template_values.update(no_scan_string_dict)
		all_template_values = template_values
		edit_field_in_form = []
		hidden_edit_field_in_form = []
		display_field_in_form = {}
		# card_types_list_members should be from 'card_dict_members_list'
		for field_type in card_types_list_members:
			name_of_field = field_type[0]
			description_of_field = field_type[1]
			value_of_field = template_values[name_of_field]
			text_or_visible = "text"
			if name_of_field in field_widget:
				field_widget_type = field_widget[name_of_field]
				if CardID == 'Mini_web':
					mini_web_list = get_mini_web_list(self,my_id_to_check)
					template_values.update({'mini_web_list' : mini_web_list })

					if value_of_field in mini_web_list:
						page_title_lookup = mini_web_list[value_of_field]
						if len(value_of_field) < 1:
							page_title_lookup = "No Title!"							
					else:
						if len(value_of_field) < 1:
							page_title_lookup = "No Title!"		
						else:
							page_title_lookup = "No Title!"				


			else:
				field_widget_type = 'text'
				page_title_lookup = "No Title!"
				
			edit_field_in_form.append([description_of_field, name_of_field , value_of_field, text_or_visible, field_widget_type, page_title_lookup ])
			display_field_in_form.update({name_of_field :value_of_field })
		for field_type in all_template_values :
			if field_type not in card_types_dict[CardID]:
				name_of_field = field_type
				description_of_field = ""
				value_of_field = template_values[name_of_field]
				text_or_visible = "hidden"
				hidden_edit_field_in_form.append([description_of_field, name_of_field , value_of_field, text_or_visible  ])
		template_values.update(html_template)
		 
		template_values.update({'field_widget' : field_widget })
		template_values.update({'display_field_in_form' : display_field_in_form })			
		template_values.update({'hidden_edit_field_in_form' : hidden_edit_field_in_form })		
		template_values.update({'edit_field_in_form' : edit_field_in_form })
		template_values.update({'all_template_values' : all_template_values })
		template_values.update({'fields_to_use' : fields_to_use })
		template_values.update({'card_types_list' : card_types_list })
		template_values.update({'card_types_dict' : card_types_dict[CardID] })
		template_values.update({'all_fields' : all_fields })
		template_values.update({'card_types_list_members' : card_types_list_members })

		return template_values







# Put the data read and write modules here to make is easier to update
def postContact_V2(self,arg_data_fields):

	user = users.get_current_user()
	user_id = user.user_id()
	field_dict = arg_data_fields
		
	my_place = place_address(key_name='%s' % field_dict['Key_Name'])
	my_place.user_id = user_id 
	my_place.Key_Name_String = field_dict['Key_Name']
	# Go set all the attributes
	field_dict_all = card_definitions_v2()
	all_field_dict = field_dict_all['all_fields']
	#my_new_template = {}
	for field_name in all_field_dict:
		#field_name_value = getattr(my_query, field_name,"")
		#my_new_template.update({field_name : field_name_value} )
		setattr(my_place, field_name, field_dict[field_name])

	my_place.put()


# This updated post module has better error checking
# It looks for a match between the current user and the key
def postContact_V3(self,arg_data_fields):
  	def update_csv_fields(arg_local_fields, arg_data_query):
		for field_name in field_dict:
			# Clear out all non ASCII characters
			field_name = field_name.decode( 'unicode-escape' ).encode( 'ascii' )
			field_clean =''.join([x for x in field_dict[field_name] if ord(x) < 128])
			setattr(arg_data_query, field_name, field_clean)
		arg_data_query.put()
			
	status_dict = {}
	user = users.get_current_user()
	user_id = user.user_id()
	field_dict = arg_data_fields
	# should this be:
	try:
	#if True:
		my_place = place_address.get(db.Key.from_path('place_address',field_dict['key_string']))

		
		# if the record exists then try to update it
		if my_place:	
		
			# Make sure the user who owns the record and the uploader have the same id!
			user_user_id = '%s' % my_place.user_id 
			if user_id == user_user_id:
				db.run_in_transaction(update_csv_fields,field_dict,my_place)
	
				field_dict.update({"success" : "Card ID: %s successfuly uploaded! " % field_dict['key_string']   })
				field_dict.update({"success_class" : "success"  })
			
			else:
				field_dict.update({"success" : "Card ID: %s not uploaded: Record belongs to another user! " % field_dict['key_string']   })
				field_dict.update({"success_class" : "fail"  })

		else:
		# If the record does not exist then grumble

			field_dict.update({"success" : "Card ID: %s not uploaded: Record does not exist!" % field_dict['key_string']   })
			field_dict.update({"success_class" : "fail"  })

	except KeyError:
		field_dict.update({"success" : "The key_string is not valid. You must not edit the first row. You may have used the wrong character set when editing."  })
		field_dict.update({"success_class" : "fail"  })
	
	
	except:
		field_dict.update({"success" : "Your csv file is corrupted so it cannot be processed"   })
		field_dict.update({"success_class" : "fail"  })
	
	status_dict = field_dict

	return status_dict






def update_contact_get_fields(self): 


	user = users.get_current_user()
	field_dict = card_definitions_v2()
	all_field_dict = field_dict['all_fields']
	my_new_template = {}
	for field_name in all_field_dict:
		#field_name_value = getattr(my_query, field_name,"")
		my_new_template.update({field_name : self.request.get(field_name)} )	

	template_data_fields = {
		#PlaceName=self.request.get('PlaceName')
	'Key_Name' : self.request.get('Key_Name'), 
	'user' : users.get_current_user(),	

	}
	template_data_fields.update(my_new_template)


 	return template_data_fields

# Pass a dictionary to post_contract rather than loads of args

def check_account(self):

	#returns true if the account is valid and enabled
	#returns false if it is valid and disabled
	#creates an account with a status dependent upon the limit imposed and returns
	#true or false depending upon status
	user = users.get_current_user()

	# we need to see if an account exists by raising a query on the account manager database
	if user:
		my_user_id = user.user_id()
		account_details = get_account_record(self, my_user_id)
	else:
		#Make sure we only allow properly signed in users to proceed by returning None if they are not signed in.
		return None
	return account_details

#This does the actual creation of an account with a status dependent upon the limit imposed and returns
def get_account_record(self, my_user_id):
	#What is our limit? set this as a global at the head of the page
	free_trial_end = 0
	today = datetime.today()
	user_id = my_user_id
	max_accounts = max_account_limit()
	default_number_of_pages = default_pages()
	user = users.get_current_user()	
	my_account_query = account_manager.get(db.Key.from_path('account_manager',user_id))
	#my_query = place_address.get(db.Key.from_path('place_address',arg_my_key))
	if my_account_query is None:
		account_exist = False
	else:
		account_exist = True	
	#If the account exists we need to check if it is valid
	# as we might disable accounts if there is a problem
	new_account = False
	#If it is valid return status of account
	if account_exist:
		#No we don't need to create an account		
		page_limit = my_account_query.page_limit
		#create_account = my_account_query.account_valid
		#If any of the following conditions apply return None
		#If the account has been suspended:
		account_valid = my_account_query.account_valid
		if ('%s' %my_account_query.suspend_account) == 'True':
			suspend_account = True
		else:
			suspend_account = False

		renewal_date = my_account_query.renewal_date			
		free_trial_end = my_account_query.free_trial_end
		Date_created = my_account_query.Date_created
		user_id = my_account_query.user_id
		email = my_account_query.email
		nickname = my_account_query.nickname
		owner = my_account_query.owner
		opt_in_to_contact = my_account_query.opt_in_to_contact


	else:
		new_account = True
		suspend_account = False
		renewal_date = datetime.now()
		Date_created = datetime.now()
		opt_in_to_contact = False
		free_trial_end = datetime.today()
		# Need some logic around the free trial - if december then increment the year and set the month to 1
		free_trial_period = timedelta(30)
		free_trial_end = free_trial_end + free_trial_period
		user_id = user.user_id()
		email = user.email()
		nickname = user.nickname()
		#owner = user.owner()		
		#If the account does not exist are we above our limit?
		#Need to watch the expense of this query as the number of users gets large
		#It has been set to get the keys only here.
		page_limit = default_number_of_pages
		query_count = db.Query(account_manager,True)
		if query_count.count() >= int(max_accounts) :
			account_valid = False
			# If we create an account but mark it false we must rememer to give a suitable free period.
			# However, we would expect this to be a fairly rare occurance.
			
		else:		
			account_valid = True	
			#If all is well create the account and return true
	try:
		days_to_end_of_trial = (free_trial_end - today)
	except:
		days_to_end_of_trial = (today - today)
	try:
		days_to_end_of_subscription = (renewal_date - today)
	except:
		days_to_end_of_subscription = (today - today)
	if not opt_in_to_contact:
		opt_in_to_contact = False
	# It is better to create an account and mark it false rather than not to create it at all.
	# Using templates makers it easier to manage the database
	account_template = { 
		'new_account' : new_account,
		'account_valid' : account_valid,
		'page_limit' : page_limit,
		'suspend_account' : suspend_account,
		'renewal_date' : renewal_date,
		'Date_created' : Date_created,
		'free_trial_end' : free_trial_end,
		'days_to_end_of_trial' : days_to_end_of_trial.days,
		'days_to_end_of_subscription' : days_to_end_of_subscription.days,
		'user_id' : user_id,
		'email' : email,
		'nickname' : nickname,
		'opt_in_to_contact' : opt_in_to_contact,
		#'owner' : owner

		}

	# Now for a bit of status checking...

	if days_to_end_of_subscription.days < 0 :
		account_template.update({'suspend_account':True })
	if days_to_end_of_trial.days < 0:
		account_template.update({'suspend_account': True })
	if days_to_end_of_trial.days > 0:
		account_template.update({'suspend_account': False })
	if days_to_end_of_subscription.days > 0 :
		account_template.update({'suspend_account':False })

	# But if the account is already suspended don't care about subscription.....
	#if suspend_account == True:
	#	account_template.update({'suspend_account':True })

	#If it is a new account
	if new_account :
		db.run_in_transaction(create_account,self, account_template)
	else: 
		db.run_in_transaction(update_account,self, account_template)

	return account_template

def update_account(self,arg_account_template):
	
	# The account template already contains the user_id
	user = users.get_current_user()
	#user_id = user.user_id()
	user_id = arg_account_template['user_id']
	email = arg_account_template['email']
	nickname = arg_account_template['nickname']
	account_manager_records = account_manager.get(db.Key.from_path('account_manager',user_id))
	if not account_manager_records:
		my_user_key = user.user_id()
		account_manager_records = account_manager(key_name='%s' % my_user_key)
		account_manager_records.page_limit = arg_account_template['page_limit']
		account_manager_records.nickname = nickname
		account_manager_records.email = email
		account_manager_records.user_id = user_id
		account_manager_records.suspend_account = arg_account_template['suspend_account']		


	#if 'new_account' in arg_account_template:	
	#	if arg_account_template['new_account']:
			
			#account_manager_records.owner = db.UserProperty(auto_current_user_add=True)
			
    			#account_manager_records.Date_created = db.DateTimeProperty(auto_now_add=True)
	#	else:
			# Must get the account record
	#		account_manager_records = account_manager.get(db.Key.from_path('account_manager',user_id))
	#if 'account_valid' in arg_account_template:
	#	account_manager_records.account_valid  = arg_account_template['account_valid']
	if 'renewal_date' in arg_account_template:
		account_manager_records.renewal_date = arg_account_template['renewal_date']
	if 'renewal_confirm_date' in arg_account_template:
		account_manager_records.renewal_confirm_date = arg_account_template['renewal_confirm_date']
	if 'page_limit' in arg_account_template:
		account_manager_records.page_limit = arg_account_template['page_limit']




	account_manager_records.suspend_account = arg_account_template['suspend_account']
	account_manager_records.put()

def create_account(self,arg_account_template):
	user = users.get_current_user()
	my_user_key = user.user_id()
	account_manager_records = account_manager(key_name='%s' % my_user_key)
			#account_manager_records.owner = db.UserProperty(auto_current_user_add=True)
	account_manager_records.page_limit = arg_account_template['page_limit']
	account_manager_records.nickname = user.nickname()
	account_manager_records.email = user.email()
	account_manager_records.user_id = user.user_id()
	account_manager_records.suspend_account = arg_account_template['suspend_account']
    			#account_manager_records.Date_created = db.DateTimeProperty(auto_now_add=True)
	account_manager_records.account_valid  = arg_account_template['account_valid']
	account_manager_records.renewal_date = arg_account_template['renewal_date']
	account_manager_records.free_trial_end = arg_account_template['free_trial_end']
	account_manager_records.suspend_account = arg_account_template['suspend_account']
	account_manager_records.put()

def mark_up_coder(arg_string):
	#Make sure the string is escaped
	escape_mark_up_list = {
		"/&/g" 	: "&amp;",	
		"/": "&frasl;",
		"<" 	: "&lt;",
		">"  	: "&gt;"
			} 
	new_string = arg_string
	for k, v in escape_mark_up_list.iteritems():
		new_string = re.sub(k, v, new_string) 
		#new_string = new_string.replace("%s" % k,"%s" % v)
		#arg_string.replace("/&/g","&amp;")
	replace_mark_up_list = {
		"&lt;br &frasl;&gt;" 	: "<br />",
		
			} 
	for k, v in replace_mark_up_list.iteritems():
		new_string = re.sub(k, v, new_string) 
	
  	return new_string



def card_definitions_v2():
	card_dict_members_list = {}
	card_dict_members = {}
	card_list_members =[]
	Business = {}
	Business_list = [
		['Cardtitle', 'Card Title'],
		['Persontitle' , 'Title (Mr, Ms, Dr, Rev)'],
		['First_Name' , 'First name'],
		['Middle_Name' , 'Middle name or initial'],
		['Last_Name' , 'Family name'],
		['Qualifications' , 'Qualifications'],
		['Type' , 'Job Title'],
		['Organisation' , 'Company or Organisation'],
		['W_address_line_1' , 'Address line 1'],
		['W_address_line_2' , 'Address line 2'],
		['W_address_Post_Town' , 'Post_Town'],
		[ 'W_address_County' , 'County' ],
		['W_address_Country' , 'Country'],
		['W_address_Post_Code' , 'Post Code'],
		['Tel1' , 'Work Tel'],
		['Tel2' , 'Mobile Tel'],
		['Tel3' , 'Home Tel'],
		['Email_address' , 'Work email'],
		['Email2' , 'Home email'],
		['Web_url' , 'Website'],
		['URL2' , 'Alternative web site'],
		['URLsocialnets' , 'Social network and conferencing names'],
		['Text_message' , 'Marketing message'],
		['scan_counter' , "Scan counter" ],	
		#['Sparebusiness1' , '(None - spare field)'],
		#['Sparebusiness2' , '(None - spare field)'],
		]
	for  field in Business_list:
		Business.update({field[0] :field[1] })	
	card_dict_members_list.update({'Business' : Business_list})	
	card_dict_members.update({'Business' : Business})
	card_list_members.append({'Business' : Business_list})
	Membership = {}
	Membership_list = [
		['Cardtitle', 'Card Title'],

		#['Reminderdate' , 'Send expiry reminder to me on'],
		['Organisation' , 'Organisation or branch'],
		['Web_url','Organisation Website'],
		['Persontitle' , 'Title (Mr, Ms, Dr, Rev)'],
		['First_Name' , 'First name'],
		['Middle_Name' , 'Middle name or initial'],
		['Last_Name' , 'Family name'],
		['Type' , 'Type of membership'],
		['ItemID' , 'Membership ID or number'],
		['Endate' , 'Membership expires'],
		['Startdate' , 'Member since'],
		['Text_message' , 'Notes'],
		['URL2','On-line Member Account'],
		['scan_counter' , "Scan counter" ],
		#['LabelID' , 'Label to print with code'],
		#['Sparemembership1' , '(None - spare field)'],
		#['Sparemembership2' , '(None - spare field)'],
		]
	for  field in Membership_list:
		Membership.update({field[0] :field[1] })	
	card_dict_members_list.update({'Membership' : Membership_list})	
	card_dict_members.update({'Membership' : Membership})
	card_list_members.append({'Membership' : Membership_list})
	Service = {}
	Service_list = [
		['Cardtitle', 'Card Title'],
		#['Reminderdate' , 'Send email reminder on'],
		['Make' , 'Product or service name'],
		['Type' , 'Model or type'],
		['Datecreated' , 'Date made'],
		['Datewarrexp' , 'Warranty ends'],
		['Startdate' , 'Last service done'],
		['Endate' , 'Next Service due'],
		['Organisation' , 'Service organisation or engineer name'],
		['Tel1' , 'Contact number'],
		['Tel2' , 'Alternate number'],
		['Email_address' , 'Contact email'],
		['Web_url' , 'Contact web site'],
		['Text_message' , 'Description and notes'],
		['scan_counter' , "Scan counter" ],
		#['LabelID' , 'Label to print with code'],
		#['Spareservice1' , '(None - spare field)'],
		#['Spareservice2' , '(None - spare field)'],
		]
	for  field in Service_list:
		Service.update({field[0] : field[1] })	
	card_dict_members_list.update({'Service' : Service_list})	
	card_dict_members.update({'Service' : Service})
	card_list_members.append({'Service' : Service_list})
	Offer = {}
	Offer_list = [	
		['Cardtitle', 'Card Title'],
		['Make' , 'Item make'],
		['Type' , 'Item model'],
		['Offers' , 'Offer'],
		['Text_message' , 'Description'],
		['Web_url' , 'Buy now button'],
		['scan_counter' , "Scan counter" ],
		#['LabelID' , 'Label to print with code'],
		#['Spareoffer1' , '(None - spare field)'],
		#['Spareoffer2' , '(None - spare field)']
		]
	for  field in Offer_list:
		Offer.update({field[0] : field[1] })
	card_dict_members_list.update({'Offer' : Offer_list})		
	card_dict_members.update({'Offer' : Offer})
	card_list_members.append({'Offer' : Offer_list})
	Event = {}
	Event_list = [
		['Cardtitle', 'Card Title (Event name)'],
		['Day' , 'Date'],
		['Itemlist' , 'Time, item, location'],
		['scan_counter' , "Scan counter" ],
		#['LabelID' , 'Label to print with code'],
		#['Spareevent1' , '(None - spare field)'],
		#['Spareevent2' , '(None - spare field)'],
		]	
	for  field in Event_list:
		Event.update({field[0] : field[1] })	
	card_dict_members_list.update({'Event' : Event_list})	
	card_dict_members.update({'Event' : Event})
	card_list_members.append({'Event' : Event_list})
	Guided_tour = {}
	Guided_tour_list = [

		['Cardtitle', 'Card Title'],
		['Locationname' , 'Location name'],
		['Text_message' , 'Description'],
		['Web_url' , 'Link to further info'],
		['scan_counter' , "Scan counter" ],
		#['LabelID' , 'Label to print with code'],
		#['Sparetour1' , '(None - spare field)'],
		#['Sparetour2' , '(None - spare field)'],
		]
	for  field in Guided_tour_list:
		Guided_tour.update({field[0] : field[1] })	
	card_dict_members_list.update({'Guided_tour' : Guided_tour_list})	
	card_dict_members.update({'Guided_tour' : Guided_tour})
	card_list_members.append({'Guided_tour' : Guided_tour_list})
	ICE = {}
	ICE_list = [
		['Cardtitle', 'Card Title'],
		['Persontitle' , 'Title (Mr, Ms, Dr, Rev)'],
		['First_Name' , 'First name'],
		['Middle_Name' , 'Middle name or initial'],
		['Last_Name' , 'Family name'],
		['Email2' , 'Home email'],
		#['Reminderdate' , 'Send me a reminder to update on'],
		['Locationname' , 'Location name'],
		['Latlong' , 'Location coordinates'],
		['W_address_Post_Code' , 'Post Code for Sat nav'],
		['Tel1' , 'Emergency contact'],
		['Tel2' , 'Backup contact'],
		['Text_message' , 'Advice'],
		['Web_url' , 'Links'],
		['scan_counter' , "Scan counter" ],
		#['LabelID' , 'Label to print with code'],
		#['SpareICE1' , '(None - spare field)'],
		#['SpareICE2' , '(None - spare field)'],
		]
	for  field in ICE_list:
		ICE.update({field[0] : field[1] })
	card_dict_members_list.update({'ICE' : ICE_list})		
	card_dict_members.update({'ICE' : ICE})
	card_list_members.append({'ICE' : ICE_list})
	Rota = {}
	Rota_list = [
		['Cardtitle', 'Card Title'],
		#['Reminderdate' , 'Remind me to update rota on'],
		['Dutylist' , 'Date and duty details'],
		['Text_message' , 'Current notices'],
		['scan_counter' , "Scan counter" ],
		#['LabelID' , 'Label to print with code'],
		#['Spareduty1' , '(None - spare field)'],
		#['Spareduty2' , '(None - spare field)'],
		]
	for  field in Rota_list:
		Rota.update({field[0] : field[1] })	
	card_dict_members_list.update({'Rota' : Rota_list})	
	card_dict_members.update({'Rota' : Rota})
	card_list_members.append({'Rota' : Rota_list})
	Stock = {}
	Stock_list = [
		['Cardtitle', 'Card Title'],
		['ItemID' , 'Stock number (eg. SKU or UPC)'],
		['Make' , 'Make'],
		['Type' , 'Model, type, colour'],
		['Organisation' , 'Supplier'],
		['Datecreated' , 'Date made'],
		['Status' , 'Status (eg. reserved, sold, discontinued, damaged)'],
		['Web_url' , 'Link to on-line catalogue or stock system'],
		['Datesold' , 'Date sold'],
		['Price1' , 'Cost price'],
		['Price2' , 'Retail price'],
		['Price3' , 'Discounted price'],
		['Text_message' , 'Details'],
		['scan_counter' , "Scan counter" ],
		#['LabelID' , 'Label to print with code'],
		#['Sparestock1' , '(None - spare field)'],
		#['Sparestock2' , '(None - spare field)'],
		]
	for  field in Stock_list:
		Stock.update({field[0] : field[1] })
	card_dict_members_list.update({'Stock' : Stock_list})		
	card_dict_members.update({'Stock' : Stock})
	card_list_members.append({'Stock' : Stock_list})
	Location = {}
	Location_list = [
		['Cardtitle', 'Card Title'],
		['Locationname' , 'You are here'],
		['Latlong' , 'Location coordinates'],
		['W_address_Post_Code' , 'Post Code for Sat nav'],
		['Text_message' , 'Information'],
		['scan_counter' , "Scan counter" ],
		#['LabelID' , 'Label to print with code'],
		#['Sparelocation1' , '(None - spare field)'],
		#['Sparelocation2' , '(None - spare field)'],
		]
	for  field in Location_list:
		Location.update({field[0] : field[1] })	
	card_dict_members_list.update({'Location' : Location_list})
	card_dict_members.update({'Location' : Location})
	card_list_members.append({'Location' : Location_list})
	Go_to_URL = {}
	Go_to_URL_list = [
		['Cardtitle', 'Card Title'],
		['Auto_forward' , 'Target website (use http:// etc.)'],
		['scan_counter' , "Scan counter" ],
		#['LabelID' , 'Label to print with code'],
		#['Sparegoto1' , '(None - spare field)'],
		#['Sparegoto2' , '(None - spare field)'],
		]
	for  field in Go_to_URL_list:
		Go_to_URL.update({field[0] : field[1] })
	card_dict_members_list.update({'Go_to_URL' : Go_to_URL_list})		
	card_dict_members.update({'Go_to_URL' : Go_to_URL})
	card_list_members.append({'Go_to_URL' : Go_to_URL_list})
	Blank = {}
	Blank_list = [
		['Cardtitle', 'Card Title'],
		#['Reminderdate' , 'Remind me to update this card on'],
		['Text_message' , 'Message'],
		['scan_counter' , "Scan counter" ],
		#['LabelID' , 'Label to print with code'],
		#['Spareblank1' , '(None - spare field)'],
		#['Spareblank2' , '(None - spare field)'],
		]
	for  field in Blank_list:
		Blank.update({field[0] : field[1] })	
	card_dict_members_list.update({'Blank' : Blank_list})	
	card_dict_members.update({'Blank' : Blank})
	card_list_members.append({'Blank' : Blank_list})

	Mini_web = {}
	Mini_web_list = [
		['Cardtitle', 'Card Title'],
		['Text_message' , 'Message'],
		['mini_web_01' , 'Page 1'],
		['mini_web_02' , 'Page 2'],
		['mini_web_03' , 'Page 3'],
		['mini_web_04' , 'Page 4'],
		['mini_web_05' , 'Page 5'],
		['mini_web_06' , 'Page 6'],
		['mini_web_07' , 'Page 7'],
		['mini_web_08' , 'Page 8'],
		['mini_web_09' , 'Page 9'],
		['mini_web_10' , 'Page 10'],
		['scan_counter' , "Scan counter" ],

		]
	for  field in Mini_web_list:
		Mini_web.update({field[0] : field[1] })	
	card_dict_members_list.update({'Mini_web' : Mini_web_list})	
	card_dict_members.update({'Mini_web' : Mini_web})
	card_list_members.append({'Mini_web' : Mini_web_list})

	Not_in_use = {}
	Not_in_use_list = [
		['Cardtitle', 'Not in use'],

		]
	for  field in Not_in_use:
		Not_in_use.update({field[0] : field[1] })	
	card_dict_members_list.update({'Not_in_use' : Not_in_use_list})	
	card_dict_members.update({'Not_in_use' : Not_in_use})
	card_list_members.append({'Not_in_use' : Not_in_use_list})

	card_type_dict = {
		'Business' : Business,
		'Membership' : Membership,
		'Service' : Service,
		'Offer' : Offer,
		#'Event' : Event,
		'Guided_tour' : Guided_tour,
		'ICE' : ICE,
		#'Rota' : Rota,
		'Stock' : Stock,
		'Location' : Location,
		'Go_to_URL' : Go_to_URL,
		'Blank' :Blank ,
		'Mini_web' : Mini_web,
		'Not_in_use' : Not_in_use ,
		}

	card_name_dict = {
		'Business' : 'Business',
		'Membership' : 'Membership',
		'Service' : 'Service',
		'Offer' : 'Offer',
		#'Event' : 'Event',
		'Guided_tour' : 'Guided tour',
		'ICE' : 'ICE',
		#'Rota' : 'Rota',
		'Stock' : 'Stock',
		'Location' : 'Location',
		'Go_to_URL' : 'Go to URL',
		'Blank' : 'Blank' ,
		'Mini_web' : 'Mini web',
		'Not_in_use' : 'Not in use'
		}





	all_fields = [
	'W_address_line_1',
	'W_address_line_2',
	'W_address_Post_Town',
	'W_address_County',
	'W_address_Post_Code',
	'W_address_Country',
	'First_Name',
	'Last_Name',
	'Middle_Name',
	'Organisation',
	'Auto_forward',
	'Email_address',
	'Work_Phone',
	'Home_Phone',
	'Mobile_Phone',
	'Google_analytics',
	'Web_url',
	'Text_message',
	'Tel1',
	'Tel2',
	'Tel3',
	'CardID',
	'Cardtitle',
	'Datesold',
	'Datecreated',
	'Datewarrexp',
	'Day',
	'Dutylist',
	'Email2',
	'Endate',
	'ItemID',
	'LabelID',
	'Latlong',
	'Locationname',
	'Make',
	'Offers',
	'Persontitle',
	'Price1',
	'Price2',
	'Price3',
	'Qualifications',
	'Reminderdate',
	'Spareblank1',
	'Spareblank2',
	'Sparebusiness1',
	'Sparebusiness2',
	'Spareduty1',
	'Spareduty2',
	'Spareevent1',
	'Spareevent2',
	'Sparegoto1',
	'Sparegoto2',
	'SpareICE1',
	'SpareICE2',
	'Sparelocation1',
	'Sparelocation2',
	'Sparemembership1',
	'Sparemembership2',
	'Spareoffer1',
	'Spareoffer2',
	'Spareservice1',
	'Spareservice2',
	'Sparestock1',
	'Sparestock2',
	'Sparetour1',
	'Sparetour2',
	'Startdate',
	'Status',
	'Itemlist',
	'Type',
	'URL2',
	'URLsocialnets',
	'Stat_counter',
	'mini_web_01',
	'mini_web_02',
	'mini_web_03',
	'mini_web_04',
	'mini_web_05',
	'mini_web_06',
	'mini_web_07',
	'mini_web_08',
	'mini_web_09',
	'mini_web_10',
	'scan_counter'
	]




	# If a field is not listed it will be a text field
	field_widget = {
	'Text_message' : 'Text_area',
	'mini_web_01' : 'mini_web',
	'mini_web_02' : 'mini_web',
	'mini_web_03' : 'mini_web',
	'mini_web_04' : 'mini_web',
	'mini_web_05' : 'mini_web',
	'mini_web_06' : 'mini_web',
	'mini_web_07' : 'mini_web',
	'mini_web_08' : 'mini_web',
	'mini_web_09' : 'mini_web',
	'mini_web_10' : 'mini_web',
	'Day'      :	'Date_field',
	'Datesold' : 'Date_field',
	'Reminderdate': 'Date_field',
	'Datecreated': 'Date_field',
	'Datewarrexp': 'Date_field',
	'Startdate': 'Date_field',
	'Endate': 'Date_field',
	'Web_url' : 'url_link',
	'URL2' : 'url_link',
	}

	all_dicts = {
		'card_dict_members' : card_dict_members, 
		'card_type_dict' : card_type_dict, 
		'card_list_members' : card_list_members, 
		'all_fields' :  all_fields,
		'card_dict_members_list' : card_dict_members_list,
		'field_widget' : field_widget,
		'card_name_dict' : card_name_dict,
		}
	
	return all_dicts

def lookup_html_template(arg_CardID):
	display_template_dict = {
	'Business' : 'landing_fragment_dict_business.html',
	'Mini_web' : 'landing_fragment_dict_mini_web.html',
	'Guided_tour' : 'landing_fragment_dict_guided_tour.html'
	}

	edit_template_dict = {
	'Business' : 'generic_edit_form_fragment.html'
	}

################# dont edit these by mistake!
	if arg_CardID in display_template_dict:
		display_template = display_template_dict[arg_CardID]
	else:
		display_template = 'landing_fragment_dict.html'
	if arg_CardID in edit_template_dict:
		edit_template = edit_template_dict[arg_CardID]
	else:
		edit_template = 'generic_edit_form_fragment.html'

	html_template_dict = {
	'display' : display_template,
	'edit' : edit_template

	}

	return html_template_dict

def get_mini_web_list(self,arg_userID):
	#user = users.get_current_user()
	domain = set_domain(self.request.url)
	card_fields_values = {}
	mini_web_dict = {}
	my_query = db.GqlQuery('SELECT * FROM place_address WHERE user_id = :1 ORDER BY Cardtitle', arg_userID)
	# Need to add a check to make sure at least one page exists here
	count_my_records = 0
	if my_query:
		  for my_place in my_query:
			#count_my_records += 1
			# Get the values from each card so we can go to the edit page
			my_landing_page_values = []

			my_card = "%s/?key_string=%s"  %( domain,my_place.Key_Name_String)
			# Now add the vales to the list
			#my_landing_page_list.append(my_landing_page_values)
			field_dict = card_definitions_v2()
			all_field_dict = field_dict['all_fields']
			mini_web_dict.update({"None" : ""})
			for field_name in all_field_dict:
				field_name_value = getattr(my_place, field_name,"")
				card_fields_values.update({field_name : field_name_value} )
			Cardtitle = card_fields_values['Cardtitle']
			Cardtitle = Cardtitle.decode( 'unicode-escape' ).encode( 'ascii' )
			Key_Name_String =  my_place.Key_Name_String
			Key_Name_String = Key_Name_String.decode( 'unicode-escape' ).encode( 'ascii' )
			#mini_web_dict.update({Cardtitle: my_place.Key_Name_String})
			mini_web_dict.update({Key_Name_String : Cardtitle})
			
	
	return mini_web_dict	

def increment_page_counter(self,arg_key):
	# This is set up user scanning while elimiating self scans
	# Will be included on the card list page.
	#Define a few internal functions so we can update the database in transaction mode.
	def put_to_counter(arg_query, arg_counter_name, arg_counter_value):
		#arg_query.arg_counter_name = "%s" % arg_counter_value
		setattr(arg_query, arg_counter_name, ("%s" % arg_counter_value))
		arg_query.put()
	def create_q_action_system_record():
		my_q_action = q_action_manager(key_name='q_action_manager')
		my_q_action.put()	
		
	my_query = self.request.query
	my_query_urlparse = cgi.parse_qs(my_query)
	if "no_scan" in my_query_urlparse:
		no_scan_value = my_query_urlparse["no_scan"]
		no_scan = no_scan_value[0]
		no_scan_string = "&no_scan=True"

	else:
		no_scan = "False"
		no_scan_string = ""

	if no_scan == "False":
		my_query = place_address.get(db.Key.from_path('place_address',arg_key))	
		
		if my_query:
		# Go set all the attributes with a little bit of error trapping	
			my_user_key = my_query.user_id
			my_account = account_manager.get(db.Key.from_path('account_manager',my_user_key))	
			
			# Page Counter
			try:
				counter_str = my_query.scan_counter
			except:
				counter_str = u"0"

			if counter_str != None or counter_str == 'None' :
				if unicode.isnumeric(counter_str):
					scan_counter = int(counter_str) + 1
				else:
					scan_counter = 1
			else:
				scan_counter = 1

			db.run_in_transaction(put_to_counter,my_query,'scan_counter', scan_counter)


			# Account Counter
			try:
				total_scan_counter_str = my_account.total_scan_counter
			except:
				total_scan_counter_str = u"0"

			if total_scan_counter_str != None or total_scan_counter_str == 'None' :
				if unicode.isnumeric(total_scan_counter_str):
						total_scan_counter = int(total_scan_counter_str) + 1
				else:
						total_scan_counter = 1
			else:
				total_scan_counter = 1
			
			db.run_in_transaction(put_to_counter, my_account,'total_scan_counter', total_scan_counter)

			# System Counter
			#my_place = place_address(key_name='%s' % field_dict['Key_Name'])
			#We may have to make the system record on startup
			
			my_q_action = q_action_manager.get(db.Key.from_path('q_action_manager','q_action_manager'))
			if not  my_q_action:
				create_q_action_system_record()

			try:
				my_q_action = q_action_manager.get(db.Key.from_path('q_action_manager','q_action_manager'))
				system_scan_counter_str = my_q_action.system_scan_counter
				#system_scan_counter_str = u"0"
			except:						
				system_scan_counter_str = u"0"
			if system_scan_counter_str != None or system_scan_counter_str == 'None' :
				if unicode.isnumeric(system_scan_counter_str):
						system_scan_counter = int(system_scan_counter_str) + 1
				else:
						system_scan_counter = 1
			else:
				system_scan_counter = 1

			db.run_in_transaction(put_to_counter, my_q_action,'system_scan_counter', system_scan_counter)

			

	no_scan_dict = {
		'no_scan_string' : no_scan_string
	}

	return no_scan_dict	


def page_not_exist(self):

	pageTitle= 'Page Not Found'
	template_values = {
		'pageTitle': pageTitle, 

	}
	path = os.path.join(os.path.dirname(__file__), 'html/page_not_found.html')
	self.response.out.write(template.render(path, template_values))
 	return
