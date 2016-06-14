# switchboard_parse
NXT Switchboard xml parsing script

----------------------------------
Description:

file_list.txt is the file name list for naming usage
It is obtained by running filelist.py script.

filelist.py read through "terminal" diretory to retrieve
sw2008 format file names since "terminal" directory 
contains most dialogue scripts.

parse_all.py
This is the main script to retrieve plain text information
from corresponding folders
One dialogue per running.
This script will take in one argument, which is the unique 
index of the dialogue file (e.g. sw2005)

parse_all.sh
This is the bash script to run parse_all.py through all 
dialogue files, and list result in plain text with the index
of the dialogue(e.g. sw2012)

----------------------------------
How to run:

First, put the file_list.txt parse_all.py and parse_all.sh into
.../xml/ directory

Second, 
mkdir /result 
in the .../xml/ directory

Finally, run

./parsing_all.sh file_list.txt

here file_list will guide paring_all to create corresponding 
result files.

----------------------------------

