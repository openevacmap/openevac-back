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

    def verify_address_id(self, address_id):
        
        if address_id is None:
            raise ValueError("Address ID is None")
        
    def on_patch(self, req, resp, **kargs):
        '''Update database according to JSON and give ID back
        '''
        
        address_id = kargs.get('id')
        patch_json = req.stream.read().decode('utf-8')
        
        try:
            self.verify_address_id(address_id)
            patch = self.get_json_list(patch_json)
        except:
            resp.status = falcon.HTTP_400
        else:
            cur = db.cursor()
            
            columns = ['address','path']
            values = ["'%s'" % address_id,"'/tmp'"]
            
            for key, value in patch.items():
                if value is not None:
                    columns.append(key)
                    values.append(value)
            
            insert = "INSERT INTO maps (%s)" % ",".join(columns)
            insert += " VALUES (%s)" % ",".join(values)
            
            cur.execute(insert)
            db.commit()
            cur.close()
