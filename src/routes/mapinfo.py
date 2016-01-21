# -*- coding: utf-8 -*-
'''
Created on 16 janv. 2016

@author: romain
'''

import decimal
import falcon
from psycopg2.extensions import adapt

import db

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
        
        raw_lat = req.get_param('lat')
        raw_lon = req.get_param('lon')
        if raw_lat is None or raw_lon is None:
            resp.status = falcon.HTTP_400
            lat = None
            lon = None
        else:
            lat = decimal.Decimal(raw_lat)
            lon = decimal.Decimal(raw_lon)
        
        if not (self.lat_is_valid(lat) and self.lon_is_valid(lon)):
            resp.status = falcon.HTTP_400
        else:
            dbc = db.connect()
            cur = dbc.cursor()
            
            nb_maps_raw = req.get_param('nb_maps')
            nb_addr_raw = req.get_param('nb_addr')
            if nb_maps_raw is None:
                nb_maps_raw = '20'
            if nb_addr_raw is None:
                nb_addr_raw = '10'
            nb_maps = decimal.Decimal(nb_maps_raw)
            nb_addr = decimal.Decimal(nb_addr_raw)

            #id (uuid), path (str), geom (geom), address (str), level (str), building (str)
            loc = "st_setsrid(st_makepoint(%s,%s),4326)" % (lon,lat)
            query = "SELECT array_to_json(array_agg(row_to_json(t)))::text FROM ("
            query += " SELECT floor(st_distance(geom::geography, %s::geography)) as dist, " % loc
            query += " ST_X(geom) as lon, ST_Y(geom) as lat, id, address, level, building, name FROM ((select * from ban_nomap where ST_DWithin(geom, %s, 0.001) order by st_distance(geom,%s) limit %s) union (select * from map_info where ST_DWithin(geom, %s, 0.1) limit %s)) as d ORDER BY ST_Distance(geom,%s), level" % (
                        loc,loc,adapt(nb_addr),loc,adapt(nb_maps),loc)
            query += " ) t"
            cur.execute(query)
            what_is_around = cur.fetchone()[0]

            
            resp.set_header('X-Powered-By', 'OpenEvacMap')
            if what_is_around is None:
                resp.status = falcon.HTTP_204
            else:
                resp.status = falcon.HTTP_200
                resp.set_header('Access-Control-Allow-Origin', '*')
                resp.set_header('Access-Control-Allow-Headers', 'X-Requested-With')
                resp.body = (what_is_around)

                query = """INSERT INTO log (loc, ip) VALUES (ST_SetSRID(ST_GeometryFromText('POINT(%s %s)'),4326),'%s');""" % (lon,lat,req.env['REMOTE_ADDR'])
                cur.execute(query)
                dbc.commit()

            cur.close()
            dbc.close()

