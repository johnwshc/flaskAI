# -*- coding: utf-8 -*-
"""
Created on Thu May 24 15:23:57 2018

@author: johnc
"""

from eyed3 import id3

tag = id3.Tag()
tag.parse("emma.mp3")
print(tag.artist)