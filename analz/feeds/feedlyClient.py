# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 09:23:51 2018

@author: johnc
"""

import requests
import json

feedly_user_id = '4d7004f6-ed84-4452-8605-fad277041e08'
feedly_access_token = 'AwjNosU1s25BcJD3VMn-WubgfqNcgDNI8G9G_-qRfod6F1uFjDjgFWY2xCyTf9asCrkaK1LMH6CRVPSjR-5AQ3lS0gDejosUlcODgkng2knSaDaq00Vl8PmnlI_CaNKpXrO_xz0flncUseg2-xWU_wMzjGfAFhSOqINODeBSFsk6-HFrnyPIQSBHj7AZeFpH87KvjCLwLpkoCr1sHwDyeyyrRkCvgduL6bK3V-xKzrGND3yIz7lsSw:feedlydev'
feedly_refresh_token = 'AwjNosU1s2ZBcJCFVZuqBqumDOtPgWcTrT4A6PSeI5NwE0PR32vjEWc2wC3Gf8KsTrlBMVHeYfPBCa_vV5sWDSgGi0SMyoUa3pebml_0nxaGKTPol09v6uGoyJnNYs2jWrKz02lIxnMXsuo0_EiS6wN8jC3TGRCSus5YBPZSF8lqtzEv3C-cXDgLzLALa0dXsaGsnWu2dcprXfsyR1viYzruRlavw8mA7LCnD-xczqz5V2efhOQocsrIoHzqOMrwQw'

#$ curl -H 'Authorization: OAuth [your access token]' https://cloud.feedly.com/v3/profile

#http://localhost/?code=A-aG__zxd_MKwftLBheyq9tMOxSOTmQ4Cwcn9sifL8Uu8LIIVzpxbkwwxOK3-CaI2fdO-ny-DsKY29iveGAjO-GnMfi_zHBUFmvuideuad4hc6ER7r46ieiiyKTeHXSWo9MilWBREumAOiLv0tXC4GHkATFnPfqyN4VzUsQzIugI3GvB2P2mqU8JZD6w3NwzA2bnZ61jVMl4&state=#***

opts = {
        'service_host': 'sandbox7.feedly.com',
        'client_id': 'sandbox',
        'token': feedly_access_token,
         # (expires on April 1st 2018)
        'client_secret': 'e4RK9ybUMPAa5PgV',
        'API_documentation': 'http://developer.feedly.com/',
        'support_newsgroup': 'https://groups.google.com/forum/#!forum/feedly-cloud',
        'access':{'access_token': 'A_g8E-IkBoiHEbo5uLhkuUsAgXcQBQAxdDhGbryk38UBkVSGZchw2IU-EtdVf21c5giFpxOTGK6_nGIIslMaZ20Wjsbr6-QMjBPYlwMyItSMI4ygvZMN43iULfJBMVfs9ONeA_6_ZDz8AClgnbH21Gd953EGNR5ECSDsyWRQoxkhcmGJhyMEQ9fc-uMXwtK8DoRYYglQNa6_50Om2rP6jsNv-xFeIUIF_Hb-K79Fr0XsY-HC-AKuNQ-XwT-hA0Aio1BZLQ:sandbox',
 'expires_in': 604800,
 'id': 'a0d0fc2b-6c6d-451f-b766-f62ce30e6c5d',
 'plan': 'standard',
 'provider': 'GooglePlus',
 'refresh_token': 'A9Mh4Eomj5p5hFGATlwx-I-UYqCDZwGgFQcaqYgCp7pJxlFF5dDkvVv9MotSH8qgpnt7QhjZjawYg_8VLaenfF4UrP_RyqRwnrzl-OdXtRCT6-P29-oIp8W1X8qydkBcMD3bTICYA4eX-5L6z3Lzp2xJ2MhtTIBwtWpK1wKgLFSlbjauiVEit_FZEWBfEHWuPz1Fe9QV-7GCNrkjwJVkomfeXu7vaJ5Ua98pX3CJTg5tr8swHNgD4eb5ERlaNhjrCgk7oqg:sandbox',
 'token_type': 'Bearer'}
        
        }


FEEDLY_REDIRECT_URI = "http://localhost"
FEEDLY_CLIENT_ID=opts['client_id']
FEEDLY_CLIENT_SECRET=opts['client_secret']

#http://localhost
#https://localhost
#rdir_url = "http://localhost:8080"
#urn:ietf:wg:oauth:2.0:oob

at2 = "AxKl_kE3bC4mT-vVT8c9sUmP75Ynz-qUy8wwzXJOL2nTffV0-Em6ppZeHwvFpPIAVtYjyEfNfE45CjjqWUlBiTA6L1L_I26l4MScdDe-TevWbUwQ3rZ8OMOiq8xaf6-a89SDUJ4derO5U5NWXl301ZYgSrCeosjrvvi4tvHH-bIEcWCMv1oyPmHO5a4nFS5nIKYiWvVldrFpv_l9vv5FjKyjY_2P6NSrK2zU6GfIAYb6fzz817-iUabPoSaI:feedlydev"

access_token = {'access_token': at2,
 'expires_in': 604800,
 'id': 'a0d0fc2b-6c6d-451f-b766-f62ce30e6c5d',
 'plan': 'standard',
 'provider': 'GooglePlus',
 'refresh_token': 'A9Mh4Eomj5p5hFGATlwx-I-UYqCDZwGgFQcaqYgCp7pJxlFF5dDkvVv9MotSH8qgpnt7QhjZjawYg_8VLaenfF4UrP_RyqRwnrzl-OdXtRCT6-P29-oIp8W1X8qydkBcMD3bTICYA4eX-5L6z3Lzp2xJ2MhtTIBwtWpK1wKgLFSlbjauiVEit_FZEWBfEHWuPz1Fe9QV-7GCNrkjwJVkomfeXu7vaJ5Ua98pX3CJTg5tr8swHNgD4eb5ERlaNhjrCgk7oqg:sandbox',
 'token_type': 'Bearer'}

jat = json.dumps(access_token)


def get_feedly_client(token=None):
    print(token)
    if token:
        return FeedlyClient(token=token, sandbox=True)
    else:
        return FeedlyClient(client_id=FEEDLY_CLIENT_ID, client_secret=FEEDLY_CLIENT_SECRET,
                            sandbox=True)

                            
class FeedlyClient(object):
    
    def __init__(self, **options):
        self.client_id = options.get('client_id')
        self.client_secret = options.get('client_secret')
        self.sandbox = options.get('sandbox', True)
        if self.sandbox:
            default_service_host = 'sandbox.feedly.com'
        else:
            default_service_host = 'cloud.feedly.com'
        self.service_host = options.get('service_host', default_service_host)
        self.additional_headers = options.get('additional_headers', {})
        self.token=None
        self.secret = options.get('secret')

    def get_code_url(self, callback_url):
        scope = 'https://cloud.feedly.com/subscriptions'
        response_type = 'code'
        
        request_url = '%s?client_id=%s&redirect_uri=%s&scope=%s&response_type=%s' % (
            self._get_endpoint('v3/auth/auth'),
            self.client_id,
            callback_url,
            scope,
            response_type
            )        
        return request_url
    
    def get_access_token(self,redirect_uri,code):
        params = dict(
                      client_id=self.client_id,
                      client_secret=self.client_secret,
                      grant_type='authorization_code',
                      redirect_uri=redirect_uri,
                      code=code
                      )
        
        quest_url=self._get_endpoint('v3/auth/token')
        res = requests.post(url=quest_url, params=params)
        return res.json()
    
    def refresh_access_token(self,refresh_token):
        '''obtain a new access token by sending a refresh token to the feedly Authorization server'''
        params = dict(
                      refresh_token=refresh_token,
                      client_id=self.client_id,
                      client_secret=self.client_secret,
                      grant_type='refresh_token',
                      )
        quest_url=self._get_endpoint('v3/auth/token')
        res = requests.post(url=quest_url, params=params)
        return res.json()
    
    
    def get_user_subscriptions(self,access_token):
        '''return list of user subscriptions'''
        headers = {'Authorization': 'OAuth '+access_token}
        print('headers: ', headers)
        quest_url=self._get_endpoint('v3/subscriptions')
        print('quest_url: ', quest_url)
        res = requests.get(url=quest_url, headers=headers)
        print(res.text)
        return res.json()
    
    def get_feed_content(self,access_token,streamId,unreadOnly,newerThan):
        '''return contents of a feed'''
        headers = {'Authorization': 'OAuth '+access_token}
        quest_url=self._get_endpoint('v3/streams/contents')
        params = dict(
                      streamId=streamId,
                      unreadOnly=unreadOnly,
                      newerThan=newerThan
                      )
        res = requests.get(url=quest_url, params=params,headers=headers)
        return res.json()
    
    def mark_article_read(self, access_token, entryIds):
        '''Mark one or multiple articles as read'''
        headers = {'content-type': 'application/json',
                   'Authorization': 'OAuth ' + access_token
        }
        quest_url = self._get_endpoint('v3/markers')
        params = dict(
                      action="markAsRead",
                      type="entries",
                      entryIds=entryIds,
                      )
        res = requests.post(url=quest_url, data=json.dumps(params), headers=headers)
        return res
    
    def save_for_later(self, access_token, user_id, entryIds):
        '''saved for later.entryIds is a list for entry id.'''
        headers = {'content-type': 'application/json',
                   'Authorization': 'OAuth ' + access_token
        }
        request_url = self._get_endpoint('v3/tags') + '/user%2F' + user_id + '%2Ftag%2Fglobal.saved'
        
        params = dict(
                      entryIds=entryIds
                      )
        res = requests.put(url=request_url, data=json.dumps(params), headers=headers)
        return res  	

    def _get_endpoint(self, path=None):
        url = "https://%s" % (self.service_host)
        if path is not None:
            url += "/%s" % path
        return url
    
#                           {'token'=opts.get('token'),
#                            'client_id'=opts.get('client_id'),
#                            'service_host'=opts.get('service_host'),
#                            'client_secret'=opts.get('client_secret')}
   
fclient = get_feedly_client(token=none)
fclient.client_id=FEEDLY_CLIENT_ID
#callback = FEEDLY_REDIRECT_URI
fclient.service_host = opts['service_host']
fclient.client_secret = FEEDLY_CLIENT_SECRET
##res = fclient.get_code_url(callback)
#print(res)
#code = opts['code']


 


                           








