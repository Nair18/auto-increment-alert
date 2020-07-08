import mysql.connector
import sys
import os
from slackclient import SlackClient
import time
import json 
import requests

def call(ll):
    message = "hello, "
    if len(ll)==0:
		message+="everything is fine."
       
    else:
    	message+=" tables "
    	for i in ll:
    		message+=str(i)
    	message+=" are about to run short of auto-increment ids."
    

    web_hook_url = 'https://hooks.slack.com/services/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'
    slack_msg = {'text':message}
    requests.post(web_hook_url,data=json.dumps(slack_msg))

mysql = mysql.connector.connect(host = "localhost", user = "karthik", passwd = "Hello@18", database = "postman")
cursor = mysql.cursor()

#cursor.execute("USE postman")
query = ("""
  SELECT
  TABLE_SCHEMA,
  TABLE_NAME,
  COLUMN_NAME,
  DATA_TYPE,
  COLUMN_TYPE,
  IF(
    LOCATE('unsigned', COLUMN_TYPE) > 0,
    1,
    0
  ) AS IS_UNSIGNED,
  (
    CASE DATA_TYPE
      WHEN 'tinyint' THEN 255
      WHEN 'smallint' THEN 65535
      WHEN 'mediumint' THEN 16777215
      WHEN 'int' THEN 4294967295
      WHEN 'bigint' THEN 18446744073709551615
    END >> IF(LOCATE('unsigned', COLUMN_TYPE) > 0, 0, 1)
  ) AS MAX_VALUE,
  AUTO_INCREMENT,
  AUTO_INCREMENT / (
    CASE DATA_TYPE
      WHEN 'tinyint' THEN 255
      WHEN 'smallint' THEN 65535
      WHEN 'mediumint' THEN 16777215
      WHEN 'int' THEN 4294967295
      WHEN 'bigint' THEN 18446744073709551615
    END >> IF(LOCATE('unsigned', COLUMN_TYPE) > 0, 0, 1)
  ) AS AUTO_INCREMENT_RATIO
FROM
  INFORMATION_SCHEMA.COLUMNS
  INNER JOIN INFORMATION_SCHEMA.TABLES USING (TABLE_SCHEMA, TABLE_NAME)
WHERE
  TABLE_SCHEMA NOT IN ('mysql', 'INFORMATION_SCHEMA', 'performance_schema')
  AND EXTRA='auto_increment';
""")

while True:
    cursor.execute(query)
    ll = []

    for x in cursor:
	    if x[-1]*100>95:
		    ll.append(x[1])

    call(ll)
    time.sleep(5000)


	
#call function sends message to slack thread
