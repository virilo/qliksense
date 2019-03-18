# -*- coding: utf-8 -*-
"""
Created on December 2016

@author: virilo
"""



from websocket import create_connection
import urllib
import json

APP_FILE="POC.qvf"
APP_ID=APP_FILE
QLIK_APPS_PATH='C:\\Users\\virilo.tejedor\\Documents\\Qlik\\Sense\\Apps\\'
QLIK_WS_URL = "ws://localhost:4848"

SAVE_QLIK_APP_AFTER_RELOAD=True

endpoint="{}/app/{}{}".format(QLIK_WS_URL, urllib.parse.quote(QLIK_APPS_PATH), urllib.parse.quote(APP_ID))


print("\n\n\n\n\n\n\nendpoint: " + endpoint)


ERROR_CODE_APP_ALREADY_OPEN=1002
ERROR_CODE_APP_NOT_FOUND=1003


ws = create_connection(endpoint)

#############################
#  OPEN DOC
#############################


params='''{
	"handle": -1,
	"method": "OpenDoc",
	"params": [
		"''' + APP_ID + '''"
	],
	"outKey": -1
}'''

print("params:")
print(params)

ws.send(params)
print ("Sent")
print ("Receiving...")
result =  ws.recv()
print ("Received '%s'" % result)
#ws.close()


'''
OK:
===
Received '{"jsonrpc":"2.0","id":0,"result":{"qReturn":{"qType":"Doc","qHandle":1}},"change":[1]}'

ERROR
=====
Received '{"jsonrpc":"2.0","id":0,"error":{"code":1002,"parameter":"POC-BOE-CATASTRO.qvf","message":"App already open"}}'

'''


result_dict=json.loads(result)

if 'error' in result_dict and result_dict['error']['code']==ERROR_CODE_APP_NOT_FOUND:
    raise Exception("App not found")
elif 'error' in result_dict and result_dict['error']['code']==ERROR_CODE_APP_ALREADY_OPEN:
    print("DEBUG: App already open")

    params='''{
        	"handle": -1,
        	"method": "GetActiveDoc",
        	"params": {},
        	"outKey": -1
    }'''
    print("params:")
    print(params)
    
    ws.send(params)
    print ("Sent")
    print ("Receiving...")
    result =  ws.recv()
    result_dict=json.loads(result)
    print ("Received '%s'" % result)
else:
    pass


q_handle=result_dict['result']['qReturn']['qHandle']





"""
params='''{"handle": "-1",
    "method": "DoReload",
	"params": {
		"qMode": "0",
		"qPartial": "false",
		"qDebug": "false"
	}}'''

"""

#############################
#  DO RELOAD
#############################



params='''{
	"handle": ''' + str(q_handle) + ''',
	"method": "DoReload",
	"params": {
		"qMode": 0,
		"qPartial": false,
		"qDebug": false
	},
	"jsonrpc": "2.0",
	"id": 3
}'''



"""
params='''{"handle": "1",
    "method": "DoReload",
	"params": {
		"qMode": "0",
		"qPartial": "false",
		"qDebug": "false"
	}}'''
"""



#params = "{\"method\":\"GetDocList\",\"handle\":-1,\"params\":[],\"id\":7,\"jsonrpc\":\"2.0\"}";  

#params = "{\"method\":\"DoReload\",\"handle\":1,\"params\":[],\"id\":7,\"jsonrpc\":\"2.0\"}";  

#params='''{"handle": "1","method": "DoReload","params": {"qMode": "0","qPartial": "false","qDebug": "false"},"jsonrpc": "2.0","id": 3}'''      


print("params:")
print(params)

ws.send(params)
print ("Sent")
print ("Receiving...")
result =  ws.recv()
result_dict=json.loads(result)
print ("Received '%s'" % result)
#ws.close()

if not result_dict['result']['qReturn']:
    print("ERROR en la recarga.  Para ver el error realizar recarga desde la aplicación QlikSense")
elif SAVE_QLIK_APP_AFTER_RELOAD:
    #############################
    #  DO SAVE
    #############################

    params='''{
    	"handle": ''' + str(q_handle) + ''',
    	"method": "DoSave",
    	"params": {
    		"qFileName": ""
    	},
    	"outKey": -1,
    	"jsonrpc": "2.0",
    	"id": 3
    }'''
    
    print("params:")
    print(params)
    
    ws.send(params)
    print ("Sent")
    print ("Receiving...")
    result =  ws.recv()
    print ("Received '%s'" % result)


ws.close()

