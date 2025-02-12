"""Lab 1, Choice 2 
Samantha Lomuscio 

This file includes various functions to convert string expressions from: 
    - Prefix to Postfix notation
    - Postfix to Prefix notation
    - Infix to Prefix notation
    - Prefix to Infix notation
    - Postfix to Infix notation

Also included are other functions:
    - Infix to Postfix notation 
    - check_parentheses
    - determine_type
    - log_error
    - convert expression 
"""

from ArrayStack import ArrayStack
import time 

def check_parentheses(input_string:str) -> bool:
    """Checkes whether the expression has matched sets of opening and closing delimeters. 

    Args:
        input_string (str): Input string expression to check. 

    Returns:
        bool: True if all delimeters match. False if they don't. 
    """
    stack = ArrayStack()
    opening_symbols = ['(', '[', '{']
    closing_symbols = [')', ']', '}']

    for character in input_string:

        if character in opening_symbols:  # Push open parentheses to stack.
            stack.push(character)

        elif character in closing_symbols:  # Check if close parentheses match the last open parentheses. 
            if stack.is_empty():  # Return False if the stack is empty because there is no corresponding opening parenthesis. 
                return False

            symbol_idx = opening_symbols.index(stack.pop()) 
            if closing_symbols[symbol_idx] != character:  # Return False if the closing doesnt match the opening parentheses.
                return False
            
    return stack.is_empty()


def determine_type(input_string:str) -> str:
    """Determines if input expression is in Infix, Prefix, or Postfix form.

    Args:
        input_string (str): Input string.

    Raises:
        Exception: Throws exception if the expression is invalid. E.g.) mismatched parentheses, or starts and ends with operators

    Returns:
        str: Type of expression. 
    """
    operators = ['*', '/', '+', '-', '^']

    if (input_string[0] in operators) and (input_string[-1] in operators):  # Check that input doesn't start & end with operators
        raise Exception("Invalid Expression: Begins and ends with operators.")
    
    if input_string[0] in operators:  # Expr. starts with operator --> Prefix
        return "prefix"
    elif input_string[-1] in operators:  # Expr. ends with operator --> Postfix
        return "postfix"
    else: 
        if check_parentheses(input_string):  # Check that parentheses match in expression
            return "infix"
        else:
            raise Exception("Invalid Expression: Mismatched parentheses.")


def prefix_to_postfix(input_string:str) -> str:
    """Converts expression from prefix notation to postfix notation. 
    Time Complexity: O(n)   for loop to parse string
    Space Complexity: O(n)  list for storage in stack 

    Args:
        input_string (str): Input string in prefix notation. 

    Returns:
        str: Output string in postfix notation. 
    """
    stack = ArrayStack()  # Initialize stack instance for analysis. 
    operators = ['*', '/', '+', '-', '^']

    input_string = input_string[::-1]  # Reverse order of string to read Right to Left.

    for character in input_string: 

        if character in operators:  # Pop last 2 items from stack and apply operator on the right.
            pop1 = stack.pop()
            pop2 = stack.pop()
            new_item = pop1 + pop2 + character
            stack.push(new_item)  # Push postfix notation version of expression to stack.

        else: 
            stack.push(character)  # Push item to stack if not an operator.

    return stack.pop()


def postfix_to_prefix(input_string: str) -> str:
    """Converts expression from postix notation to prefix notation. 
    Time Complexity: O(n)   for loop to parse string 
    Space Complexity: O(n)  list for storage in stack

    Args:
        input_string (str): Input string in postfix notation

    Returns:
        str: Output string in prefix notation 
    """
    stack = ArrayStack()  # Initialize stack instance for analysis. 
    operators = ['*', '/', '+', '-', '^']

    for character in input_string: 

        if character in operators:  # Pop last 2 items from stack and apply operator on the left.
            pop1 = stack.pop()
            pop2 = stack.pop()
            new_item = character + pop2 + pop1  
            stack.push(new_item)  # Push postfix notation version of expression to stack. 

        else: 
            stack.push(character)  # Push item to stack if not an operator.

    return stack.pop()


