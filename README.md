# drton
**drton** is a mini-compiler for a programming language written in *[Darija](https://en.wikipedia.org/wiki/Moroccan_Arabic)*. 
This mini-compiler has its own lexical, syntactic and semantic analyzer. It is based on mostly on Python, which is also used as an intermediate language to generate the machine language by using python [ply](https://www.dabeaz.com/ply/).

## Requirements:
* Python (v3.7+)
* Python ply `pip install ply`

## Use:
You can start using it by using the following commands:
* `python parser.py` for interpreted mode
* `python parser.py file.dr` to compile a file

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
 `tol ` | `len`
 `zid ` | `append`
 `kber ` | `extend`
 `n9s ` | `pop`
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
    - arithmetic : `+ - * / % ^`
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
We can use the slicing operator *[ : ]* to extract an item or parts of the string:
    ```Python
    a= "hello world!"
    kteb(a[0:5]) 
    hello
    ```

* **Lists** : \
A list is created by placing all the items (elements) inside square brackets [ ], separated by commas.

    ```Python
    a = [5,10,15,20,25,30,35,40]

    kteb(a[2])
    # Output: 15

    kteb(a[0:3])
    # Output: [5, 10, 15]

    kteb("a[5:]")
    # Output: [30, 35, 40]
    ```
    - Lists indexing:

        ```Python
        # List indexing
        my_list = ['p', 'r', 'o', 'b', 'e']

        kteb(my_list[0])
        # Output: p

        kteb(my_list[2])
        # Output: o

        kteb(my_list[4])
        # Output: e

        n_list = ["Happy", [2, 0, 1, 5]]
        # Nested List

        kteb(n_list[0][1])
        # Output: a

        kteb(n_list[1][3])
        # Output: 5
        ```

    - List slicing:

        ```Python
        my_list = ['p','r','o','g','r','a','m','i','z']

        kteb(my_list[2:5])
        # Output: elements 3rd to 5th

        kteb(my_list[:-5])
        # Output: elements beginning to 4th

        kteb(my_list[5:])
        # Output: elements 6th to end

        kteb(my_list[:])
        # Output: elements beginning to end
        ```
    - The following methods can be used with lists:

        ```Python
        a=[1,2,3,4]

        a.zid(5) # pushes an element to the end of the list
        # Output: [1,2,3,4,5]

        a.n9s() # pops the last element of the list
        # Output: [1,2,3,4]

        a.n9s(2) # pops the element at the indicated index
        # Output: [1,2,4]
        
        a.dkhel(2,3) # insert an element at the given index 
        # Output: [1,2,3,4]

        a.kber([5,6,7,8]) # pushes a list to the end of the list
        # Output: [1, 2, 3, 4, 5, 6, 7, 8]

        a.khwi() # deletes all elements of the given list
        # Output: []
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

    kteb(x wa y)
    # Output: khate2

    kteb(x aw y)
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
            kteb("Negative number")
        }
        ```

* **lkola** (*for loop*):\
The `lkola` loop is used to iterate over a sequence.

    ```Python
    lkola(i=0;i<5;i++){
        kteb("Iteration:",i)
    }
    ```

* **ma7ed** (*while loop*):\
The `ma7ed` loop is used to iterate over a block of code as long as the test expression (condition) is true.

    ```Python
    n = 10
    # initialize sum and counter
    sum = 0
    i=1
    ma7ed(i<n){
        sum = sum + i
        i = i+1    # update counter
    }
    # print the sum
    kteb("The sum is", sum) # Output : The sum is 45
    ```

* **khrej** (*break*):
The `khrej` statement terminates the loop containing it. Control of the program flows to the statement immediately after the body of the loop.

    ```Python
    str="string"
    lkola (a=0;a<tol(str);a++){
        ila(str[a] == "i"){
            khrej
        }
        kteb(str[a])
    }
    kteb("The end")
    # Output:
    #s
    #t
    #r
    #The end
    ```

* **kmel** (*continue*):
The `kmel` statement is used to skip the rest of the code inside a loop for the current iteration only. Loop does not terminate but continues on with the next iteration.

    ```Python
    str="string"
    lkola (a=0;a<tol(str);a++){
        ila(str[a] == "i"){
            kmel
        }
        kteb(str[a])
    }
    kteb("The end")
    # Output:
    #s
    #t
    #r
    #n
    #g
    #The end
    ```

* **ta3rif** (*function def*):\
A function is a group of related statements that performs a specific task.
    - You can use a function without a return statement:

        ```Python
        ta3rif greet(name){ #indent is unecessary but used for styling
            kteb("Salam, " , name)
        }

        greet('Ibrahim') # Output: Salam, Ibrahim
        ```
    - As you can use it with a return `red` statement:

        ```Python
        ta3rif absolute_value(num){
            ila(num >= 0){
                red(num)
            }
            wla{
                red(-num)
            }
        }

        kteb(absolute_value(2)) # Output: 2
        kteb(absolute_value(-4)) # Output: 4
        ```
> You'll find more examples in the examples folder!

* **jereb..masd9ch..akhiran** *(try..except..finally)*:

    ```Python
        str="string"
        jereb{
            lkola (a=0;a<tol(str);a++){
                kteb(str[a]) #we can triger error by removing this
            }
        }
        masd9ch{
            kteb('There is a problem!')
        }
        akhiran{
            kteb('default case')
        }
        # Output: if there is no error:
        # s
        # t
        # r
        # i
        # n
        # g
        # default case
        
        # Output: if there is an error:
        # There is a problem!
        # default case
    ```
