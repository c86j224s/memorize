#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

#
# TODO make this ugly code more beautiful
#

class UtcDateTime (object):
	def __init__ (self, datetime_utc=datetime.utcnow ()):
		self.dt_utc = datetime_utc

	def __del__ (self):
		pass

	def __add__ (self, seconds):
		self.dt_utc += timedelta (seconds=seconds)
		return self

	def __sub__ (self, seconds):
		self.dt_utc -= timedelta (seconds=seconds)
		return self

	def get_dict (self):
		d = {}
		d["_type_"] = __name__
		d["year"] = self.dt_utc.year
		d["month"] = self.dt_utc.month
		d["day"] = self.dt_utc.day
		d["hour"] = self.dt_utc.hour
		d["minute"] = self.dt_utc.minute
		d["second"] = self.dt_utc.second
		return d

	def parse (self, dt):
		if dt.get ("_type_") != __name__:
			return None

		self.dt_utc = datetime (year=dt.get ("year"), month=dt.get ("month"), day=dt.get ("day"),
			hour=dt.get ("hour"), minute=dt.get ("minute"), second=dt.get ("second"))

		return self

	def get_datetime (self):
		return self.dt_utc
