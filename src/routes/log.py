# -*- coding: utf-8 -*-
'''
Created on 16 janv. 2016

@author: christian
'''

import falcon
import os
from PIL import Image
from psycopg2.extensions import adapt

import config
import db


class Log(object):
    '''
    Get logged data
    '''

    _table = "log"
    
    def on_get(self, req, resp):
            '''Return logged requests
            '''
            
            dbc = db.connect()
            cur = dbc.cursor()
            
            query = """select format('{ "type": "FeatureCollection", "features": [%s]}',string_agg(j,',')) from (select format('{"type": "Feature", "geometry": %s, "properties": {"age": "%s"}}', st_asgeojson(loc),floor(EXTRACT(epoch FROM age(now(),time)))) as j from log where time > now()- interval '2 hour' order by time desc) as p;"""
            cur.execute(query)
            log_data = cur.fetchone()[0]

            resp.set_header('X-Powered-By', 'OpenEvacMap')
            if log_data is None:
                resp.status = falcon.HTTP_404
            else:
                resp.status = falcon.HTTP_200
                resp.set_header('Access-Control-Allow-Origin', '*')
                resp.set_header('Access-Control-Allow-Headers', 
                                'X-Requested-With')
                resp.body = (log_data)

            cur.close()
            dbc.close()


