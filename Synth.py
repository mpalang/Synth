# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 11:36:00 2022

@author: Mo
"""
import lib.functions as sy
import csv


sound=sy.synth('g#',No=1,form='sawtooth',detune=10, scale=True, duration=1)



# note_frequencies={}

# note_frequencies['a']=440

# note_frequencies['a2']=note_frequencies['a']*2

# notes=['a','a#','h','c','c#','d','d#','e','f','f#','g','g#']

# for i,n in enumerate(notes):
#     note_frequencies[n]=440+i*(440*2-440)/12


# with open('lib/note_frequencies.csv', 'w', newline='') as f:
#     csv_writer=csv.writer(f)
#     for row in note_frequencies.keys():
#         csv_writer.writerow((row,note_frequencies[row]))
    