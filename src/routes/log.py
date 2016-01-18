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
            
            #id (uuid), path (str), geom (geom), address (str), level (str), building (str)
            query = "SELECT array_to_json(array_agg(row_to_json(t)))::text FROM (select EXTRACT(epoch FROM age(time,now()))::integer as age, st_asgeojson(loc) as geometry from log where time > now()- interval '1 hour') as t;"
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


