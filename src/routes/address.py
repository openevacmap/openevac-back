# -*- coding: utf-8 -*-
'''
Created on 16 janv. 2016

@author: romain
'''

import falcon

from db import db

class Address(object):
    '''
    Patch maps information related to an address
    '''

    def patch_json_is_valid(self, patch_json):
        
        is_valid = True
        if patch_json is None:
            is_valid = False
        return is_valid

    def on_patch(self, req, resp):
        '''Update database according to JSON and give ID back
        '''
        
        
        patch_json = req.stream.read()
        print(patch_json)
        if not self.patch_json_is_valid(patch_json):
            resp.status = falcon.HTTP_400
        else:
            return