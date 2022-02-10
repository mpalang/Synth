#%% Preface
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

import logging
import sys

#%% Basics

# def playSound(sound, sampleRate=44100):
    
#     play_obj = sa.play_buffer(sound, 1, 2, sampleRate)
#     play_obj.wait_done()

def exportaswave(sound, filename, sampleRate):
    wavfile.write(filename,sampleRate,sound)
    return filename

def plotSound(t,sound,sampleRate):
    
    plot(t,sound)
    plt.xlim(0,1000/sampleRate)

def oszi(f, octave, detune, form, duration, sampleRate):
    
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
        
    fHz=fHz+fHz*detune/1000
    
    fHz= fHz*(2**(octave-4))
    
    if form=='sine':
        y=np.sin(2*np.pi*fHz* t)
    
    if form=='sawtooth':
        y=si.sawtooth(2 * np.pi * fHz * t)
    
    if form=='square':
        y=si.square(2*np.pi*fHz*t, duty=0.5)
        
    if form=='triangle':
        y=si.sawtooth(2 * np.pi * fHz * t, 0.5)
        
    if form=='sawtooth-reverse':
        y=si.sawtooth(2 * np.pi * fHz * t, 0)
        
    
    return t,y

#%% ####Effects#####


def fuzz(y, parms):
    
    amount=parms
    
    if not amount:
        amount=20
        
    y_v=y.copy()
    y_max=np.max(y)
    y_min=np.min(y)
    distp=y_max*(1-amount/100)
    distm=y_min*(1-amount/100)
    
    for i,v in enumerate(y_v):
        if v > distp:
            y_v[i]=distp
        if v < distm:
            y_v[i]=distm
            
        
    return y_v
    
        
def moeffect(sound, parms):
    
    amount=parms
    
    sound2=np.zeros(len(sound))
    for i,v in enumerate(sound):
        if i+amount<len(sound)-1:
            sound2[i]=sound[i+amount]
        else:
            sound2[i]=sound[i+amount-(len(sound)-1)]    
            
    sound=sound+sound2
    
    return sound

    
#%% Execute #########

    
def createSound(f, No, form, octave, duration, detune, effects, sampleRate):
    
    if type(f)!=list:
    
        f=[f]
        
    if not detune:
        detune=[0]*No
        
    else:
        if type(detune)!=list:
            detune=[detune]
            
    if len(detune)!=No:
        logging.error('Detune and Notes must have the same number of values!')
        sys.exit()
        
    
    if type(form)!=list:
        form=[form]*No
        
    else:
        if not len(detune)==No:
            logging.error('Form and Number of Oscillators must have the same number of values if written as list!')
            sys.exit()
    
        
    sound=np.zeros(duration*sampleRate)
   
    for i,v in enumerate(f):
        
        for j,u in enumerate(range(No)):
            
            t,o=oszi(v, octave, detune[j], form[j], duration, sampleRate)
            sound=sound+o
            
    if 'Fuzz' in effects.keys():
         
         sound=fuzz(sound, effects['Fuzz'])
         
    if 'Moeffect' in effects.keys():
        
        sound=moeffect(sound, effects['Moeffect'])

        
    
    
    return t,sound




def synth(f,
          octave=4,
          No=1,
          duration=3,
          detune=False, 
          form='sine', 
          scale=False,
          effects={},
          volume=1,
          sampleRate=44100, 
          saveoption=True,
          filename='sound.wav'):
    
    
    if scale:
        
        note_frequencies={}
        sound=[]
        with open('lib/note_frequencies.csv','r',newline='') as file:
            csv_reader=csv.reader(file)
            for row in csv_reader:
                note_frequencies[row[0]] =  float(row[1])
    
    else:
        
        t,sound=createSound(f, No, form, octave, duration, detune, effects, sampleRate) 
    
    sound = sound*volume/np.max(sound)

    plotSound(t,sound,sampleRate)
    
    exportaswave(sound, filename, sampleRate)
          
      