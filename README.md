# Project 001 - Thompson's Lexical Analyzer

By Zaykha Kyaw San (zaykha@google.com)

## How to compile the program

#### Activating the setup

    $ cd ~/workspace/pr01/python001
    $ source activate.sh

## How to run tests

#### Running student-grader

    $ cd ~/workspace/pr01/python001
    $ ./../bin/student-grader ./bin/pr01
    
#### Running unit tests

    $ cd ~/workspace/pr01/python001
    $ pytest

## How to run the program
    
#### Usage 1
If an input.txt exists. This file contains the input string to be parsed. For example, "aaa".

    $ cd ~/workspace/pr01/python001
    $ cat <PATH_TO_INPUT.txt> | ./bin/pr01 <PATH_TO_NFA_BYTECODE_FILE.ns>    

#### Usage 2
If an input.txt does not exist. In this case, the input can be entered manually to STANDARD IN.
Example input "aaa".
**IMPORTANT:** Press ctrl+d to end the input. Pressing enter key will pass a newline character '\n'.

    $ cd ~/workspace/pr01/python001
    $ ./bin/pr01 <PATH_TO_NFA_BYTECODE_FILE.ns>
    aaa

## Where the code is, and how to read it

All the files are in ~/workspace/pr01/python001.








