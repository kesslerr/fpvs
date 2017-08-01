#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 11:00:34 2016

@author: Roman Kessler, kesslerr (@med.uni-marburg.de)

THIS IS WORK IN PROGRESS

To Dos:

- change trigger: serial to parallel
- arbitrary task - use that one from my CHF experiment
- prepare images for presentation
- concatenate conditions in a way that makes sense

"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui #, parallel # parallel war ausgeklammert
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import random, itertools
from array import *
import math
import os  # handy system and path functions
import serial


''' define here all criteria necessary 

    condition 1 = standard: objects and faces
        50 seconds
        stimulation frequency 6 Hz
        oddball frequency ~1.2 Hz
        
    condition 2 = faces and fearful faces
    
    
    
    condition 3 = gaze directed to observer as oddball
    
    
    condition 4 = head directed to observer as oddball
        
        
    condition 5 = 


'''

win = visual.Window([1280,1024], waitBlanking=True, fullscr=True,
color=-1, monitor='EEG', units='deg', allowGUI=False)

image = visual.PatchStim(win, 'some.bmp')
image.setAutoLog(False) #
image.draw() # or image.setAutoDraw(True)
win.flip() # stim onset
port.Out32(0x378, trig) #stimulus onset trigger 

# sequence of conditions



# number of runs per condition

##################################### START #################################


_thisDir = os.path.dirname(os.path.abspath(__file__))

os.chdir(_thisDir)

expName = 'rk_FPVS'  # from the Builder filename that created this script
expInfo = {'participant':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])
os.mkdir(_thisDir + os.sep + 'log' + os.sep + 'sub%s' %(expInfo['participant'] ))
logpathname = _thisDir + os.sep + 'log' + os.sep + 'sub%s' %(expInfo['participant'])

logFile = logging.LogFile(filename+'.log', level=logging.INFO, filemode='w')
logging.console.setLevel(logging.error)  # this outputs to the screen, not a file # formerly .warning

endExpNow = False  # flag for 'escape' or other condition => quit the exp

### INDIVIDUAL PARAMETERS FOR SETTING BEFORE EXPERIMENT ###

global emulation
emulation = True
grayvalue = [0,0,0]
oddball_occ = 5 # every 5th stimulus is an oddball

### BEGIN ###

screenfreq = 60.0
t_per_frame = 1000/screenfreq

stim_freq = 6.0 # Hz
frames_per_stim = screenfreq / stim_freq

global TriggerOn_freq
TriggerOn_freq = False
global TriggerOn_odd
TriggerOn_odd = False


### CREATE EXPERIMENTAL WINDOW ###

if emulation == False:
    win = visual.Window(size=(800, 600), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
        monitor='testMonitor', color=grayvalue, colorSpace='rgb',
        blendMode='avg', useFBO=True, units='deg',
        )
else:
    win = visual.Window(size=(800, 600), fullscr=False, screen=0, allowGUI=True, allowStencil=False,
        monitor='testMonitor', color=grayvalue, colorSpace='rgb',
        blendMode='avg', useFBO=True, units='deg',
        )

### SERIAL TRIGGER INITIALISATION

if emulation == False:
    TriggerOutput = serial.Serial("/dev/cu.KeySerial1", timeout=None) # TRIGGER
    global TriggerOn
    TriggerOn = False

time_exp = core.Clock()


# permutate file presentations
face_list = range(0,137)
object_list = range(0,137)

shuffle(face_list)
shuffle(object_list)

### CREATE STIMULUS OBJECT

TheStimulus = visual.ImageStim(win=win, name='TheStimulus',units='pix', 
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=[600,800],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

### introduction
introtext=visual.TextStim(
        win, text='Fixiere immer den roten Punkt in der Mitte.\n\nVersuche wenig zu blinzeln.\n\n\nEs dauert nur 1 Minute!\n\nFixiere, und nach Tastendruck geht es los!',
        font='', pos=(0.0, 0.0), depth=0, rgb=None, color=(1.0, 1.0, 1.0),
        colorSpace='rgb', opacity=1.0, contrast=1.0, units='', ori=0.0,
        height=None, antialias=True, bold=False, italic=False,
        alignHoriz='center', alignVert='center', fontFiles=(),
        wrapWidth=None, flipHoriz=False, flipVert=False, name=None, autoLog=None)
introtext.draw()
fixation = visual.GratingStim(win, mask='circle', size=0.3, pos=[0,0], sf=0, rgb=[1,0,0])
fixation.draw()
win.flip()
event.waitKeys() # wait for a key press to continue
win.flip()

#total_counter=0
oddball_counter=0
frequent_counter=0

# contrast estimates
con = []
for i in range(10):
    con.append(-math.cos( (2 * math.pi ) / 10. * i) )
    con[i] = con[i] / 2 + 0.5
    print(con[i])
    
for nstim in range(0,163):
    print(nstim)
    # oddball
    if nstim % oddball_occ == 4:
        TheStimulus.setImage('/media/cth/Samsung_T3/FPVS/paradigm/stimuli/Faces_fearful/' + str(face_list[oddball_counter]) + '.jpg')
        if emulation == False:
            win.callOnFlip(TriggerOutput.setDTR, True)
            TriggerOn_odd = True
        #print(oddball_counter)
        oddball_counter += 1
    # frequent
    else:
        TheStimulus.setImage('/media/cth/Samsung_T3/FPVS/paradigm/stimuli/Faces_neutral/' + str(object_list[frequent_counter]) + '.jpg')
        if emulation == False:
            win.callOnFlip(TriggerOutput.setDTR, True)
            TriggerOn_freq = True
        frequent_counter += 1
    
    TheStimulus.draw(win=win)
    fixation = visual.GratingStim(win, mask='circle', size=0.3, pos=[0,0], sf=0, rgb=[1,0,0])
    fixation.draw()
    win.flip() #''' #### Start-Frame!! t=0 #### '''
    
    # wait for the correct frame to present stimulus
    framecounter = 0
    while framecounter < 10:
        if emulation == False:
            if framecounter == 2:
                if TriggerOn_freq == True:
                    TriggerOn_freq = False
                    win.callOnFlip(TriggerOutput.setDTR, False)
            elif framecounter == 5:
                if TriggerOn_odd == True:
                    TriggerOn_odd = False
                    win.callOnFlip(TriggerOutput.setDTR, False)
        
        TheStimulus.setContrast(con[framecounter])        
        TheStimulus.draw(win=win)
        fixation = visual.GratingStim(win, mask='circle', size=0.3, pos=[0,0], sf=0, rgb=[1,0,0])
        fixation.draw()
        win.flip()
        framecounter += 1
    
introtext=visual.TextStim(
        win, text='Geschafft!\n\n',
        font='', pos=(0.0, 0.0), depth=0, rgb=None, color=(1.0, 1.0, 1.0),
        colorSpace='rgb', opacity=1.0, contrast=1.0, units='', ori=0.0,
        height=None, antialias=True, bold=False, italic=False,
        alignHoriz='center', alignVert='center', fontFiles=(),
        wrapWidth=None, flipHoriz=False, flipVert=False, name=None, autoLog=None)
introtext.draw()
fixation = visual.GratingStim(win, mask='circle', size=0.3, pos=[0,0], sf=0, rgb=[1,0,0])
fixation.draw()
win.flip()
event.waitKeys() # wait for a key press to continue
win.flip()

win.close()
