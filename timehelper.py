#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

# serialize / deserialize between datetime and dict (for saving as json)
		
def serializeDateTimeToDict (dt):
	return {
		"_type_" : "_datetime_",
		"year" : dt.year,
		"month" : dt.month,
		"day" : dt.day,
		"hour" : dt.hour,
		"minute" : dt.minute,
		"second" : dt.second,
		"microsecond" : dt.microsecond
	}
	
def deserializeDictToDateTime (d):
	if d.get ("_type_") != "_datetime_":
		return None
		
	return datetime (
		year=d.get ("year"), month=d.get ("month"), day=d.get ("day"),
		hour=d.get ("hour"), minute=d.get ("minute"), second=d.get ("second"),
		microsecond=d.get ("microsecond")
	)