# -*- coding: utf-8 -*-
'''
Created on 16 janv. 2016

@author: romain
'''

import falcon
import routes

if __name__ == '__main__':
    
    # falcon.API instances are callable WSGI apps
    app = falcon.API()
    
    
    # things will handle all requests to the matching URL path
    app.add_route('/maps-info', routes.mapinfo)
