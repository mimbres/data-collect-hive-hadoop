import subprocess # required for executing command line
import os
from shlex import split

# File path
HIVE_BIN_PATH = '/home/hadoop/hive/bin/hive'
#HADOOP_BIN_PATH = '/home/hadoop/hadoop-2.6.0-cdh5.5.1/bin/hadoop'
OUTPUT_CSV_DIR = '/home/1ronyar/melon-dataset/hive-tables/'
OUTPUT_MP3_DIR = '/home/1ronyar/melon-dataset/audio/'

if not os.path.exists(OUTPUT_CSV_DIR):
    os.makedirs(OUTPUT_CSV_DIR)
if not os.path.exists(OUTPUT_MP3_DIR):
    os.makedirs(OUTPUT_MP3_DIR)

# Get a list of table names
command = split(HIVE_BIN_PATH + " -e 'show tables'")
result = subprocess.check_output(command)
table_names = result.decode("utf-8").split()
print('Found {} tables from hive.'.format(len(table_names)))

# Get tables as .csv
for tname in table_names:
    os.system(HIVE_BIN_PATH + " -e 'select * from " + tname + "' | sed 's/[\t]/,/g' > " + OUTPUT_CSV_DIR + tname + ".csv")








