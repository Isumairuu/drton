# darija-compiler
**NAME** is a mini-compiler for a programming language written in *[Darija](https://en.wikipedia.org/wiki/Moroccan_Arabic)*. 
This mini-compiler will include its own lexical, syntactic and semantic analyzer, it is based on Python, that serves as an intermediate language to generate the machine language. 

## Requirements
* Python3
* Python ply

## Keywords (and equivalent in python):
Keyword | Python 
------------ | -------------
 `kteb` | `print`
 `qra` | `input`
 `ila ` | `if`
 `wla ` | `else`
 `dir ` | `do`
 `ma7ed ` | `while`
 `lkola ` | `for`
 `khrej ` | `break`
 `kmel ` | `continue`
 `wa ` | `and`
 `aw ` | `or`
 `khate2 ` | `false`
 `s7i7 ` | `true`
 `mojod ` | `global`
 `walo ` | `None`
 `l3akss ` | `not`
 `ta3rif ` | `def`
 `red ` | `return`
 `jereb ` | `try`
 `masd9ch ` | `except`
 `akhiran ` | `finally`
 `douz ` | `pass`
 `tol ` | `len`
 `zid ` | `append`
 `kber ` | `extend`
 `msse7 ` | `pop`
 `dkhel ` | `insert`
 `khwi ` | `clear`

## Features:
* Variables
* Comments
* Control flow statements:
    - loops (while,do-while,for)
    - conditional statements
    - function calls
    - exceptions
* Operators:
    - artihmetic : `+ - * / % ^`
    - comparison : `> >= < <= == !=`
    - logical : `and or not`
    - assignement : `=`
    - unary : `++ --`

### Identifiers:
Rules for writing identifiers:
1. Identifiers can be a combination of letters in lowercase or uppercase or digits or an underscore _. 
2. An identifier cannot start with a digit.
3. Keywords cannot be used as identifiers.
4. Variables are case sensitive `test` is different than `Test`. 

### Comments:
Any instruction that starts with `#` will be ignored.

### Data types:
* **Numbers**:
You can use either integers or floating points numbers in this language.
    - int : `123`
    - float: `1.23`

* **Strings** : You can choose either `'string'` or `"string"` to represent a string.  
We can use the slicing operator [ ] to extract an item or parts of the string:
    ```Python
    a= "hello world!"
    kteb(a[0:5]) 
    hello
    ```

* **lists** : `['hello',455,1.23]`
We can use the slicing operator [ ] with lists too.
    ```Python
    a = [5,10,15,20,25,30,35,40]

    kteb(a[2])
    # Output: 15

    kteb(a[0:3])
    # Output: [5, 10, 15]

    kteb("a[5:]")
    # Output: [30, 35, 40]
    ```



### Operators:
* Arithmetic operators:
    ```Python
    x = 15
    y = 4

    kteb(x+y)
    # Output: 19

    kteb(x-y)
    # Output: 11

    kteb(x*y)
    # Output: 60

    kteb(x/y)
    # Output: 3.75

    kteb(x%y)
    # Output: 3

    kteb(x^y) # x power y
    # Output: 50625 
    ```

* Comparison operators:
    ```Python
    x = 10
    y = 12

    kteb(x>y)
    # Output: khate2

    kteb(x<y)
    # Output: s7i7

    kteb(x==y)
    # Output: khate2

    kteb(x!=y)
    # Output: s7i7

    kteb(x>=y)
    # Output: khate2

    kteb(x<=y)
    # Output: s7i7
    ```

* Logical operators:
    ```Python
        x = s7i7
        y = khate2

        print(x wa y)
        # Output: khate2

        print(x aw y)
        # Output: s7i7
    ```

### Flow control:
* **ila..wla** (*if..else*):
    - The `ila..wla` statement evaluates test expression and will execute the body of `ila` only when the test condition is `s7i7` (True).\
    If the condition is `khate2` (false), the body of `wla` is executed. *(The indent is unecessary)*
        ```Python
        num=5 #or num=-5
        ila(num >= 0){
            kteb('The number is positive')
        }
        wla{
            kteb('The number is negative')
        }
        ```
    - We can have a `ila..wla` statement inside another `ila..wla` statement. This is called nesting in computer programming. 
        ```Python
        num = qra("Enter a number: ")
        ila (num >= 0){
            ila (num == 0){
                kteb("Zero")
            }
            wla{
                kteb("Positive number")
            }
        }
        wla{
            print("Negative number")
        }
        ```

* **lkola** (*for loop*):

