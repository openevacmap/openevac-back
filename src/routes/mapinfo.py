# -*- coding: utf-8 -*-
'''
Created on 16 janv. 2016

@author: romain
'''

import decimal
import falcon
import psycopg2

class MapInfo(object):
    '''
    Manage map info requests 
    '''

    _table = "map_info"

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

    def on_get(self, req, resp):
        '''Return json object related to GET with lat & lon HTTP parameters
        '''
        if not hasattr(req, "params"):
            resp.status = falcon.HTTP_400
            lat = None
            lon = None
        else:
            lat = decimal.Decimal(req.params.get('lat'))
            lon = decimal.Decimal(req.params.get('lon'))
        
        if not (self.lat_is_valid(lat) and self.lon_is_valid(lon)):
            resp.status = falcon.HTTP_400
        else:
            db = psycopg2.connect("dbname=evac user=romain")
            cur = db.cursor()
            
            
            #id (uuid), path (str), geom (geom), address (str), level (str), building (str)
            query = "SELECT array_to_json(array_agg(row_to_json(t))) FROM ("
            query += " SELECT address, level, building, id, address_label FROM %s" % self._table
                    # Look at 1/10 (0.1) degrees around spot.
            query += " WHERE ST_DWithin(ST_SetSRID(ST_MakePoint(%s,%s),4326),geom,0.1)" % (lon,lat)
            query += " ORDER BY ST_Distance(geom,ST_SetSRID(ST_MakePoint(%s,%s),4326))" % (lon,lat)
            query += " LIMIT 40"
            query += " ) t"
            cur.execute(query)
            what_is_around = cur.fetchall()[0][0]
            
            resp.set_header('X-Powered-By', 'OpenEvacMap')
            if what_is_around is None:
                resp.status = falcon.HTTP_204
            else:
                resp.status = falcon.HTTP_200
                resp.set_header('Access-Control-Allow-Origin', '*')
                resp.set_header('Access-Control-Allow-Headers', 'X-Requested-With')
                resp.body = (what_is_around)
            
            db.close()
