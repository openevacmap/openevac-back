# -*- coding: utf-8 -*-
'''
Created on 16 janv. 2016

@author: romain
'''

import falcon
import os
import config
from PIL import Image

from db import db

preview_size = 600,600

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

        map_id = req.get_param('id')
        if not self.map_id_is_valid(map_id):
            resp.status = falcon.HTTP_400
        else:
            cur = db.cursor()
            
            #id (uuid), path (str), geom (geom), address (str), level (str), building (str)
            query = "SELECT path FROM %s" % self._table
                    # Look at 1/10 (0.1) degrees around spot.
            query += " WHERE id='%s'" % (map_id)
            cur.execute(query)
            map_path = cur.fetchall()[0][0]
            

            resp.set_header('X-Powered-By', 'OpenEvacMap')
            if map_path is None:
                resp.status = falcon.HTTP_404
            else:
                full_path = os.path.join(config.map_dir,map_path)
                preview = req.get_param('preview')
                if preview is None:
                    preview = '0'
                if preview=='1':
                    outfile = os.path.splitext(full_path)[0] + "_preview.jpg"
                    print(outfile)
                    if os.path.exists(outfile)==False:
                        im = Image.open(full_path)
                        im.thumbnail(preview_size, Image.ANTIALIAS)
                        im.save(outfile, "JPEG")
                    full_path=outfile
                resp.status = falcon.HTTP_200
                resp.set_header('Access-Control-Allow-Origin', '*')
                resp.set_header('Access-Control-Allow-Headers', 
                                'X-Requested-With')
                resp.set_header("Content-Type", "image/jpeg")
                resp.set_header("Content-Length", "%s" % os.path.getsize(
                                                                    full_path))
                with open(full_path, "rb") as f:
                    resp.body = f.read()
