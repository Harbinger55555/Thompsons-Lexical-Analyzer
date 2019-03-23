#!/usr/bin/env python3

import collections
import sys

Config = collections.namedtuple("Config", ("nfa_program", "input"))

Instruction = collections.namedtuple("Instruction", ("op", "X", "Y"))
MATCH = lambda: Instruction("MATCH", None, None)
CHAR = lambda X, Y: Instruction("CHAR", int(X), int(Y))
JMP = lambda X: Instruction("JMP", int(X), None)
SPLIT = lambda X, Y: Instruction("SPLIT", int(X), int(Y))


class NfaParsingException(Exception):
    """
    Raised when:
    1). Length of instruction string is equal to 1 or greater than 4.
    2). Instruction does not begin with PC.
    3). Instruction is not defined.
    4). PC not in order.
    
    Also raised for instruction specific cases when:
    5). CHAR:
        - Either X or Y cannot be casted to an integer.
        - X is greater than Y.
    6). MATCH:
        - Length does not equal 2 (Also accounts for X or Y not being None).
    7). JMP:
        - X cannot be casted to an integer.
        - Length does not equal 3 (Also accounts for no X or Y not being None).
        - JMP to an invalid PC (negative or greater than total PC).
    8). SPLIT:
        - Either X or Y cannot be casted to an integer.
        - SPLIT to an invalid PC (negative or greater than total PC).
    """
    pass


def tokenize(config):
    try:
        instructions = parse_nfa(config[0])
    except NfaParsingException as e:
        print >> sys.stderr, e
        return 1
    
    # Thread lists and their respective sets to hold PCs and prevent duplicate appends.
    cqueue, cset = [], set()
    nqueue, nset = [], set()
    
    # Variables to record matches.
    match_pc, match_tc, start_tc = -1, -1, 0
    matches = []
    matches_str = ""
    pc = 0 # Program counter, which is the instruction index.
    
    cqueue.append(pc)
    cset.add(pc)
    input_str = config[1]
    eos = len(input_str)
    
    # Eos must be included.
    # For loop is not used since it doesn't allow update of the counter
    # from inside the loop.
    tc = 0
    while tc <= eos:
        while cqueue:
            pc = cqueue.pop(0)
            inst = instructions[pc]
            opcode = inst.op
            if opcode == "CHAR":
                if tc < eos:
                    char_ascii = ord(input_str[tc])
                    if char_ascii >= inst.X and char_ascii <= inst.Y:
                        add_unique_thread(nqueue, nset, pc+1)
            elif opcode == "MATCH":
                if match_tc < tc:
                    match_pc, match_tc = pc, tc
                elif match_pc > pc:
                    match_pc, match_tc = pc, tc
            elif opcode == "JMP":
                add_unique_thread(cqueue, cset, inst.X)
            elif opcode == "SPLIT":
                add_unique_thread(cqueue, cset, inst.X)
                add_unique_thread(cqueue, cset, inst.Y)
        cqueue, nqueue = nqueue, cqueue
        cset, nset = nset, set()
        if not cqueue and match_pc != -1:
            print("{}:\"{}\"".format(str(match_pc), repr(input_str[start_tc:match_tc]).strip("'")))
            add_unique_thread(cqueue, cset, 0)
            start_tc = tc
            match_pc = -1
            tc -= 1
        tc += 1
    return 0 if match_tc == eos else 1


def parse_nfa(nfa_txt):
    # An instruction is a named tuple like Instruction(op='CHAR', a=1, b=2).
    # The PC will be the index of the returned list.
    res = []
    ordered_pc = 0
    ins_raws = nfa_txt.strip().split('\n')
    
    # Ignore empty spaces; whitespace characters will raise NfaParsingException though.
    ins_raws = [x for x in ins_raws if x]
    for ins_raw in ins_raws:
        ins = ins_raw.split(' ')
        if (len(ins) == 1 or len(ins) > 4):
            raise NfaParsingException("Wrong Instruction Length!")
        try:
            pc = int(ins[0])
            opcode = ins[1]
            if opcode == "CHAR":
                X, Y = int(ins[2]), int(ins[3])
                if X > Y:
                    raise NfaParsingException("Invalid CHAR Instruction!")
                res.append(CHAR(X, Y))
            elif opcode == "MATCH":
                if len(ins) != 2:
                    raise NfaParsingException("Invalid MATCH Instruction!")
                res.append(MATCH())
            elif opcode == "JMP":
                JMP_PC = int(ins[2])
                if len(ins) != 3 or JMP_PC < 0 or JMP_PC >= len(ins_raws):
                    raise NfaParsingException("Invalid JMP Instruction!")
                res.append(JMP(JMP_PC))
            elif opcode == "SPLIT":
                SPLIT_PC1, SPLIT_PC2 = int(ins[2]), int(ins[3])
                if SPLIT_PC1 < 0 or SPLIT_PC2 < 0 or SPLIT_PC1 >= len(ins_raws) or SPLIT_PC2 >= len(ins_raws):
                    raise NfaParsingException("Invalid SPLIT Instruction!")
                res.append(SPLIT(SPLIT_PC1, SPLIT_PC2))
            else:
                raise NfaParsingException("Undefined Instruction!")
            # Check if PCs are in order.
            if pc != ordered_pc:
                raise NfaParsingException("PCs are not in order!");
            ordered_pc += 1
        except (ValueError, IndexError):
            raise NfaParsingException("Invalid Instruction!");
    return res
    

def add_unique_thread(tlist, tset, tpc):
    if tpc not in tset:
        tlist.append(tpc)
        tset.add(tpc)
