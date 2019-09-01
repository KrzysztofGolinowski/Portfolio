import operator
import math

# dict of operators and assigned to them function and number of arguments
functions = {'+': [operator.add, 2], 
             '-': [operator.sub, 2], 
             '*': [operator.mul, 2], 
             '/': [operator.truediv, 2], 
             '//': [operator.floordiv, 2], 
             
             '^': [operator.pow, 2],
             'abs': [operator.abs, 1], 
             'neg': [operator.neg, 1], 
             'mod': [operator.mod, 2], 
             
             'pi': [math.pi, 0], 
             'e': [math.e, 0],
             'sqrt': [math.sqrt, 1],
             'sin': [math.sin, 1], 
             'cos': [math.cos, 1], 
             'tan': [math.tan, 1],
             'exp': [math.exp, 1], 
             'ln': [math.log, 1],
             'log': [math.log, 2],
             
             '−': [operator.sub, 2], 
             '×': [operator.mul, 2],
             '÷': [operator.truediv, 2], 
             '**': [operator.pow, 2], 
             '%': [operator.mod, 2]}
    
def calc_rpn(equation):
    
    # trim input and prepare stack
    stack = []

    for i in equation.split():
        
        # check if element is operator
        if i in functions:
            
            # get function of 
            op = functions[i]
            
            # if zero args function, like math.pi, just add value to stack
            if op[1] == 0:
                stack.append(op[0])
            
            # else, check if stack has enought elements, if yes - add result to stack
            elif op[1] <= len(stack):
                args = [stack.pop() for _ in range(op[1])][::-1]
                stack.append(op[0](*args))
            
            # otherwise raise exception
            else:
                raise Exception("Not enought values on stack to call '{}'".format(i))
        
        # check if element seems to be float
        elif set(i).issubset("-+0123456789.e"):
            # try to convert it to float
            try:
                stack.append(float(i))
            except ValueError:
                raise Exception("Cannot convert element '{}' to float".format(i))
            
        else:
            raise Exception("Not regonized char in: '{}'".format(i))

    # check if only 1 value left on the stack
    if len(stack) == 1:
        return stack[0]
    else:
        raise Exception("After all calculations there is no single value remaining on the stack. Check your expression!")


if __name__ == '__main__':

    print("To stop, type 'exit', 'quit' or 'q'")
    while True:
        eq = input('Please input your expression: ')

        if eq.lower() in ['exit', 'quit', 'q']:
            break

        print("= {}".format(calc_rpn(eq)))

