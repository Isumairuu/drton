# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import sys
import ply.lex as lex
import ply.yacc as yacc

# List of token names.   This is always required


tokens = [
    'INT', 'FLOAT',  # Numbers
     'MINUS', 'TIMES', 'DIVIDE',  # operations
     # Parentheses and brackets and braces
    'ID',
    'STRING',
    'EQUALS', #delimiters
    'INCREMENTATION', 'DECREMENTATION',
    'SUP', 'INF', 'EQUALSCOMP', 'INFEQUALS', 'SUPEQUALS', 'DIFFERENT',  # comparison ops

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
    'Walo': 'WALO',  # None
    'qra': 'QRA',  # input
    'kmel': 'KMEL',  # continue
    'dir': 'DIR',  # do
    'jereb': 'JEREB',  # try
    'masd9ch': 'MASD9CH',  # except
    'akhiran': 'AKHIRAN',  # finally
    'lkola': 'LKOLA',  # for
    # arrays TODO
    '3amm': '3AMM',  # global TODO
    'douz': 'DOUZ',  # pass TODO
    '3akss': '3AKSS',  # TODO 3akss(condition)
    '3aref': '3AREF',  # def TODO
    'red': 'RED',  # return TODO

    'tele3': 'TELE3',  # raise TODO
    'naw3': 'NAW3',  # class TODO

    # 'huwa': 'HUWA',  # is
    # 'rje3': 'RJE3',  # yield
    # 'men': 'MEN',  # from
    # 'tsna': 'TSNA',  # await
    # 'mamtzamench': 'MAMTZAMENCH',  # async
    # 'ftared': 'FTARED',  # assert
    # 'b7al': 'B7AL',  # as
    # 'mse7': 'MSE7',  # del
    # 'jib': 'JIB',  # import
    # 'fi': 'FI',  # in
    # 'lambda': 'LAMBDA',  # lambda
    # 'machima7ali': 'MACHIMA7ALI',  # nonlocal
    # 'm3a': 'M3A',  # with

}

tokens = tokens + list(reserved.values())

# Regular expression rules for simple tokens
t_EQUALSCOMP = r'\=\='
t_DIFFERENT = r'\!\='
t_SUP = r'\>'
t_INF = r'\<'
t_INFEQUALS = r'\<\='
t_SUPEQUALS = r'\>\='
t_INCREMENTATION = r'\+\+'
t_DECREMENTATION = r'--'
# t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'\='
# t_LPAREN = r'\('
# t_RPAREN = r'\)'
# t_SEMICOLON = r';'
# t_LCBRACE = r'\{'
# t_RCBRACE = r'\}'
# t_COMMA = r','
# t_LBRACKET = r'\['
# t_RBRACKET = r'\]'
literals = [',','[',']','{','}','(',')','+',';']

def t_COMMENT(t):
    r'\#.*'

    # A regular expression rule with some action code


def t_STRING(t):
    # [^"] : means any character except ", this way "hello" + "there" wont be considered a "String" but "string" + "string"
    r'("[^"]*")|(\'[^\']*\')'
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
    ('left', '+', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'WA', 'AW'),
    ('nonassoc', '(', ')'),
    ('nonassoc', 'SUP', 'INF', 'SUPEQUALS', 'INFEQUALS', 'EQUALSCOMP'),

)


# def p_darija(p):
#     '''
#     darija : var_assign
#            | printing
#            | incrementation
#            | decrementation
#            | expression
#            | if
#            | for
#            | input
#            | while
#            | doWhile
#            | try
#            | empty
#     '''
#     run(p[1])


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
              | expression DIFFERENT expression
    '''
    p[0] = (p[2], p[1], p[3])


def p_condition_exp(p):
    '''
    condition : expression
    '''
    p[0] = p[1]


def p_expression(p):
    '''
    expression : expression '+' expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
               | '(' expression ')'
               | MINUS expression
               | '+' expression
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


def p_expression_terminals(p):
    '''
    expression : INT
               | FLOAT
               | STRING
               | KHATE2
               | S7I7
               | WALO
               | array
    '''
    p[0] = p[1]
# ARRAYS :)
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

