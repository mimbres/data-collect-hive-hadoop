import subprocess # required for executing command line
import os
from shlex import split

# File path
HIVE_BIN_PATH = '/home/hadoop/hive/bin/hive'
TMP_CSV_DIR = '/home/1ronyar/melon-dataset/hive-tables/'
OUTPUT_CSV_DIR = 'marg-cb:/home/work/melon-dataset/hive-tables'


if not os.path.exists(TMP_CSV_DIR):
    os.makedirs(TMP_CSV_DIR)

# Get a list of table names
command = split(HIVE_BIN_PATH + " -e 'show tables'")
result = subprocess.check_output(command)
table_names = result.decode("utf-8").split()
print('Found {} tables from hive.'.format(len(table_names)))

# Select tables!
table_names = [table_names[5], table_names[6], table_names[7], table_names[14]]
# Get tables as .csv
for tname in table_names:
    os.system(HIVE_BIN_PATH + " -e 'select * from " + tname + "' | sed 's/[\t]/,/g' > " + TMP_CSV_DIR + tname + ".csv")

# Move files to docker volume
command = "docker cp " + TMP_CSV_DIR + " " + OUTPUT_CSV_DIR
assert(0==os.system(command)) # error if copying to docker volume was unsuccessful 

# remove temporary files
command = "rm -r " + TMP_CSV_DIR + "*"
os.system(command)








