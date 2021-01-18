# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex
import ply.yacc as yacc

# List of token names.   This is always required


tokens = [
    'INT',
    'FLOAT',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'ID',
    'STRING',
    'EQUALS',
    'INCREMENTATION',
    'DECREMENTATION',
    'SEMICOLON',
    'SUP',
    'INF',
    'EQUALSCOMP',
    'INFEQUALS',
    'SUPEQUALS',

]

reserved = {
    'kteb': 'KTEB',  # print
    'wla': 'WLA',  # else
    'ma7ed': 'MA7ED',  # while
    'khate2': 'KHATE2',  # false
    'ila': 'ILA',  # if
    'wa': 'WA',  # and
    'aw': 'AW',  # or
    's7i7': 'S7I7',  # true
    'khrej': 'KHREJ',  # break
    'naw3': 'NAW3',  # class
    'kmel': 'KMEL',  # continue
    '3aref': '3AREF',  # def
    'wlaila': 'WLAILA',  # elif
    'masd9ch': 'MASD9CH',  # except
    'akhiran': 'AKHIRAN',  # finally
    'lkola': 'LKOLA',  # for
    '3amm': '3AMM',  # global
    'huwa': 'HUWA',  # is
    'Walo': 'WALO',  # None
    'machi': 'machi',  # not
    'douz': 'DOUZ',  # pass
    'tele3': 'TELE3',  # raise
    'red': 'RED',  # return
    'jereb': 'JEREB',  # try
    'qra': 'QRA',  # input

    'rje3': 'RJE3',  # yield
    'men': 'MEN',  # from
    'tsna': 'TSNA',  # await
    'mamtzamench': 'MAMTZAMENCH',  # async
    'ftared': 'FTARED',  # assert
    'b7al': 'B7AL',  # as
    'mse7': 'MSE7',  # del
    'jib': 'JIB',  # import
    'fi': 'FI',  # in
    'lambda': 'LAMBDA',  # lambda
    'machima7ali': 'MACHIMA7ALI',  # nonlocal
    'm3a': 'M3A',  # with

}

tokens = tokens + list(reserved.values())

# Regular expression rules for simple tokens
t_EQUALSCOMP = r'\=\='
t_SUP = r'\>'
t_INF = r'\<'
t_INFEQUALS = r'\<\='
t_SUPEQUALS = r'\>\='
t_INCREMENTATION = r'\+\+'
t_DECREMENTATION = r'--'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'\='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'

# literals = ['{', '}', '==']


def t_COMMENT(t):
    r'\#.*'

    # A regular expression rule with some action code


def t_STRING(t):
    # [^"] : means any character except ", this way "hello" + "there" wont be considered a "String" but "string" + "string"
    r'("[^"]*")|(\'[^\']\')'
    if t.value[0] == '"':
        t.value = t.value[1:-1]
    elif t.value[0] == "'":
        t.value = t.value[1:-1]
    return t


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_S7I7(t):
    r's7i7'
    t.value = True
    return t


def t_KHATE2(t):
    r'khate2'
    t.value = False
    return t


def t_WALO(t):
    r'walo'
    t.value = None
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

    # Define a rule so we can track line numbers


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


    # A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
# Compute column.
#     input is the input text string
#     token is a token instance
# def find_column(input, token):
#     line_start = input.rfind('\n', 0, token.lexpos) + 1
#     return (token.lexpos - line_start) + 1

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'WA', 'AW'),
    ('nonassoc', 'LPAREN', 'RPAREN'),
    ('nonassoc', 'SUP', 'INF', 'SUPEQUALS', 'INFEQUALS', 'EQUALSCOMP'),

)


def p_darija(p):
    '''
    darija : var_assign
           | printing
           | incrementation
           | decrementation
           | expression
           | if
           | while
           | empty
    '''
    run(p[1])


def p_incrementation(p):
    '''
    incrementation : ID INCREMENTATION

    '''
    p[0] = ('++', p[1])


def p_decrementation(p):
    '''
    decrementation :  ID DECREMENTATION
    '''
    p[0] = ('--', p[1])


def p_var_assign(p):
    '''
    var_assign : ID EQUALS expression

    '''
    p[0] = ('=', p[1], p[3])


def p_if(p):
    '''
    if : ILA LPAREN condition RPAREN LBRACKET block RBRACKET 
        | ILA LPAREN condition RPAREN LBRACKET block RBRACKET WLA LBRACKET block RBRACKET

    '''
    if len(p) == 8:
        p[0] = (p[1], p[3], p[6])
    else:
        p[0] = (p[1], p[3], p[6], p[10])