def p_printing(p):
    '''
    printing : KTEB '(' condition ')'
            | KTEB '(' incrementation ')'
            | KTEB '(' decrementation ')'
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
didBreak = False
didContinue = False


def run(p):
    global ids, didBreak, didContinue
    if type(p) == tuple:
        if(p[0] == 'prog'):
            for i in p[1]:
                run(i)
        try:
            if p[0] == '+':
                try:
                    return run(p[1]) + run(p[2])
                except TypeError:
                    # number and string concatenation
                    return str(run(p[1])) + str(run(p[2]))
            elif p[0] == '-':
                return run(p[1]) - run(p[2])
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
        except TypeError:
            print("     action impo")
        if p[0] == '=':
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
        elif p[0] == '!=':
            return run(p[1]) != run(p[2])
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
                for i in p[2]:
                    if didBreak == True:  # case where a block inside this block triggered break, we shouldnt keep executing the current if block
                        break
                    elif i == 'khrej':
                        # dans les instruction de if, si on trouve "khrej" c'est qu'on doit sortir du while,
                        # donc j'ai defini cette variable global, qu'on va verifier dans while pour voir si on a break ou non,
                        # si elle appartient au instructions qui se trouve dans if, je donne true a la variable global,
                        #  et je ne termine pas les autre, instruction
                        didBreak = True
                        break
                    elif didContinue == True:
                        break
                    elif i == 'kmel':
                        # meme principe que break
                        didContinue = True
                        break
                    run(i)
            else:
                if len(p) > 3:
                    for i in p[3]:
                        if didBreak == True:
                            break
                        elif i == 'khrej':
                            didBreak = True
                            break
                        elif didContinue == True:
                            break
                        elif i == 'kmel':
                            didContinue = True
                            break
                        run(i)
        elif p[0] == "ma7ed":
            # on donne a ces variables false au cas ou elle sont devenu true suite a autre boucle
            didBreak = False
            didContinue = False
            while run(p[1]):
                for i in p[2]:
                    # si parmis les instructions qui se trouve directement dans le block de while, je sort de la boucle for,
                    # et du coups en entre pas dans else donc on sort de while(see for/else dans python)
                    if i == 'khrej':
                        break
                    if i == 'kmel':
                        didContinue = True
                        break
                    elif didBreak == True:
                        # je verifie sinon si un if qui s'est executé dans ce block contient un break('khrej'),
                        #  si oui il aura changé didBreak en TRUE, et du coups on va sortir de ce while,
                        didBreak = False
                        break
                    elif didContinue == True:
                        break
                    else:
                        run(i)
                else:
                    continue
                if(didContinue == True):  # in the case of continue, we dont want to exit the loop
                    didContinue = False
                    continue
                break
        elif p[0] == "lkola":
            didBreak = False
            didContinue = False
            if p[1][0] == '=':
                run(p[1])

            while run(p[2]):
                for i in p[4]:
                    if i == 'khrej':
                        break
                    elif i == "kmel":
                        didContinue = True
                        break
                    elif didBreak == True:
                        didBreak = False
                        break
                    elif didContinue == True:
                        break
                    else:
                        run(i)
                else:
                    run(p[3])
                    continue
                if(didContinue == True):  # in the case of continue, we dont want to exit the loop
                    didContinue = False
                    run(p[3])
                    continue
                break
        elif p[0] == 'dir':
            didBreak = False
            didContinue = False
            while(True):
                for i in p[1]:
                    if i == 'khrej':
                        break
                    if i == 'kmel':
                        didContinue = True
                        break
                    elif didBreak == True:
                        didBreak = False
                        break
                    elif didContinue == True:
                        break
                    else:
                        run(i)
                else:
                    if(run(p[2])):
                        continue
                if(didContinue == True):  # in the case of continue, we dont want to exit the loop
                    didContinue = False
                    if(run(p[2])):
                        continue
                break
        elif p[0] == 'qra':
            if p[1] == ')':
                return(int(input()))  # TODO read string, numbers
            else:
                return(int(input(run(p[1])+'\n')))  # TODO read string, numbers
        elif p[0] == "jereb":
            if len(p) == 4:
                try:
                    for i in p[1]:
                        run(i)
                except:
                    for i in p[3]:
                        run(i)
            else:
                try:
                    for i in p[1]:
                        run(i)
                except:
                    for i in p[3]:
                        run(i)
                finally:
                    for i in p[5]:
                        run(i)

    else:
        return p


parser = yacc.yacc()

while True:
    try:
        i = input('>> ')

        # i = '''
        # ila(1>0){
        #     kteb("ok")
        #     ila(5==5){
        #         kteb("yes")
        #         ila(2<1){
        #             kteb("ah")
        #             }
        #         wla{
        #             kteb("no")
        #             a = 0
        #             ma7ed(a<10){
        #                 kteb(a)
        #                 a++
        #                 ila(a==5){
        #                 kteb("by")
        #                 b = 0
        #                 ma7ed(b<10){
        #                     b++
        #                     kteb("b= " + b)
        #                     ila(b==5){
        #                         kteb("by2")
        #                         khrej
        #                     }
        #                 }
        #                 khrej
        #                 }
        #             }
        #         }
        #     }
        # }
        # '''

    except EOFError:
        break
    parser.parse(i)
#     # break
# try:
# f = open(sys.argv[1])
# parser.parse(f.read())
# except:
#     print("Erreur")
