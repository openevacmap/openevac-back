# -*- coding: utf-8 -*-
'''
Created on 16 janv. 2016

@author: romain
'''

import falcon
import os
import psycopg2

class Map(object):
    '''
    Get the map according to the UUID
    '''

    _table = "maps"
    
    def map_id_is_valid(self, map_id):
        
        is_valid = True
        if map_id is None:
            is_valid = False
        return is_valid

    def on_get(self, req, resp):
        '''Return JPEG map image according to id param
        '''
        
        print("toto")
        map_id = req.get_param('id')
        print(map_id)
        if not self.map_id_is_valid(map_id):
            resp.status = falcon.HTTP_400
        else:
            db = psycopg2.connect("dbname=evac user=romain")
            cur = db.cursor()
            
            #id (uuid), path (str), geom (geom), address (str), level (str), building (str)
            query = "SELECT path FROM %s" % self._table
                    # Look at 1/10 (0.1) degrees around spot.
            query += " WHERE id='%s'" % (map_id)
            print(query)
            cur.execute(query)
            map_path = cur.fetchall()[0][0]
            
            resp.set_header('X-Powered-By', 'OpenEvacMap')
            if map_path is None:
                resp.status = falcon.HTTP_404
            else:
                resp.status = falcon.HTTP_200
                resp.set_header('Access-Control-Allow-Origin', '*')
                resp.set_header('Access-Control-Allow-Headers', 
                                'X-Requested-With')
                resp.set_header("Content-Type", "image/jpeg")
                resp.set_header("Content-Length", "%s" % os.path.getsize(
                                                                    map_path))
                with open(map_path, "rb") as f:
                    resp.body = f.read()

            db.close()