def infix_to_prefix(input_string:str) -> str:
    """Converts expression from infix to prefix. 
    Time Complexity: O(n)   for loop to reverse and another to parse string; __not__ nested for loops.
    Space Complexity: O(n)  list for storage in stack 

    Args:
        input_string (str): Input string in infix notation. 

    Returns:
        str: Output string in prefix notation. 
    """
    # Check that the infix expression is balanced first 
    if not check_parentheses(input_string):
        raise Exception("Mismatched parentheses.")

    stack = ArrayStack()
    operators = ['*', '/', '+', '-', '^']
    prescedence = {'+': 1, '-': 1, '*':2, '/':2, '^':3}
    output_string = ''

    reversed_input_string = ''
    for char in input_string:  # Reverse the input string 
        if char == '(':
            reversed_input_string += ')'  # Make sure to flip parentheses in the reversed string
        elif char == ')':
            reversed_input_string += '('
        else:
            reversed_input_string += char
    reversed_input_string = reversed_input_string[::-1]

    for character in reversed_input_string:

        if character.isalnum() == True:
            output_string += character  # Append values to string that are not operators or parenthesis

        elif character == '(':
            stack.push(character)  # Push open parentheses to stack

        elif character == ')':
            while (not stack.is_empty()):  # and (stack.peek() != '('):
                if stack.peek() == '(':
                    stack.pop()
                    break
                output_string += stack.pop()  # Append all operators held in stack to the string up to "("
            # stack.pop()  # Get rid of the opening parenthsis corresponding to the current character closed parenthesis

        elif character in prescedence:
            # stack.push(character)
            while (not stack.is_empty()) and (stack.peek() != '(') and (prescedence[character] <= prescedence[stack.peek()]):
                output_string += stack.pop()  # Append higher prescedence operators to string compared to current operator
            stack.push(character)

    while not stack.is_empty():
        output_string += stack.pop()  # Append remaining operators to the string 

    return output_string[::-1]


def infix_to_postfix(input_string:str) -> str:
    """EXTRA FUNCTION - ENHANCEMENT :)
    Converts expression from infix to postfix. 

    Args:
        input_string (str): Input string in infix notation. 

    Returns:
        str: Output string in postfix notation. 
    """
    # Check that the infix expression is balanced first 
    if not check_parentheses(input_string):
        raise Exception("Mismatched parentheses.")
    
    stack = ArrayStack()
    operators = ['*', '/', '+', '-', '^']
    prescedence = {'+': 1, '-': 1, '*':2, '/':2, '^':3}
    output_string = ''

    for character in input_string:

        if character.isalnum() == True:
            output_string += character  # Append values to string that are not operators or parenthesis

        elif character == '(':
            stack.push(character)  # Push open parentheses to stack

        elif character == ')': 
            while (not stack.is_empty()):
                if stack.peek() == '(':
                    stack.pop()
                    break
                output_string += stack.pop() 

        elif character in prescedence:
            # stack.push(character)
            while (not stack.is_empty()) and (stack.peek() != '(') and (prescedence[character] <= prescedence[stack.peek()]):
                output_string += stack.pop()  # Append higher prescedence operators to string compared to current operator
            stack.push(character)

    while not stack.is_empty():
        output_string += stack.pop()  # Append remaining operators to the string 

    return output_string
    

def prefix_to_infix(input_string:str) -> str:
    """Converts expression from prefix notation to infix notation.
    Time Complexity: O(n)   for loop to parse string 
    Space Complexity: O(n)  list for storage in stack

    Args:
        input_string (str): Input string in prefix notation. 

    Returns:
        str: Output string in infix notation. Parentheses included. 
    """
    stack = ArrayStack()  # Initialize stack instance for analysis. 
    operators = ['*', '/', '+', '-', '^']

    input_string = input_string[::-1]  # Reverse order of string to read Right to Left.

    for character in input_string:

        if character in operators:  # Pop last 2 items from stack and apply operator. Include parentheses.

            pop1 = stack.pop()
            pop2 = stack.pop()
            new_item = "(" + pop1 + character + pop2 + ")"
            stack.push(new_item)  # Push infix notation version of expression to stack. 
        
        else: 
            stack.push(character)  # Push item to stack if not an operator. 
    
    return stack.pop()


