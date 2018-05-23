import subprocess # required for executing command line
import os
from shlex import split

# File path
HADOOP_BIN_PATH = '/home/hadoop/hadoop-2.6.0-cdh5.5.1/bin/hadoop'
TMP_MP3_DIR = '/home/1ronyar/melon-dataset/audio/'  # slash(/) in the last is necessary!
OUTPUT_MP3_DIR = 'marg-cb:/home/work/melon-dataset/audio'

if not os.path.exists(TMP_MP3_DIR):
    os.makedirs(TMP_MP3_DIR)

# Get a list of directories in media_files directory 
command = split(HADOOP_BIN_PATH + " fs -ls /media_files/")
result = subprocess.check_output(command)
result = result.decode("utf-8").split()
dir_all = [s for s in result if '/media_files/' in s]
total_dir = len(dir_all)
print('Found {} sub-directories in media_files directory.'.format(total_dir))

# Copy
cnt = 1
for dir in dir_all:
    dir_source = dir
    dir_target = TMP_MP3_DIR
    # copy to local tmp directory
    command = HADOOP_BIN_PATH + " fs -copyToLocal " + dir_source + " " + dir_target 
    assert(0==os.system(command)) # error if 'hadoop fs -copyToLocal' command was unsuccessful
    os.system("du -bsh " + TMP_MP3_DIR + "*")

    # move to docker volume
    command = "docker cp " + TMP_MP3_DIR + " " + OUTPUT_MP3_DIR
    assert(0==os.system(command)) # error if copying to docker volume was unsuccessful

    # remove temporary files
    command = "rm -r " + TMP_MP3_DIR + "*"
    os.system(command)

    # print progresss
    print('copy-hadoop-audio.py:{}/{} completed'.format(cnt, total_dir))
    cnt += 1





