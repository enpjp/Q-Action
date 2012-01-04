# Create a first landing page to use
class admin_create_landing_page(webapp.RequestHandler):
    def get(self):
## User control -------------------------------------------------------
        user = users.get_current_user()
	login_url = users.create_login_url(self.request.uri)
	logout_url = users.create_logout_url(self.request.uri)
        if user:
 	    #self.response.out.write(""" <div class="login"><!-- login text here here --> You are logged-in as: %s <a href="%s">Logout</a><br></div>  """ % (user.nickname(), logout_url) )
	    logon_message = "You are logged-in as: "
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
	# Test if user is allowed a new contact set the default to one
	my_query = db.GqlQuery('SELECT * FROM place_address WHERE owner = :1', user)
	number_of_records = my_query.count()
	# Always true for admin
	if 0 < 1:
		# Create new contact
		Key_Name = hashlib.sha224(os.urandom(10)).hexdigest()
		Key_Name = Key_Name[0:12]
		#Test if key name exists, if it does go home!
		my_test_query = db.GqlQuery('SELECT * FROM place_address WHERE Key_Name = :1', Key_Name)
		if my_test_query.count() > 0:
			self.redirect( '/')


		template_values_fields = {
			'Key_Name' : Key_Name,
			#'user_id' : user_id,
			#'edit_my_record' : edit_my_record,
			#'login_url' : login_url,
			#'logout_url' : logout_url,
			#'logon_message' : logon_message,
			#'user_nickname_or_url' : user_nickname_or_url,
			#'pageTitle': pageTitle, 
			#'my_url' : my_url,
			#'my_path' : my_path,
			'First_Name' : "A",
	            	'Middle_Name': "N",
			'Last_Name': "Other",
			'Organisation' : "",
	 		'W_address_line_1' : "",
			'W_address_line_2' : "",
			'W_address_Post_Town' :  "",
			'W_address_County' :  "",
			'W_address_Post_Code' : "",
			'W_address_Country'  : "",
			'Email_address' : "",
			'Work_Phone' : "",
			'Home_Phone' : "",
			'Mobile_Phone' : "",
			'Web_url' : "",
			'Text_message' : "",
			'Auto_forward' : "",
			'my_qr_code' : "",
			'my_qr_data' : "",
			'zero' : 0,
			'Google_analytics' : "",
			'Stat_counter' : "",

			'Tel1' : '',
			'Tel2' : '',
			'Tel3' : '',
			'CardID' : 'Business',
			'Cardtitle' : '',
			'Datesold' : '',
			'Datecreated' : '',
			'Datewarrexp' : '',
			'Day' : '',
			'Dutylist' : '',
			'Email2' : '',
			'Endate' : '',
			'ItemID' : '',
			'LabelID' : '',
			'Latlong' : '',
			'Locationname' : '',
			'Make' : '',
			'Offers' : '',
			'Persontitle' : '',
			'Price1' : '',
			'Price2' : '',
			'Price3' : '',
			'Qualifications' : '',
			'Reminderdate' : '',
			'Spareblank1' : '',
			'Spareblank2' : '',
			'Sparebusiness1' : '',
			'Sparebusiness2' : '',
			'Spareduty1' : '',
			'Spareduty2' : '',
			'Spareevent1' : '',
			'Spareevent2' : '',
			'Sparegoto1' : '',
			'Sparegoto2' : '',
			'SpareICE1' : '',
			'SpareICE2' : '',
			'Sparelocation1' : '',
			'Sparelocation2' : '',
			'Sparemembership1' : '',
			'Sparemembership2' : '',
			'Spareoffer1' : '',
			'Spareoffer2' : '',
			'Spareservice1' : '',
			'Spareservice2' : '',
			'Sparestock1' : '',
			'Sparestock2' : '',
			'Sparetour1' : '',
			'Sparetour2' : '',
			'Startdate' : '',
			'Status' : '',
			'Itemlist' : '',
			'Type' : '',
			'URL2' : '',
			'URLsocialnets' : '',

        	}


		db.run_in_transaction(postContact_V2, self, template_values_fields)
		template_values = get_a_record_from_key(self, Key_Name)
		field_list = template_values
		template_values.update({'field_list' : field_list})

		#Forward to the edit form
		path = os.path.join(os.path.dirname(__file__), 'html/edit_landing_page.html')
        	self.response.out.write(template.render(path, template_values))
	else:
        	self.redirect( '/')
 