def postfix_to_infix(input_string: str) -> str:
    """Converts expression from postfix notation to infix notation. 
    Time Complexity: O(n)   for loop to parse string 
    Space Complexity: O(n)  list for storage in stack

    Args:
        input_string (str): Input string in postfix notation. 

    Returns:
        str: Output string in infix notation. Parentheses included. 
    """
    stack = ArrayStack()  # Initialize stack instance for analysis. 
    operators = ['*', '/', '+', '-', '^']
    
    for character in input_string:

        if character in operators:  # Pop last 2 items from stack and apply operator. Include parentheses.

            pop1 = stack.pop()
            pop2 = stack.pop()
            new_item = "(" + pop2 + character + pop1 + ")"
            stack.push(new_item)  # Push infix notation version of expression to stack. 

        else: 
            stack.push(character)  # Push item to stack if not an operator. 

    return stack.pop()


def convert_expression(input_string:str, output_file) -> None:
    """Wrapper function that takes input string, determines if it is prefix, postfix, or infix, then calls the appropriate conversion function to convert the input string to either prefix, postfix, or infix. Also, it writes the input string, the input string expressiont type, and the conversions to an output text file. 

    Args:
        input_string (str): Input string to convert. 
        output_file (): File-like object to write output to. 
    """
    start_time = time.time()
    print("===========================================================", file=output_file)
    print(f"Input String:\t   {input_string}\n", file=output_file)
    expression_type = determine_type(input_string)
    print(f"Input String Type: {expression_type}\n", file=output_file)

    if expression_type == "postfix":
        infix = postfix_to_infix(input_string)
        prefix = postfix_to_prefix(input_string)
        print(f"Infix version:\t{infix}", file=output_file)
        print(f"Prefix version:\t{prefix}", file=output_file)

    elif expression_type == "prefix":
        infix = prefix_to_infix(input_string)
        prefix = prefix_to_postfix(input_string)
        print(f"Infix version:\t {infix}", file=output_file)
        print(f"Postfix version: {prefix}", file=output_file)

    elif expression_type == "infix":
        prefix = infix_to_prefix(input_string)
        postfix = infix_to_postfix(input_string)
        print(f"Prefix version:\t\t{prefix}", file=output_file)
        print(f"Postfix version:\t{postfix}", file=output_file)
    stop_time = time.time()
    total_time = stop_time - start_time
    print(f"\nTotal time taken to convert: {total_time*1000000:.4g} microseconds.", file=output_file)
    print("===========================================================\n", file=output_file)


def log_error(e:Exception, output_file) -> None:
    """Logs error to the output text file. 

    Args:
        e (Exception): Exception thrown.
        output_file (): File-like object to write output to. 
    """
    print(f"Error in expression:", file=output_file)
    print(f"\t\t{e}", file=output_file)
    print("===========================================================\n", file=output_file)


def main():
    """Main function to convert expressions to/from infix, prefix, and postfix notation. 
    """
    import os

    current_file_path = os.path.dirname(os.path.abspath(__file__))  # Find the path to this file.
    os.chdir(current_file_path)  # cd to the directory containing this file.

    input_file = os.path.join(current_file_path, "input_output", "input.txt")
    output_file = os.path.join(current_file_path, "input_output", "output.txt")

    
    with open(input_file, 'r') as f:  # Open input text file containing input cases.
        with open(output_file, 'w') as output_f:  # Open output file to write output to. 

            for line in f:  # Loop through each line in the input text file. Each line is an input string. 
                input_string = line.strip().replace(" ", "")  # Remove all spaces from input strings.

                if len(input_string) == 0:  # Skip empty lines in the file.
                    continue
                
                try:
                    convert_expression(input_string, output_f)  # Determine format of string, & convert. Write output to file.
                except Exception as e:
                    log_error(e, output_f)

if __name__=="__main__":
    main()
