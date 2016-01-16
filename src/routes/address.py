# -*- coding: utf-8 -*-
'''
Created on 16 janv. 2016

@author: romain
'''

import falcon
import json

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

    def get_json_list(self, patch_json):
        
        if not self.patch_json_is_valid(patch_json):
            raise ValueError("None found, expected a JSON string")
        
        patch = json.loads(patch_json)
        
        if not isinstance(patch, dict):
            raise ValueError("Json does not contain a dict")
        return patch

    def on_patch(self, req, resp):
        '''Update database according to JSON and give ID back
        '''
        
        patch_json = req.stream.read().decode('utf-8')
        
        try:
            patch = self.get_json_list(patch_json)
        except:
            resp.status = falcon.HTTP_400
        else:
            print(patch)
            return