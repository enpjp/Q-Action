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

from google.appengine.ext import db
#Define some data models


class place_address(db.Model):
# This is the master dictionary containing all qr-codes and contact details
	owner = db.UserProperty(auto_current_user_add=True)
	user_id = db.StringProperty(multiline=False)
    	Date_created = db.DateTimeProperty(auto_now_add=True)	
	Key_Name_String = db.StringProperty(multiline=False)
#  These are the existing fields in the card
	First_Name = db.StringProperty(multiline=False)
	Middle_Name = db.StringProperty(multiline=False)
	Last_Name = db.StringProperty(multiline=False)
	Organisation = db.StringProperty(multiline=False)
	W_address_line_1 = db.StringProperty(multiline=False)
	W_address_line_2 = db.StringProperty(multiline=False)
	W_address_Post_Town = db.StringProperty(multiline=False)
	W_address_County = db.StringProperty(multiline=False)
	W_address_Post_Code = db.StringProperty(multiline=False)
	W_address_Country = db.StringProperty(multiline=False)
	Email_address = db.StringProperty(multiline=False)
	Work_Phone = db.StringProperty(multiline=False)
	Home_Phone = db.StringProperty(multiline=False)
	Mobile_Phone = db.StringProperty(multiline=False)
    	Web_url = db.StringProperty(multiline=False)
    	Text_message = db.StringProperty(multiline=True)
	Auto_forward = db.StringProperty(multiline=False)
	Google_analytics = db.StringProperty(multiline=False)
	Stat_counter = db.StringProperty(multiline=False)
#  These are the new fields in the card
	Tel1 = db.StringProperty(multiline=False)
	Tel2 = db.StringProperty(multiline=False)
	Tel3 = db.StringProperty(multiline=False)
	CardID = db.StringProperty(multiline=False)
	Cardtitle = db.StringProperty(multiline=False)
	Datesold = db.StringProperty(multiline=False)
	Datecreated = db.StringProperty(multiline=False)
	Datewarrexp = db.StringProperty(multiline=False)
	Day = db.StringProperty(multiline=False)
	Dutylist = db.StringProperty(multiline=False)
	Email2 = db.StringProperty(multiline=False)
	Endate = db.StringProperty(multiline=False)
	ItemID = db.StringProperty(multiline=False)
	LabelID = db.StringProperty(multiline=False)
	Latlong = db.StringProperty(multiline=False)
	Locationname = db.StringProperty(multiline=False)
	Make = db.StringProperty(multiline=False)
	Offers = db.StringProperty(multiline=False)
	Persontitle = db.StringProperty(multiline=False)
	Price1 = db.StringProperty(multiline=False)
	Price2 = db.StringProperty(multiline=False)
	Price3 = db.StringProperty(multiline=False)
	Qualifications = db.StringProperty(multiline=False)
	Reminderdate = db.StringProperty(multiline=False)
	Spareblank1 = db.StringProperty(multiline=False)
	Spareblank2 = db.StringProperty(multiline=False)
	Sparebusiness1 = db.StringProperty(multiline=False)
	Sparebusiness2 = db.StringProperty(multiline=False)
	Spareduty1 = db.StringProperty(multiline=False)
	Spareduty2 = db.StringProperty(multiline=False)
	Spareevent1 = db.StringProperty(multiline=False)
	Spareevent2 = db.StringProperty(multiline=False)
	Sparegoto1 = db.StringProperty(multiline=False)
	Sparegoto2 = db.StringProperty(multiline=False)
	SpareICE1 = db.StringProperty(multiline=False)
	SpareICE2 = db.StringProperty(multiline=False)
	Sparelocation1 = db.StringProperty(multiline=False)
	Sparelocation2 = db.StringProperty(multiline=False)
	Sparemembership1 = db.StringProperty(multiline=False)
	Sparemembership2 = db.StringProperty(multiline=False)
	Spareoffer1 = db.StringProperty(multiline=False)
	Spareoffer2 = db.StringProperty(multiline=False)
	Spareservice1 = db.StringProperty(multiline=False)
	Spareservice2 = db.StringProperty(multiline=False)
	Sparestock1 = db.StringProperty(multiline=False)
	Sparestock2 = db.StringProperty(multiline=False)
	Sparetour1 = db.StringProperty(multiline=False)
	Sparetour2 = db.StringProperty(multiline=False)
	Startdate = db.StringProperty(multiline=False)
	Status = db.StringProperty(multiline=False)
	Itemlist = db.StringProperty(multiline=False)
	Type = db.StringProperty(multiline=False)
	URL2 = db.StringProperty(multiline=False)
	URLsocialnets = db.StringProperty(multiline=False)
#       These are the mini web fields
	mini_web_01 = db.StringProperty(multiline=False)	
	mini_web_02 = db.StringProperty(multiline=False)	
	mini_web_03 = db.StringProperty(multiline=False)
	mini_web_04 = db.StringProperty(multiline=False)
	mini_web_05 = db.StringProperty(multiline=False)
	mini_web_06 = db.StringProperty(multiline=False)
	mini_web_07 = db.StringProperty(multiline=False)
	mini_web_08 = db.StringProperty(multiline=False)
	mini_web_09 = db.StringProperty(multiline=False)
	mini_web_10 = db.StringProperty(multiline=False)
	scan_counter = db.StringProperty(multiline=False)


class account_manager(db.Model):
	owner = db.UserProperty(auto_current_user_add=True)
	nickname = db.StringProperty(multiline=False)
	email = db.StringProperty(multiline=False)
	user_id = db.StringProperty(multiline=False)
    	Date_created = db.DateTimeProperty(auto_now_add=True)
	account_valid  = db.BooleanProperty(False)
	suspend_account = db.BooleanProperty(False)
	page_limit = db.StringProperty(multiline=False)
	renewal_date = db.DateTimeProperty()
	free_trial_end = db.DateTimeProperty()
	total_scan_counter = db.StringProperty(multiline=False)
	renewal_confirm_date = db.DateTimeProperty()

class q_action_manager(db.Model):
	system_scan_counter = db.StringProperty(multiline=False)


