#!/usr/bin/env python2.7
#coding=utf-8
import os
import sys

def enum(**enums):
    return type('Enum', (), enums)
 
Event = enum(ReadEvent = 1, 
             WriteEvent = 2, 
             ErrorEvent = 3
             )

if __name__ == '__main__':
    pass