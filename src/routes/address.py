# -*- coding: utf-8 -*-
'''
Created on 16 janv. 2016

@author: romain
'''

import decimal
import falcon
import json
import os

import config
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
        if not ('image' in patch and
                'lat' in patch and
                'lon' in patch):
            raise ValueError("Missing mandatory key/values in patch")
        
        return patch

    def verify_address_id(self, address_id):
        
        if address_id is None:
            raise ValueError("Address ID is None")
        
    def on_patch(self, req, resp, **kargs):
        '''Update database according to JSON and give ID back
        '''
        
        address_id = kargs.get('id')
        patch_json = req.stream.read().decode('utf-8')
        print(patch_json)
        try:
            self.verify_address_id(address_id)
            patch = self.get_json_list(patch_json)
        except:
            resp.status = falcon.HTTP_400
            raise
        else:
            cur = db.cursor()
            
            columns = ['address','path']
            values = ["'%s'" % address_id,"'/tmp'"]
            
            
            lat = decimal.Decimal(patch.pop('lat'))
            lon = decimal.Decimal(patch.pop('lon'))

            for key, value in patch.items():
                if value is not None:
                    columns.append(key)
                    values.append("'%s'" % value)
            
            columns.append('geom')
            values.append('st_Setsrid(st_makePoint(%s,%s),4326)' % (lat, lon))
            
            insert = "INSERT INTO maps (%s)" % ",".join(columns)
            insert += " VALUES (%s)" % ",".join(values)
            insert += " RETURNING *"
            cur.execute(insert)
            print(cur.query)
            print(cur.fetchone())
            
            #image_data = patch.pop('image')
            #image_path = os.path.join(config.map_dir, "%s.jpg" % uuid)

            #with open(image_path, "wb") as f:
            #    f.write(image_data)
            
            db.commit()
            cur.close()
