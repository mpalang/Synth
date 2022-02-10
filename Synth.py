# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 11:36:00 2022

@author: Mo
"""
import lib.functions as sy
import csv


sound=sy.synth('g#', 
               octave=3, 
               No=1, 
               form='sine', 
               detune=0, 
               effects={'Moeffect': 50,
                        'Fuzz': 70}
               )