def p_while(p):
    '''
    while : MA7ED LPAREN condition RPAREN LBRACKET block RBRACKET

    '''
    p[0] = (p[1], p[3], p[6])


def p_block(p):  # block to be executed when condition is satisfied,
    # didnt do "darija" function because darija initiates run function, thus it will execute even if condition is not satisfied
    '''
    block : var_assign
           | printing
           | incrementation
           | decrementation
           | expression
           | if
           | while
           | empty
    '''
    p[0] = p[1]


def p_condition_big(p):
    '''
    condition : LPAREN condition RPAREN AW LPAREN condition RPAREN
              | LPAREN condition RPAREN WA LPAREN condition RPAREN

    '''
    p[0] = (p[4], p[2], p[6])


def p_condition_medium1(p):
    '''
    condition : condition WA LPAREN condition RPAREN
              | condition AW LPAREN condition RPAREN

    '''
    p[0] = (p[2], p[1], p[4])


def p_condition_medium2(p):
    '''
    condition : LPAREN condition RPAREN WA condition
              | LPAREN condition RPAREN AW condition

    '''
    p[0] = (p[4], p[2], p[5])


def p_condition(p):
    '''
    condition :  condition WA condition
              |  condition AW condition

    '''
    p[0] = (p[2], p[1], p[3])


def p_condition_comp(p):
    '''
    condition : expression SUP expression
              | expression INF expression
              | expression EQUALSCOMP expression 
              | expression SUPEQUALS expression
              | expression INFEQUALS expression
    '''
    p[0] = (p[2], p[1], p[3])


def p_condition_exp(p):
    '''
    condition : expression
    '''
    p[0] = p[1]


def p_expression(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | LPAREN expression RPAREN
               | MINUS expression
               | PLUS expression
    '''
    if p[1] == '+':
        p[0] = p[2]
    elif p[1] == '(':
        p[0] = p[2]
    elif p[1] == '-':
        p[0] = ('neg', p[2])
    else:
        p[0] = (p[2], p[1], p[3])


def p_expression_id(p):
    '''
    expression : ID
    '''
    p[0] = ('id', p[1])


def p_expression_terminals(p):
    '''
    expression : INT
               | FLOAT
               | STRING
               | KHATE2
               | S7I7
               | WALO
    '''
    p[0] = p[1]


def p_printing(p):
    '''
    printing : KTEB LPAREN expression RPAREN
            | KTEB LPAREN incrementation RPAREN
            | KTEB LPAREN decrementation RPAREN
            | KTEB LPAREN condition RPAREN
    '''
    p[0] = (p[1], p[3])


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def p_error(p):
    print("Syntax error at ", p.value)


ids = {}


def run(p):
    global ids
    if type(p) == tuple:
        if p[0] == '+':
            try:
                return run(p[1]) + run(p[2])
            except TypeError:
                print("Action impossible")
        elif p[0] == '-':
            try:
                return run(p[1]) - run(p[2])
            except TypeError:
                print("Action impossible")
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '++':
            ids[p[1]] = ids[p[1]] + 1
            return ids[p[1]]
        elif p[0] == '--':
            ids[p[1]] = ids[p[1]] - 1
            return ids[p[1]]
        elif p[0] == 'neg':
            return -run(p[1])
        elif p[0] == '=':
            ids[p[1]] = run(p[2])
        elif p[0] == 'id':
            return ids[p[1]]
        elif p[0] == 'kteb':
            print(run(p[1]))
        elif p[0] == 'wa':
            return run(p[1]) and run(p[2])
        elif p[0] == 'aw':
            return run(p[1]) or run(p[2])
        elif p[0] == '==':
            return run(p[1]) == run(p[2])
        elif p[0] == '>=':
            return run(p[1]) >= run(p[2])
        elif p[0] == '<=':
            return run(p[1]) <= run(p[2])
        elif p[0] == '>':
            return run(p[1]) > run(p[2])
        elif p[0] == '<':
            return run(p[1]) < run(p[2])
        elif p[0] == "ila":
            if run(p[1]):
                run(p[2])
            else:
                if len(p) > 3:
                    run(p[3])

        elif p[0] == "ma7ed":
            while run(p[1]):
                run(p[2])
    else:
        return p


parser = yacc.yacc()

while True:
    try:
        i = input('>> ')

    except EOFError:
        break
    parser.parse(i)
