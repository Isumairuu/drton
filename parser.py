import sys
from lexer import *
import ply.yacc as yacc
from functions import *

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'WA', 'AW'),
    ('nonassoc', '(', ')'),
    ('nonassoc', 'SUP', 'INF', 'SUPEQUALS', 'INFEQUALS', 'EQUALSCOMP'),

)


def p_program(p):
    '''
    program : instruction_list
    '''
    p = ('prog', p[1])
    run(p)


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
               | ID EQUALS input
    '''
    p[0] = ('=', p[1], p[3])


def p_var_assign_global(p):
    '''
    var_assign : MOJOD var_assign
    '''
    p[0] = ('=', p[1], p[2])


def p_arrayelt_assign(p):
    '''
    arrayelt_assign : arrayelt EQUALS expression
                    | arrayslice EQUALS expression
    '''
    p[0] = ('=', p[1], p[3])


def p_if(p):
    '''
    if : ILA '(' condition ')' '{' instruction_list '}'
        | ILA '(' condition ')' '{' instruction_list '}' WLA '{' instruction_list '}'

    '''
    if len(p) == 8:
        p[0] = (p[1], p[3], p[6])
    else:
        p[0] = (p[1], p[3], p[6], p[10])


def p_for(p):
    '''
    for : LKOLA '(' var_assign  ';' condition ';' incrementation  ')' '{' instruction_list '}'
        | LKOLA '(' var_assign  ';' condition ';' decrementation  ')' '{' instruction_list '}'
        | LKOLA '(' expression ';' condition ';' incrementation  ')' '{' instruction_list '}'
        | LKOLA '(' expression ';' condition ';' decrementation  ')' '{' instruction_list '}'
    '''
    p[0] = (p[1], p[3], p[5], p[7], p[10])


def p_while(p):
    '''
    while : MA7ED '(' condition ')' '{' instruction_list '}'

    '''
    p[0] = (p[1], p[3], p[6])


def p_doWhile(p):
    '''
    doWhile :  DIR '{' instruction_list '}' MA7ED '(' condition ')'
    '''
    p[0] = (p[1], p[3], p[7])


def p_instruction(p):
    '''
    instruction : var_assign
           | arrayelt_assign
           | printing
           | incrementation
           | decrementation
           | expression
           | try
           | if
           | for
           | KHREJ
           | KMEL
           | while
           | doWhile
           | input
           | empty
           | func
           | return
    '''
    p[0] = p[1]


def p_instruction_list(p):
    '''
        instruction_list : instruction
                        |  instruction_list instruction
    '''
    # when there is more than one instruction in an instruction list, each time we enter here, an instruction is reduced,
    #  and added in a table, we see if table is created, if not then it is the first entry,
    #  we creat table that will contain the instruction we will reduce.
    #  and so on until all instruction are inside table and then when executing we will run each element of that table

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if(not isinstance(p[1], list)):
            p[1] = [p[2]]
        else:
            p[1].append(p[2])
        p[0] = p[1]


def p_condition_big(p):
    '''
    condition : '(' condition ')' AW '(' condition ')'
              | '(' condition ')' WA '(' condition ')'

    '''
    p[0] = (p[4], p[2], p[6])


def p_condition_medium1(p):
    '''
    condition : condition WA '(' condition ')'
              | condition AW '(' condition ')'

    '''
    p[0] = (p[2], p[1], p[4])


def p_condition_medium2(p):
    '''
    condition : '(' condition ')' WA condition
              | '(' condition ')' AW condition
              |  condition WA condition
              |  condition AW condition

    '''
    if(len(p) == 6):
        p[0] = (p[4], p[2], p[5])
    else:
        p[0] = (p[2], p[1], p[3])


def p_condition(p):
    '''
    condition : L3AKSS '(' condition ')'
    '''
    p[0] = (p[1], p[3])


def p_condition_comp(p):
    '''
    condition : expression SUP expression
              | expression INF expression
              | expression EQUALSCOMP expression
              | expression SUPEQUALS expression
              | expression INFEQUALS expression
              | expression DIFFERENT expression
    '''
    p[0] = ('comp', p[2], p[1], p[3])


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
               | expression MODULO expression
               | expression POWER expression
               | '(' expression ')'
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
               | array
               | arrayelt
               | arrayslice
               | appel_func
               | arrfn
               | len
    '''
    p[0] = p[1]


def p_input(p):
    '''
    input : QRA '(' expression ')'
          | QRA '(' ')'
    '''
    p[0] = (p[1], p[3])


def p_try(p):
    '''
    try :  JEREB '{' instruction_list '}' MASD9CH '{' instruction_list '}'
        |  JEREB '{' instruction_list '}' MASD9CH '{' instruction_list '}' AKHIRAN '{' instruction_list '}'
    '''
    if len(p) == 9:
        p[0] = (p[1], p[3], p[5], p[7])
    else:
        p[0] = (p[1], p[3], p[5], p[7], p[9], p[11])


