# -*- coding: utf-8 -*-
'''
Created on 16 janv. 2016

@author: romain
'''

import cgi
import decimal
import falcon
import os

import config
from db import db

class Address(object):
    '''
    Patch maps information related to an address
    '''
    
    _table = "maps"

    def lat_is_valid(self, lat):
        
        lat_is_valid = True
        if lat is None:
            lat_is_valid = False
        return lat_is_valid
    
    def lon_is_valid(self, lon):
        lon_is_valid = True
        if lon is None:
            lon_is_valid = False
        return lon_is_valid


    def verify_address_id(self, address_id):
        
        if address_id is None:
            raise ValueError("Address ID is None")
        
    def on_options(self, req, resp, **kargs):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'POST')
        resp.set_header('Access-Control-Allow-Headers', 
                        'X-Requested-With, Content-Type')
        resp.status = falcon.HTTP_204
        
        
    def on_post(self, req, resp, **kargs):
        '''Update database according to JSON and give ID back
        '''
        
        
        address_id = kargs.get('id')

        env = req.env
        env.setdefault('QUERY_STRING', '')
        
        form = cgi.FieldStorage(fp=req.stream, environ=env)
        try:
            file_item = form['image']
            raw_lat_item = form['lat']
            raw_lon_item = form['lon']
        except KeyError:
            raw_lat = None
            raw_lon = None
            image_file = None
        else:
            image_file = file_item.file
            raw_lat = raw_lat_item.value
            raw_lon = raw_lon_item.value
        
        if raw_lat is None or raw_lon is None or image_file is None:
            resp.status = falcon.HTTP_400
            lat = None
            lon = None
        else:
            lat = decimal.Decimal(raw_lat)
            lon = decimal.Decimal(raw_lon)
        
        if not (self.lat_is_valid(lat) and self.lon_is_valid(lon)):
            resp.status = falcon.HTTP_400
        else:
            cur = db.cursor()
            
            columns = ['geom', 'address']
            values = ['st_Setsrid(st_makePoint(%s,%s),4326)' % (lon, lat),
                      "'%s'" % address_id]
            for param in ('name','building','level'):
                try:
                    param_item = form[param]
                except KeyError:
                    pass
                else:
                    columns.append(param)
                    values.append("'%s'" % param_item.value)
            
            insert = "INSERT INTO %s (%s)" % (self._table, ",".join(columns))
            insert += " VALUES (%s)" % ",".join(values)
            insert += " RETURNING *"
            cur.execute(insert)

            uuid = cur.fetchone()[0]

            image_path = os.path.join(config.map_dir, "%s.jpg" % uuid)
            
            with open(image_path, "wb") as f:
                f.write(image_file.read())
            
            cur2 = db.cursor()
            update = "UPDATE %s" % self._table
            update += " SET path='%s'" % image_path
            update += " WHERE id='%s'" % uuid
            cur2.execute(update)
            db.commit()
            cur.close()
            cur2.close()
            resp.status = falcon.HTTP_200
            resp.set_header('Access-Control-Allow-Origin', '*')
            resp.set_header('Access-Control-Allow-Headers', 'X-Requested-With')

