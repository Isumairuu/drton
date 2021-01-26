import sys
from lexer import *
import ply.yacc as yacc

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
           | len
           | empty
           | func
           | appel_func
           | return
           | arrfn
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
               | arrayelt
               | arrayslice
               | arrfn
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
    p[0] = [run(p[2])]


def p_demensions(p):
    '''
    dimensions : dimensions '[' expression ']'
    '''
    p[1].append(run(p[3]))
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
          | ID '.' MSSE7 '(' expression ')'
          | ID '.' MSSE7 '(' ')'
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
        p[0] = [run(p[1])]
    else:
        if(not isinstance(p[1], list)):
            p[1] = [run(p[3])]
        else:
            p[1].append(run(p[3]))
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
    else:
        p[0] = ('appel_func', p[1], p[3])


def p_return(p):
    '''
    return : RED expression

    '''

    p[0] = ('red', p[2])


#################################

def p_printing(p):
    '''
    printing : KTEB '(' condition ')'
            | KTEB '(' incrementation ')'
            | KTEB '(' decrementation ')'
    '''
    p[0] = (p[1], p[3])


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
    try:
        print("Ghalat dyal syntax fster: ", p.lineno)
        print("9bel men:", p.value)
    except AttributeError:
        # p.lineno and p.value might generate error if at the end of block } is missing
        print("Ghalat dyal syntax, t2eked bila ga3 l2a9wass o ma3qofat msdodin")
    exitDarija()


ids = {}
functions = {}
function_arguments = {}
didBreak = False
didContinue = False
locals = [[]]
functions = {}
function_arguments = {}


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def exitDarija():
    if len(sys.argv) > 1:
        exit()


def run(p):
    global ids, didBreak, didContinue, locals
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
            print("Had l'operation li 7awetli dir maymknch!")
            exitDarija()
        if p[0] == '=':
            if p[1][0] == 'arrelt':
                # dimension are stored in a table(p[1][2]), so the objective is to arrive at ids[p[1][1]][1stDim][2ndDim]...[lastDim],
                #  and since when we have array = array, they will share the same memory allocation and any change that will happen to one
                #  will happen to the other, thus with a loop, we advance until we arrive at the dimension before last then
                # we modify the value, we stop at the before last so that our variable would still be a table and would still share
                #  the same memory as our table in "ids"
                tab = ids[p[1][1]]
                j = len(p[1][2])-1
                t = 0
                for i in p[1][2]:
                    if t < j:
                        tab = tab[i]
                    else:
                        break
                    t = t+1
                tab[p[1][2][j]] = run(p[2])
            else:
                if p[1] == 'mojod':
                    ids[p[2][1]] = run(p[2][2])
                    locals[0].append(p[1])
                else:
                    ids[p[1]] = run(p[2])
                    locals[len(locals)-1].append(p[1])
        elif p[0] == 'id':
            try:
                return ids[p[1]]
            except KeyError:
                print("lvariable '"+p[1]+"' makaynach")
                exitDarija()
        elif p[0] == 'kteb':
            print(run(p[1]))
        elif p[0] == 'arrelt':
            try:
                tab = ids[p[1]]
                for i in p[2]:
                    tab = tab[i]
                return tab
            except TypeError:
                print("l'indice li 3titi fih mochkil")
                exitDarija()
            except KeyError:
                print("lvariable '"+p[1]+"' makaynach")
                exitDarija()
        elif p[0] == 'slice':
            try:
                if len(p) == 5:
                    return ids[p[1]][run(p[2]):run(p[4])]
                elif len(p) == 2:
                    return ids[p[1]][:]
                elif len(p) == 4:
                    return ids[p[1]][:run(p[3])]
                else:
                    return ids[p[1]][run(p[2]):]
            except TypeError:
                print('T9d t9sm ghir lists wla joumal!')
                exitDarija()
        elif p[0] == 'arrfn':
            try:
                if p[2] == 'zid':
                    return ids[p[1]].append(run(p[3]))
                elif p[2] == 'kber':
                    return ids[p[1]].extend(run(p[3]))
                elif p[2] == 'khwi':
                    return ids[p[1]].clear()
                elif p[2] == 'dkhel':
                    return ids[p[1]].insert(run(p[3]), run(p[4]))
                elif p[2] == 'msse7':
                    if len(p) == 3:
                        return ids[p[1]].pop()
                    else:
                        return ids[p[1]].pop(run(p[3]))
            except TypeError:
                print("'"+p[2]+"' Kat khdm ghir m3a tableau")
                exitDarija()
        elif p[0] == 'wa':
            return run(p[1]) and run(p[2])
        elif p[0] == 'aw':
            return run(p[1]) or run(p[2])
        elif p[0] == 'comp':
            try:
                if p[1] == '==':
                    return run(p[2]) == run(p[3])
                elif p[1] == '!=':
                    return run(p[2]) != run(p[3])
                elif p[1] == '>=':
                    return run(p[2]) >= run(p[3])
                elif p[1] == '<=':
                    return run(p[2]) <= run(p[3])
                elif p[1] == '>':
                    return run(p[2]) > run(p[3])
                elif p[1] == '<':
                    return run(p[2]) < run(p[3])
            except TypeError:
                print("Maymknch dir had lmo9arana '" +
                      p[1]+"' bles types li 3titi")
                exitDarija()

        elif p[0] == 'l3akss':
            return not(run(p[1]))
        elif p[0] == 'tol':
            try:
                return len(run(p[1]))
            except TypeError:
                print("Kat khdm ghir m3a list wla jomla")
        elif p[0] == "ila":
            if run(p[1]):
                locals.append([])
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
                for i in locals[len(locals)-1]:
                    ids.pop(i)
                locals.pop()
            else:
                if len(p) > 3:
                    locals.append([])
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
                        locals.append([])
                        run(i)
                    for i in locals[len(locals)-1]:
                        ids.pop(i)
                    locals.pop()
        elif p[0] == "ma7ed":
            # on donne a ces variables false au cas ou elle sont devenu true suite a autre boucle
            didBreak = False
            didContinue = False
            locals.append([])
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
            for i in locals[len(locals)-1]:
                ids.pop(i)
            locals.pop()
        elif p[0] == "lkola":
            didBreak = False
            didContinue = False
            locals.append([])
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
            for i in locals[len(locals)-1]:
                ids.pop(i)
            locals.pop()
        elif p[0] == 'dir':
            didBreak = False
            didContinue = False
            locals.append([])
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
            for i in locals[len(locals)-1]:
                ids.pop(i)
            locals.pop()
        elif p[0] == 'qra':
            if p[1] == ')':
                inp = input()
            else:
                inp = input(run(p[1])+'\n')
            if is_number(inp):
                inp = float(inp)
                if inp % int(inp) == 0:
                    return(int(inp))
                else:
                    return(inp)
            else:
                return(inp)

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
        elif p[0] == "ta3rif":
            if(len(p) == 4):
                function_arguments[p[1]] = p[2]
                for i in p[2]:
                    ids[i] = 0

                functions[p[1]] = p[3]
            else:
                functions[p[1]] = p[2]

        elif p[0] == "appel_func":
            if(len(p) == 3):
                k = 0
                for i in function_arguments[p[1]]:
                    ids[i] = p[2][k]
                    k = k+1
            locals.append([])
            for i in functions[p[1]]:
                run(i)
            for j in locals[len(locals)-1]:
                ids.pop(j)
            locals.pop()

    else:
        return p


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
