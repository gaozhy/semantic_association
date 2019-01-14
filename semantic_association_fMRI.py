# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 11:51:47 2019
1: Task description:
    The participants were asked to make the judgement about whether the two consective 
word (probe first and target then) were semantic related or not.

2: Slow event fMRI design, trial structure:
    probe(2s), fix1(2s), target(2s,yes/no), fix2(6s).
    
3: 4 runs, each run with 45 trials

4: conditions: Unrelated, Weak association, Medium association, Strong association. 
    unr,60; wse,40; mse,40; sse,40.
    
@author: zg750
"""




from psychopy import visual, core, monitors, event, sound, gui, logging
from datetime import datetime
from random import shuffle
import os
import time
import csv
import sys, os, errno # to get file system encoding (used in setDir())
import numpy as np
import random
from collections import OrderedDict

# Experiment constants
instruct_figure = 'instruction.jpg'
trigger_figure = 'trigger.png'
ready_figure = 'ready.png'
expName = 'SemanticRelationJudgement'  # the experiment name
data_folder = 'data' + '_' +  expName  # make a directory to store data
stimuli_name = 'sem_stim_run'

# assign the monitor name                                                                                                                                                                                                                                          
monitor_name = 'HP ProOne 600'

# window size = x, y
win_size_x = 800
win_size_y = 600

# window background color
win_bg_col   = (1.0,1.0,1.0) # background color is black
win_text_col = (-1,-1,-1)  # text color is white

# instruction, position height (font size)
instru_pos = (0,0) # (0,0) indicates the central position
probe_pos = (0,0)
fix_pos = (0,0)
target_pos = (0,0)
yes_pos = (-250,-180)
no_pos = (250,-180)
image_pos = (0,0) # instruction and trigger and get ready would be shown in images

instru_h = 62 # what is this? 
text_h = 62
yes_no_h = 62



num_skip_trials = 1  # the number of trials that can be skipped, used for testing the scirpt


num_trials = 45 # total trial numbers of each run 


# presentation time of clue and probe
probe_durat =2
fix1_durat = 2
target_durat = 2
fix2_durat = 6


# response time 
timelimit_deci = 4
# slow event related design with each trial lasts 10 second.
trial_duration = 12


## define functions
# get the current directory of this script - correct
def get_pwd():
    global curr_dic
    curr_dic = os.path.dirname(sys.argv[0])  # U:/task_fMRI_Experiment/exp_March
    return curr_dic
    
# make a folder in the current directory used to store data  - correct
def makedir(folder_name):
    os.chdir(curr_dic)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


# quit functions  - to allow subjects to quit the experiment  - correct
def shutdown ():
    win.close()
    core.quit()
    
# get the participants info, initialize the screen and create a data file for this subject
def info_gui(expName):
    # Set up a dictionary in which we can store our experiment details
    expInfo={}
    expInfo['expname'] =expName
    # Create a string version of the current year/month/day hour/minute
    expInfo['expdate']=datetime.now().strftime('%Y%m%d_%H%M')
    expInfo['subjID']=''
    expInfo['subjName']=''
    expInfo['run']=''
    
    # Set up our input dialog
    # Use the 'fixed' argument to stop the user changing the 'expname' parameter
    # Use the 'order' argumennt to set the order in which to display the fields
    dlg = gui.DlgFromDict(expInfo,title='input data', fixed = ['expname','expdate'],order =['expname','expdate','subjID','subjName','run'])
    
    if not dlg.OK:
        print ('User cancelled the experiment')
        core.quit()
   
# creates a file with a name that is absolute path + info collected from GUI
    filename = data_folder + os.sep + '%s_%s_%s_%s.csv' %(expInfo['subjID'], expInfo['subjName'], expInfo['expdate'], expInfo['run'])
    stimuli_file = stimuli_name +expInfo['run']+'.csv'
    return expInfo, filename,stimuli_file
# to avoid overwrite the data. Check whether the file exists, if not, create a new one and write the header.
# Otherwise, rename it - repeat_n
# correct
def write_file_not_exist(filename):
    repeat_n = 1
    while True:
        if not os.path.isfile(filename):
            f = open(filename,'w')
           # f.write(header)
            break
        else:
            filename = data_folder + os.sep + '%s_%s_%s_repeat_%s.csv' %(expInfo['subjID'], expInfo['subjName'], expInfo['expdate'],str(repeat_n))
            repeat_n = repeat_n + 1


# Open a csv file, read through from the first row   # correct
def load_conditions_dict(conditionfile):

#load each row as a dictionary with the headers as the keys
#save the headers in its original order for data saving

# csv.DictReader(f,fieldnames = None): create an object that operates like a regular reader 
# but maps the information in each row to an OrderedDict whose keys
# are given by the optional fieldnames parameter.

    with open(conditionfile) as csvfile:
        reader = csv.DictReader(csvfile)
        trials = []

        for row in reader:
            trials.append(row)
    
    # save field names as a list in order
        fieldnames = reader.fieldnames  # filenames is the first row, which used as keys of trials

    return trials, fieldnames   # trial is a list, each element is a key-value pair. Key is the 
                                # header of that column and value is the corresponding value

# Create the log file to store the data of the experiment 
# create the header

            
def write_header(filename, header):
    with open (filename,'a') as csvfile:
        fieldnames = header
        data_file = csv.DictWriter(csvfile,fieldnames=fieldnames,lineterminator ='\n')
        data_file.writeheader()
        
#write each trial
def write_trial(filename,header,trial):
    with open (filename,'a') as csvfile:
        fieldnames = header
        data_file = csv.DictWriter(csvfile,fieldnames=fieldnames,lineterminator ='\n')
        data_file.writerow(trial)



# generate the ideal onset of each trial

def gen_ideal_onset(num_trials):
    
    ideal_trial_onset =[]
    
    for trial_num in range(1, num_trials+1,1):
        

        trial_onset = trial_duration*(trial_num -1)

        ideal_trial_onset.append(trial_onset)
    return ideal_trial_onset 

# set up the window
# fullscr: better timing can be achieved in full-screen mode
# allowGUI: if set to False, window will be drawn with no frame and no buttons to close etc...

def set_up_window(): 
    mon = monitors.Monitor(monitor_name)
    mon.setDistance (114)
    win = visual.Window([win_size_x,win_size_y],fullscr = True, monitor = mon,allowGUI = True, winType = 'pyglet', units="pix",color=win_bg_col)
    win.mouseVisible = False  # hide the mouse
    return win
        
# read the content in the csv or text file
def read_cont (filename):
    f = open(filename,'r')
    return f

# prepare the content on the screen - content is text
def prep_cont(line, pos, height):
    line_text = visual.TextStim(win,line,color = win_text_col,pos = pos,height = height)
    return line_text


# prepare the content on the screen - pictures
# create an image stimulus for presenting the images in
# set this to None and then you can update as you go by calling in images from a file for example
    
    # prepare the image on the screen 
def prep_image(image,pos):
    image_stim = visual.ImageStim(win,image,pos = pos)
    return image_stim
    
# display the content on the screen
def disp_instr_cont(line):
    line.draw()
    win.flip()
    keys = event.waitKeys(keyList =['return','escape'])
    if keys[0][0]=='escape':
        shutdown()
        

def instruct(path,instruct_figure):
    """
    path is where the instruct figure stored
    instruct_figure is the name of instruct_figure
    """
    imstim = visual.ImageStim(win,image = os.path.join(path,instruct_figure),pos = instru_pos)
    imstim.draw()
    event.clearEvents()
    instru_onset = win.flip()
    keys = event.waitKeys(keyList =['return','escape'],timeStamped = True)
    if keys[0][0]=='escape':
        shutdown()
    
def trigger_exp():

    trigger = prep_cont('experiment starts soon',instru_pos,instru_h)
    trigger.draw()
    win.flip()
    
def ready():

    trigger = prep_cont('experiment starts soon',instru_pos,instru_h)
    trigger.draw()
    ready_onset = win.flip()
    return ready_onset
    
def end_exp():

    trigger = prep_cont('End of Experiment',instru_pos,instru_h )
    trigger.draw()
    end_onset = win.flip()
    keys = event.waitKeys(keyList =['return'],timeStamped = True)
    print ('end of experiment:',end_onset)
    shutdown()
    return end_onset



        
# display each trial on the screen at the appropriate time
def run_stimuli(stimuli_file,fixa_list):
    """
    stimuli file is sem_stim_runi.csv file, including the stimuli for each run
    
    fixa_list is a list, including random jittered fixation time for each trial
    
    """
    # read the stimuli  # re-define, not use numbers, but use keywords
    all_trials, headers = load_conditions_dict(conditionfile=stimuli_file)
    headers += ['trial_ID', 'conditions','AssociaitonStrength', 'probe_onset','probe_durat', 'fixa1_onset', 'fixa1_durat', 'target_onset', 'target_durat','target_offset','fixa2_onset','fixa2_durat','RT', 'correct','KeyPress'] 
    
    # read the fixation duration
#    all_fixa, fixa_headers = load_conditions_dict(conditionfile=fixa_file)
    # open the result file to write the heater
    
    write_header(filename,headers) 
    
#    
#    
   # shuffle(all_trials) #- 
    trial_pres_num = 1 # initialize a counter (so that we can have mini-blocks of 10)
    fixa_num = 0          
    
    #trigger the scanner
    trigger_exp()
    event.waitKeys(keyList=['5'], timeStamped=True)
    #  remind the subjects that experiment starts soon.
    #ready()
    #core.wait(3)  # 2 TRs
    run_onset = win.flip() 
    
    print ('run_onset',run_onset)
    
    for trial in all_trials: 
        
       
        #''' trial is a ordered dictionary. The key is the first raw of the stimuli csv file'''
          
        # prepare fixation, clue, probe and target for dispaly
        
        fix  = prep_cont('+',fix_pos,text_h)
        probe = prep_cont(trial['probe'],probe_pos,text_h)
        target = prep_cont(trial['target'],target_pos,text_h)
        yes   = prep_cont('Y',yes_pos,yes_no_h)
        no    = prep_cont('N',no_pos,yes_no_h)



        condition = trial['StimType']

        
        
         # draw probe and filp the window
        probe.draw()

        while core.monotonicClock.getTime() < (run_onset + trial_duration*(trial-1) - (1/120.0)):
            pass       
        probe_onset = win.flip()
        
        # draw fixa between probe and target and flip the window
        fix.draw()
        timetodraw = probe_onset + probe_durat
        while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
            pass
        fix1_onset = win.flip()
        
        # draw target and flip the window           
        target.draw()
        #yes.draw()
        #no.draw()
        timetodraw = fix1_onset + fix_durat1
        while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
            pass
        event.clearEvents()
        target_onset = win.flip()

        keys = event.waitKeys(maxWait = timelimit_deci, keyList =['1','2','escape'],timeStamped = True)
        

        # If subjects do not press the key within maxwait time, RT is the timilimit and key is none and it is false
        if keys is None:
            RT = 'None'
            keypress = 'None'
            correct = 'False'
            target_offset = target_onset+ timelimit_deci

            #write_trial(filename,headers,trial) 

    # If subjects press the key, record which key is pressed, RT and whether it is right
    #
        elif type(keys) is list:
            if keys[0][0]=='escape':
                shutdown()
            
            else:
                keypress = keys[0][0]
                RT = keys[0][1] - target_onset
                correct = (keys[0][0]==trial['correct_answer']) 
                target_offset = keys[0][1] 
                trial['RT']=RT
                trial['correct'] = correct
                trial['KeyPress'] = keypress
       
        fix.draw()
        timetodraw = target_onset + target_durat
        while core.monotonicClock.getTime() < (timetodraw - (1/120.0)):
            pass
        fix2_onset = win.flip()                
                
                
        trial['trial_ID']=trial_pres_num
        trial['fixa1_onset'] = fix1_onset - run_onset
        trial['fixa1_durat']= fix_durat1
        trial['probe_onset'] = probe_onset - run_onset
        trial['probe_durat']= probe_durat
        trial['fixa2_onset'] = fix2_onset -run_onset
        trial['fixa2_durat']= fix_durat2
        trial['target_onset'] = target_onset - run_onset
        trial['target_offset'] = target_offset - run_onset
        trial['target_durat'] = target_durat
        trial['RT'] = RT
        trial['correct'] = correct
        trial['KeyPress'] = keypress
        
        trial_pres_num +=1 # the number-th presentnted trial
        write_trial(filename,headers,trial)     # calls the function that writes csv output
       


        
# -----------------------------------------------------------------------------------------------------------------------------------------------
# call the functions defined
# get the current directory
curr_dic = get_pwd()

# make a directory – data to store the generated data
makedir(data_folder)

# record subjects info and create a csv file with the info about subjects
expInfo, filename, stimuli_file,fixa_file = info_gui(expName)

# if the data does not exist, create one, otherwise,  rename one –filename-repeat-n
write_file_not_exist(filename)

# set up the window to display the instruction
win = set_up_window()

# read the instruction
# instruct()

# generate the jitter list for the fixation and probe
# know the number of trials
trials, fieldnames = load_conditions_dict(stimuli_file)
trials_num = len(trials)



ideal_trial_onset = gen_ideal_onset(num_trials)  # ideal onset list of each trial      


# sets a local clock that will be used to store timing information synced with the scanner
expClock = core.Clock()
expClock.reset()   

# run the stimuli
run_stimuli(stimuli_file,fixa_list)

# end of the experiment
end_onset = end_exp()

print ('end onset',end_onset)

    
    
# Experiment()   
