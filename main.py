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
#Not needed
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
# Note this must be the first line
from google.appengine.dist import use_library
use_library('django', '1.2')


from google.appengine.ext import webapp
#from google.appengine.ext.webapp import util

from views import *





class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')


def main():
    application = webapp.WSGIApplication([('/', HomePage),
					('/create.html', create_landing_page),
					#('/admin/create.html', admin_create_landing_page),
					('/work_to_do.html', work_to_do_page),
					('/landing_page_list.html', landing_page_list),	
					('/qr_code_private_page.html', qr_code_private_page_v1),
					('/edit_landing_page.html', edit_landing_page_form),
					('/update_contact.html', update_contact),

					('/info/.*.html', InfoPage),
					('/download.csv', download_csv_files),	
					('/choose.html', ChooseFileToUpload),
					('/upload.html', PostToDatabase_V1),
					('/subscribe/buy_subscription.html', BuySubscriptionPage),				
					('/.*', qr_code_landing_page_v1),	

							],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
