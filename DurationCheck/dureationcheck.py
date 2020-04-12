from pathlib import Path
#from subprocess import  check_output, CalledProcessError, STDOUT
import subprocess32 as subprocess
import os

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
    		duration += float(folderDuration(path))
        elif str(path).endswith('.mp4') or str(path).endswith('.avi'):
            print(str(path))
            duration += float(getDuration(path))
            
    return duration


if __name__=="__main__":

    total_hr=0
    total_min=0
    total_sec=0
    
    folderPath = "/media/lupus/P3/Courses/DevOps/[Tutorialsplanet.NET] Udemy - Kubernetes from A to Z/"
    #folderPath = "/media/lupus/P4/perse/Learn How To Code Google's Go (golang) Programming Language/"
    #folderPath = "/media/lupus/P4/perse/Practical Ethical Hacking - The Complete Course/"
    #folderPath = "/media/lupus/P3/temp/Graph Databases 101 for Data Scientists and Analysts/"
    #folderPath = "/media/lupus/P3/Courses/LANGUAGE/Bash Shell Scripting Tutorial for Beginners/2. Bash Shell Scripting Tutorial/"
    #folderPath = "/media/lupus/P3/Courses/HACKING N PENTEST/Bug Bounty Hunting - Offensive Approach to Hunt Bugs/"
    #folderPath ='/media/lupus/P4/perse/GATE/TOC'
    #folderPath ='/media/lupus/P4/perse/GATE/Computer Networks'
    #folderPath ='/media/lupus/P4/perse/GATE/OS'
    #folderPath ='/media/lupus/P4/perse/GATE/c-C++'

    #folderPath = re.escape(folderPath)

    '''
    for path in Path(folderPath).iterdir():
        info = path.stat()
        #print(info.st_size/1025)
        #fn = '/app/648c89e8-d31f-4164-a1af-034g0191348b.mp4'
        if os.path.isdir(path):
    		print(path)
        duration = float(getDuration(path).strip('\n'))
        print(duration)
        total_sec += int(duration%60)
        total_min += int(duration/60) + int(total_sec/60)
        total_sec = int(total_sec%60)
        
    '''
    
    duration = folderDuration(folderPath)
    print(duration)
    total_sec += int(duration%60)
    total_min += int(duration/60) + int(total_sec/60)
    total_sec = int(total_sec%60)
    


    print("Total Duration: {}hr {}min {}secs ".format(total_min/60, total_min%60, total_sec))
