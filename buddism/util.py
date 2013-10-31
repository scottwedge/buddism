import os
from subprocess import Popen, PIPE, STDOUT

def get_file_size(file_path):
    return os.path.getsize(file_path)

def get_mp3_duration(file_path):
    cmd = "ffmpeg -i %s 2>&1 | grep Duration | awk '{print $2}' | tr -d ,"%(file_path)
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    a = p.stdout.read()
    args = a.strip('\n ').split(':')
    ret = 0.0
    pre = 0.0
    for item in args:
        ret = pre + float(item)  
        pre = ret * 60
    return ret
