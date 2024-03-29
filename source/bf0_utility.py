import pandas as pd
import time
import os



# Category,BoxNo,SideA,SideB,ActiveSide,TimeNextREV,MistakeNo

#   -1: new words
#    0: to be reviewed now
#    1: to be reviewed after a day
#    3: to be reviewed after 3 days
#    7: to be reviewed after a week
#   15: to be reviewed after 2 weeks
#   60: to be reviewed after 2 months
#  120: to be reviewed after 4 months
#  999: output

def mainAddress():
    # get the current working directory
    dir_path = os.getcwd()
    #print("The current directory is:", dir_path)
    return dir_path


def mainDataCheck(df):
    # clean data 
    # check for 1-duplicates 2-zeros 3-... 
    df = df
    return df


def mainMapReduce():
    dir_path = mainAddress()
    file_name = dir_path + '/data/data.csv'
    # read file - file_name = "data.csv"   
    df = pd.read_csv(file_name)
    #clean the data
    df = mainDataCheck(df)

    tdf = df[(df['TimeNextREV'] < int(time.time() / 60.))]
    # read categories
    study_options = tdf['Category'].unique().tolist()
    # call gui: first page containing all options to study 
    # ( course_A, ..., course_Z, French, Skill_A, ..., Skill_Z, Startup, Book, favourite_dialogues, work_place_dialogues, pickup_dialogues, poems)
    return study_options, df


def mainLietner(row, answer):
    box_id = [-1, 0, 1, 3, 7, 15, 30, 60, 120]
    # update box number to zero if answer was negative
    if answer == 0 :
        row['BoxNo'] = 0
        row['MistakeNo'] += 1
        row["TimeNextREV"] = int(time.time()/60.) + 360
    else:
        card_box_id = (row['BoxNo'].values)[0]
        if card_box_id < 120:
            # update box,  number if answer was positive
            row['BoxNo'] = box_id[box_id.index(card_box_id)+1]
            row["TimeNextREV"] = int(time.time()/60.) + (1440 * int((row['BoxNo'].values)[0])) + 360

        else: # == 120
            # if first side is learnt 
            if (row['ActiveSide'].values)[0] == 0 : 
                row['ActiveSide'] = 1
                row["TimeNextREV"] = int(time.time()/60.) + 360 

            if (row['ActiveSide'].values)[0] == 1 : 
                row["TimeNextREV"] = int(time.time()/60.) + 262800 
                row['ActiveSide'] == 0
    return row
                
def mainDataWriter(df):
    dir_path = mainAddress()
    df.to_csv( dir_path + "/data/data.csv", index=False)