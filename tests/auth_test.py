#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest, os, os.path, shutil
import auth, kvstore

class UserAuthentication_Test (unittest.TestCase):
	def setUp (self):
		if os.path.exists ("sandbox"):
			shutil.rmtree ("sandbox")
		os.makedirs ("sandbox")
		conf = {
			"kvstore_type" : kvstore.KVStore.LOCAL_STORE,
			"rootdir" : "sandbox/",
			"kvstore_location" : "",
			"pwdtype" : "raw",
			"expire_duration" : 1800,
		}
		self.auth = auth.UserAuthentication (conf)

	def test (self):
		email = "testaccount@mailserver.com"
		pwd = "password"
		pwd2 = "password1234!@#$"
		self.assertTrue (self.auth.sign_up (email, pwd))
		self.assertEqual (self.auth.sign_in (email, pwd), None)
		self.assertFalse (self.auth.change_password (email, pwd, pwd2))
		self.assertTrue (self.auth.auth_confirm_email (email, self.auth.issue_confirm_code (email)))
		sessionid = self.auth.sign_in (email, pwd)
		self.assertNotEqual (sessionid, None)
		self.assertNotEqual (self.auth.verify_session (email, sessionid), None)
		self.assertTrue (self.auth.change_password (email, pwd, pwd2))
		self.assertNotEqual (self.auth.verify_session (email, sessionid), None)
		self.assertEqual (self.auth.sign_in (email, pwd), None)
		sessionid2 = self.auth.sign_in (email, pwd2)
		self.assertNotEqual (sessionid2, None)
		self.assertNotEqual (self.auth.verify_session (email, sessionid2), None)
		self.assertNotEqual (self.auth.verify_session (email, sessionid), None)
		self.assertTrue (self.auth.sign_out (email, sessionid2))
		self.assertTrue (self.auth.sign_out (email, sessionid))

if __name__ == "__main__":
	unittest.main ()
