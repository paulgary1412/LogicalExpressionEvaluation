import itertools

def convert_to_postfix(infix):
    precedence = {'~': 4, '&': 3, '|': 2, '>': 1, '=': 0}
    stack = []
    postfix = ''

    for char in infix:
        if char.isalpha():
            postfix += char
        elif char in precedence.keys():
            while stack and stack[-1] != '(' and precedence[char] <= precedence[stack[-1]]:
                postfix += stack.pop()
            stack.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()

    while stack:
        postfix += stack.pop()

    return postfix

def evaluate_postfix(postfix, values):
    stack = []

    for char in postfix:
        if char.isalpha():
            stack.append(values[char])
        elif char == '~':
            operand = stack.pop()
            stack.append(not operand)
        else:
            operand2 = stack.pop()
            operand1 = stack.pop()
            
            if char == '&':
                result = operand1 and operand2
            elif char == '|':
                result = operand1 or operand2
            elif char == '>':
                result = not operand1 or operand2
            elif char == '=':
                result = (not operand1 or operand2) and (not operand2 or operand1)
            
            stack.append(result)

    return stack.pop()

def display_truth_table(var_list, input_expr):
    num_vars = len(var_list)
    postfix_expr = convert_to_postfix(input_expr)

    print(" |  ".join(var_list + [input_expr, "Result"]))
    print("".join("" for _ in range(len(var_list) + 3)))

    results = []

    for vals in itertools.product([True, False], repeat=num_vars):
        var_dict = {var_list[i]: vals[i] for i in range(num_vars)}
        result = evaluate_postfix(postfix_expr, var_dict)
        results.append(result)
        
        row_vals = [f'T   ' if val else f'F   ' for val in vals] + [f'T   ' if var_dict[var] else f'F   ' for var in var_list] + [f'T   ' if result else f'F   ']
        print("|".join(row_vals))

    if all(results):
        print("The logical expression is a Tautology.")
    elif not any(results):
        print("The logical expression is a Contradiction.")
    else:
        print("The logical expression is neither a Tautology nor a Contradiction.")

def evaluate_logical_expression():
    input_expr = input('Enter a logical expression: ')
    input_expr = input_expr.replace("V", "|")
    input_expr = input_expr.replace("v", "|")
    input_expr = input_expr.replace("^", "&")

    char_list = list(set(input_expr))
    var_list = [c for c in char_list if c.isalpha()]
    var_list.sort()

    values = {}
    for var in var_list:
        values[var] = input(f'Enter truth value for {var} (T or F): ') == 'T'

    postfix_expr = convert_to_postfix(input_expr)
    result = evaluate_postfix(postfix_expr, values)

    print(f'The result of the logical expression is: {"T" if result else "F"}')

    option_display_truth_table = input('Do you want to display the truth table? (Y/N): ')
    if option_display_truth_table.lower() == 'y':
        display_truth_table(var_list, input_expr)

def main_program():
    global exit_flag
    print("Options:")
    print("1. Logical Expression Evaluator")
    print("2. Display Truth Table")
    print("3. Exit")

    option = input('Enter the option (1, 2, or 3): ')

    if option == '1':
        evaluate_logical_expression()
    elif option == '2':
        input_expr = input('Enter a logical expression with conclusion: ')
        char_list = list(set(input_expr))
        var_list = [c for c in char_list if c.isalpha()]
        var_list.sort()

        display_truth_table(var_list, input_expr)
    elif option == '3':
        print("Program Terminated.")
        exit_flag = 1
    else:
        print('Invalid option. Please enter 1, 2, or 3.')

exit_flag = 0

while exit_flag == 0:
    main_program()
