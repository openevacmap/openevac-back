# -*- coding: utf-8 -*-
'''
Created on 16 janv. 2016

@author: romain
'''

import falcon
import routes

# falcon.API instances are callable WSGI apps
app = falcon.API()


# things will handle all requests to the matching URL path
app.add_route('/v0/maps-info', routes.mapinfo)
app.add_route('/v0/map', routes._map)
app.add_route('/v0/addresses/{id}', routes.address)
app.add_route('/v0/log', routes.log)
app.add_route('/v0/stats', routes.stat)
