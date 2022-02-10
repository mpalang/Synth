# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 20:57:05 2022

@author: Mo
"""

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from random import random

import csv

from scipy.io import wavfile
from scipy import signal as si
# import simpleaudio as sa

#%%

def oszi(f, form='sine', duration=3, sampleRate=44100 ):
    
    """
    creates the basic signal. Note can be either specified in Hz or the musical denotation as string (e.g. 'a' for 440 Hz).
    """
    
    note_frequencies={}
    with open('lib/note_frequencies.csv','r',newline='') as file:
        csv_reader=csv.reader(file)
        for row in csv_reader:
            note_frequencies[row[0]] =  float(row[1])
    
    t = np.linspace(0, duration, sampleRate*duration, False)
    
    if type(f)==float:
        fHz=f
        
    if type(f)==str:
        fHz=note_frequencies[f]
        
   
    
    if form=='sine':
        y=np.sin(2*np.pi*fHz* t)
    
    if form=='sawtooth':
        y=si.sawtooth(2 * np.pi * fHz * t)
    
    if form=='square':
        y=si.square(2*np.pi*fHz*t, duty=0.5)
        
    
    return t,y

def verzerrer(y, amount, volume):
    y_v=y.copy()
    y_max=np.max(y)
    y_min=np.min(y)
    distp=(1-amount)*y_max
    distm=(1-amount)*y_min
    
    for i,v in enumerate(y_v):
        if v > distp:
            y_v[i]=y[i]-random()*(y_max-distp)
        if v < distm:
            y_v[i]=y[i]+random()*(-(y_min-distm))
            
        
    
    return y_v*volume
    
        
        
# def playSound(sound, sampleRate=44100):
    
#     play_obj = sa.play_buffer(sound, 1, 2, sampleRate)
#     play_obj.wait_done()

def exportaswave(sound, filename='sound.wav', sampleRate=44100):
    wavfile.write('sound.wav',sampleRate,sound)
    return filename
    

def chord(sound):
    
    chord_init=(1,1.5)
    chord=[]
    
    for i in chord_init:
    
        chord.append(sound)
    
    dump=np.zeros(chord[0].shape)
    
    for i in chord:
        dump=dump+i
    
    return chord
    
def synth(f,No=1,duration=3,detune=0, form='sine', scale=False, chord=None, sampleRate=44100, saveoption=True):
    

        
    if scale:
        
        note_frequencies={}
        sound=[]
        with open('lib/note_frequencies.csv','r',newline='') as file:
            csv_reader=csv.reader(file)
            for row in csv_reader:
                note_frequencies[row[0]] =  float(row[1])

        for note in note_frequencies.keys():
            t,step=oszi(note_frequencies[note], form=form, duration=duration, sampleRate=sampleRate)
            sound=np.append(sound,step)
            
        t=np.append(t,[t]*(int(len(sound)/len(t))-1))  
        
    else:
        t,sound=oszi(f,form)
    
    for i in range(No-1):
        sound2=oszi(f*i+detune*(i+1))[1]
        sound=sound+sound2
        
     
    if chord:
        sound=chord(sound)
        
    
    # if shape
    plot(t,sound)
    plt.xlim(0,500/sampleRate)   
        
    
    if saveoption:
        exportaswave((sound*(2**15-1)/np.max(np.abs(sound))).astype(np.int16))

        

    

    
    