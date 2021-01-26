# darija-compiler
**NAME** is a mini-compiler for a programming language written in *[Darija](https://en.wikipedia.org/wiki/Moroccan_Arabic)*. 
This mini-compiler will include its own lexical, syntactic and semantic analyzer, it is based on Python, that serves as an intermediate language to generate the machine language. 

## Requirements
* Python3
* Python ply

## TOKENS (and python equivalent):
* kteb : print
* qra : input
* ila  : if
* wla  : else
* dir  : do
* ma7ed  : while
* lkola  : for
* khrej  : break
* kmel  : continue
* wa  : and
* aw  : or
* khate2  : false
* s7i7  : true
* mojod  : global
* walo  : None
* l3akss  : not
* ta3rif  : def
* red  : return
* jereb  : try
* masd9ch  : except
* akhiran  : finally
* douz  : pass
* tol  : len
* zid  : append
* kber  : extend
* msse7  : pop
* dkhel  : insert
* khwi  : clear

## Data types:
* int `123456`
* float `12.3456`
* strings `'string'` or `"string"`
* lists `[]`

## Features:
* Variables
* Comments
* Control flow statements:
    - loops (while,do-while,for)
    - conditional statements
    - function calls
    - exceptions
* Operators:
    - artihmetic : `+ - * / `
    - comparison : `> >= < <= == !=`
    - logical : `and or not`
    - assignement : `=`
    - unary : `++ --`