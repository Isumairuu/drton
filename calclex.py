# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
tokens = [
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'ID',
#    'IF',
#    'THEN',
#    'ELSE',
#    'WHILE',
#    'FOR',
#    'PRINT',
#    'KTEB',
   'QRA'
]

reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'for' : 'FOR',
   'print' : 'PRINT',
   'كتب' : 'KTEB',
   'input' : 'INPUT'
}

tokens = tokens + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_FOR = r'for'
t_IF = r'if'
t_THEN = r'then'
t_PRINT = r'print'
t_WHILE = r'while'
t_ELSE = r'else'
t_KTEB = r'كتب'
t_QRA = r'اقرأ'
t_INPUT = r'input'

def t_COMMENT(t):
    r'\#.*'
    # pass
    # No return value. Token discarded

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
3 + 4 * 10
  + -20 *2
  abc
  if a then
  اقرأ a then b
  #hjh
  input abc
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok.type, tok.value, tok.lineno, tok.lexpos)
    #tok.type = token name from tokens list
    #tok.value = actual value
    #tok.lineno = line number
    #tok.lexpos = token position in line