########################### arrays ############################


def p_arraylist_1(p):
    '''
    arraylist :  expression
    '''
    p[0] = [p[1]]


def p_arraylist_2(p):
    '''
    arraylist : arraylist ',' expression
    '''
    p[0] = p[1]
    p[0].append(p[3])


def p_array(p):
    '''
    array : '[' arraylist ']'
    '''
    p[0] = p[2]


def p_array_empty(p):
    '''
    array : '[' ']'
    '''
    p[0] = []


def p_arrayelt(p):
    '''
    arrayelt : ID dimensions
    '''
    p[0] = ('arrelt', p[1], p[2])


def p_dimensions(p):
    '''
    dimensions : '[' expression ']'
    '''
    p[0] = [p[2]]


def p_demensions(p):
    '''
    dimensions : dimensions '[' expression ']'
    '''
    p[1].append(p[3])
    p[0] = p[1]


def p_arrayslice(p):
    '''
    arrayslice : ID '[' expression ':' expression ']'
               | ID '[' ':' expression ']'
               | ID '[' expression ':' ']'
               | ID '[' ':' ']'
    '''

    if len(p) == 7:
        p[0] = ('slice', p[1], p[3], p[4], p[5])
    elif len(p) == 5:
        p[0] = ('slice', p[1])
    elif p[3] == ':':
        # accessing [:expr]
        # I included the ':' just to differentiate later
        p[0] = ('slice', p[1], p[3], p[4])
    else:
        # accessing [expr:]
        p[0] = ('slice', p[1], p[3])


def p_arrfn(p):
    '''
    arrfn : ID '.' ZID '(' expression ')'
          | ID '.' KBER '(' array ')'
          | ID '.' KHWI '(' ')'
          | ID '.' DKHEL '(' expression ',' expression ')' 
          | ID '.' N9S '(' expression ')'
          | ID '.' N9S '(' ')'
    '''
    if len(p) == 7:
        p[0] = ('arrfn', p[1], p[3], p[5])
    elif len(p) == 6:
        p[0] = ('arrfn', p[1], p[3])
    elif len(p) == 9:
        p[0] = ('arrfn', p[1], p[3], p[5], p[7])

######### functions #########


def p_argument_list(p):
    '''
        argument_list : expression
                      | argument_list ',' expression
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if(not isinstance(p[1], list)):
            p[1] = [p[3]]
        else:
            p[1].append(p[3])
        p[0] = p[1]


def p_parameter(p):
    '''
    parameter : ID
    '''
    p[0] = p[1]


def p_parameter_list(p):
    '''
        parameter_list : parameter
                       | parameter_list ',' parameter
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if(not isinstance(p[1], list)):
            p[1] = [p[3]]
        else:
            p[1].append(p[3])
        p[0] = p[1]


def p_func(p):
    '''
    func : TA3RIF ID '(' parameter_list ')' '{' instruction_list '}'
         | TA3RIF ID '(' ')' '{' instruction_list '}'
    '''
    if(len(p) == 8):
        p[0] = ('ta3rif', p[2], p[6])
    else:
        p[0] = ('ta3rif', p[2], p[4], p[7])


def p_appel_func(p):
    '''
    appel_func : ID '(' argument_list ')'
               | ID '('  ')'

    '''
    if(len(p) == 4):
        p[0] = ('appel_func', p[1])
    elif(len(p) == 5):
        p[0] = ('appel_func', p[1], p[3])


def p_return(p):
    '''
    return : RED '(' expression ')'
    '''
    p[0] = ('red', p[3])

#################################


def p_printing(p):
    '''
    printing : KTEB '(' condition ')'
            | KTEB '(' incrementation ')'
            | KTEB '(' decrementation ')'
            | KTEB '(' condition ',' condition ')'
    '''
    if len(p) == 5:
        p[0] = (p[1], p[3])
    else:
        p[0] = (p[1], p[3], p[5])


def p_len(p):
    '''
    len : TOL '(' expression ')'
    '''
    p[0] = (p[1], p[3])


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def p_error(p):
    global foundError
    if(not(foundError)):
        try:
            print("Ghalat dyal syntax fster: ", p.lineno)
            print("9bel men:", p.value)
        except AttributeError:
            # p.lineno and p.value might generate error if at the end of block } is missing
            print("Ghalat dyal syntax, t2eked bila ga3 l2a9wass o ma3qofat msdodin")
        finally:
            foundError = True
    exitDarija()


parser = yacc.yacc()


if len(sys.argv) > 1:
    f = open(sys.argv[1])
    parser.parse(f.read())
else:
    while True:
        try:
            i = input('>> ')

            parser.parse(i)
        except EOFError:
            break
