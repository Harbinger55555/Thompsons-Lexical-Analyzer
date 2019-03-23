#!/usr/bin/env python3

from pytest import raises
from tokenizer import Config
from tokenizer import Instruction
from tokenizer import NfaParsingException
from tokenizer import parse_nfa
from tokenizer import tokenize

def test_parse_nfa_valid():
    # Test successful parsing of all instruction.
    nfa_all_ins = '0 CHAR 97 98\n1 MATCH\n2 JMP 1\n3 SPLIT 0 1'
    parsed_nfa = [
        Instruction('CHAR', 97, 98),
        Instruction('MATCH', None, None), 
        Instruction('JMP', 1, None), 
        Instruction('SPLIT', 0, 1), 
    ]
    assert parse_nfa(nfa_all_ins) == parsed_nfa
    
    # Test parsing of empty input.
    assert parse_nfa('') == []

        
def test_parse_nfa_invalid():
    # Test parsing of instruction with length equal to 1.
    with raises(NfaParsingException):
        parse_nfa('5')
    
    # Test parsing of instruction with length greater than 4.
    with raises(NfaParsingException):
        parse_nfa('0 CHAR 1 1 1')
        
    # Test parsing of instruction that does not begin with pc.
    with raises(NfaParsingException):
        parse_nfa('MATCH 0')
    
    # Test parsing of undefined instructions.
    with raises(NfaParsingException):
        parse_nfa('0 Unknown 97 98')
    
    # Test parsing of unordered PC.
    with raises(NfaParsingException):
        parse_nfa('0 CHAR 97 97\n2 MATCH\n1 MATCH')


def test_parse_char_invalid():
    # Non-integer X or Y.
    with raises(NfaParsingException):
        parse_nfa('0 CHAR a b')
        
    # X is greater than Y.
    with raises(NfaParsingException):
        parse_nfa('0 CHAR 98 97')


def test_parse_match_invalid():
    # Length not equal 2.
    with raises(NfaParsingException):
        parse_nfa('0 MATCH 3')


def test_parse_jmp_invalid():        
    # Non-integer X.
    with raises(NfaParsingException):
        parse_nfa('0 JMP a')
        
    # Length not equal 3.
    with raises(NfaParsingException):
        parse_nfa('0 JMP\n1 MATCH')
    
    with raises(NfaParsingException):
        parse_nfa('0 JMP 1 0\n1 MATCH')
    
    # Invalid PC.
    with raises(NfaParsingException):
        parse_nfa('0 JMP 1')


def test_parse_split_invalid():
    # Non-integer X or Y.
    with raises(NfaParsingException):
        parse_nfa('0 SPLIT a b')
    
    # Invalid PC.
    with raises(NfaParsingException):
        parse_nfa('0 SPLIT 1 2')
    
    
def test_tokenizer():
    nfa_match_a = '''0 CHAR 97 97\n1 MATCH'''
    assert tokenize(Config(nfa_match_a, "a")) == 0
    assert tokenize(Config(nfa_match_a, "b")) == 1
