#!/usr/bin/python
import gdata.spreadsheet.service
import requests
from xml.dom.minidom import parseString
import time

def get_wotd():
	API_KEY = 'API_KEY'
	
	r = requests.get('http://api-pub.dictionary.com/v001?vid=%s&type=wotd' % API_KEY)
	xml_doc = parseString(r.text)
	entry = (xml_doc.getElementsByTagName('entry'))[0]
	word = (entry.getElementsByTagName('word')[0]).firstChild.nodeValue
	definition = (entry.getElementsByTagName('shortdefinition')[0]).firstChild.nodeValue
	day = time.strftime("%m/%d/%y", time.localtime())
	return (word, definition, day)

word, definition, date = get_wotd()
email = 'EMAIL'
password = 'PASSWORD'
# Find this value in the url with 'key=XXX' and copy XXX below
spreadsheet_key = 'SPREADSHEET_KEY'
# All spreadsheets have worksheets. I think worksheet #1 by default always
# has a value of 'od6'
worksheet_id = 'od6'

spr_client = gdata.spreadsheet.service.SpreadsheetsService()
spr_client.email = email
spr_client.password = password
spr_client.source = 'Automatic Word of The Day Spreadsheet Writing Program'
spr_client.ProgrammaticLogin()

# Prepare the dictionary to write
dict = {}
dict['word'] = word
dict['definition'] = definition
dict['date'] = date
print dict

entry = spr_client.InsertRow(dict, spreadsheet_key, worksheet_id)
if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
	print "Insert row succeeded."
else:
	print "Insert row failed."
