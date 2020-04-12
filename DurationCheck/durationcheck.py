from pathlib import Path
import argparse
import subprocess32 as subprocess
import os
import sys

def getDuration(filename):

    command = [
        'ffprobe',
        '-v',
        'error',
        '-show_entries',
        'format=duration',
        '-of',
        'default=noprint_wrappers=1:nokey=1',
        filename
      ]

    try:
        #output = check_output( command, stderr=STDOUT ).decode()
        filename =str(filename)
        #print(filename)
        output = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

        #output = subprocess.check_output(output).decode()
    except subprocess.CalledProcessError as e:
        #output = e.output.decode()
        output = float(result.stdout)
        
        
    if output.stdout.strip("\n")=="N/A":
        return '0.0'
    else:
        return output.stdout.strip("\n")


def folderDuration(folderPath):

    duration =0.0

    for path in Path(folderPath).iterdir():
        info = path.stat()
        if os.path.isdir(str(path)):
            curr_scope = float(folderDuration(path)) 
            duration += curr_scope
            print("{}/ --> {}".format( path, curr_scope) )
        elif str(path).endswith('.mp4') or str(path).endswith('.avi'):
            curr_scope = float(getDuration(path)) 
            duration += curr_scope
            print("{} --> {}".format( path, curr_scope) )
        
    return duration


if __name__=="__main__":
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--path", required=True, help=" \"path\" to target folder")
    args = vars(ap.parse_args())
    
    FOLDER_PATH = str(args["path"])
    
    print("\nScanning Folder :\n{} ... \n".format(FOLDER_PATH))
    
    if not os.path.isdir(FOLDER_PATH):
        print("** Please enter a valid Folder Path **")
        exit()
        
    elif os.path.exists(os.path.dirname(FOLDER_PATH))==False:
        print("** This folder path does not exist **")
        exit()
    
    TOTAL_MIN=0
    TOTAL_SEC=0
    
    duration = folderDuration(FOLDER_PATH)
    print(duration)
    TOTAL_SEC += int(duration%60)
    TOTAL_MIN += int(duration/60) + int(TOTAL_SEC/60)
    TOTAL_SEC = int(TOTAL_SEC%60)

    print("Total Duration: {}hr {}min {}secs ".format(TOTAL_MIN/60, TOTAL_MIN%60, TOTAL_SEC))
