# -*- coding: utf-8 -*-
'''
Created on 21 janv. 2016

@author: christian
'''

import falcon
import os

import config
import db


class Stat(object):
    '''
    Get global statistics
    '''

    def on_get(self, req, resp):
            '''Return global statistics
            '''
            
            dbc = db.connect()
            cur = dbc.cursor()
            
            query = """select format('{"nb_maps":%s,"nb_addr":%s,"last_map":"%s"}',
                count(*),
                count(distinct(address)),
                left(max(time)::text,19)) as stats from maps;"""
            cur.execute(query)
            stats = cur.fetchone()[0]

            resp.set_header('X-Powered-By', 'OpenEvacMap')
            if log_data is None:
                resp.status = falcon.HTTP_404
            else:
                resp.status = falcon.HTTP_200
                resp.set_header('Access-Control-Allow-Origin', '*')
                resp.set_header('Access-Control-Allow-Headers', 
                                'X-Requested-With')
                resp.body = (stats)

            cur.close()
            dbc.close()

