# -*- coding: utf-8 -*-

import sys
import os

class MapCache():
    def  __init__(self):
        self.map = {}
        
    def put(self, key, value):
        if key in self.map:
            return False
            
        self.map[key] = value
        return True
        
    def get(self, key):
        if key in self.map:
            return self.map[key]
        return None
        
    def update(self, key, value):
        self.map[key] = value
            
        
        