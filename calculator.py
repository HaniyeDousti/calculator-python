import math
import inspect
from datetime import datetime

HISTORY_FILE = "history.txt"

#Functions
def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    if num2 == 0:
        return 'Error: division by zero'
    
    return round(num1 / num2, 3)

def power(num1, num2):
    return num1 ** num2

def mod(num1, num2):
    if num2 != 0:
        return num1 % num2
    else:
        return 'Error! modulo by zero'

def square(num1):
    return num1 ** 2

def square_root(num1):
    if num1 >= 0:
        return round(math.sqrt(num1), 5)
    else:
        return 'Error! negative value'

def get_number(prompt):
    while True:
        try: 
            return float(input(prompt))
        except ValueError:
            print('Invalid input! Try again.')

def get_yes_no(prompt):
    while True:
      ask_user = input(prompt).strip()
      if ask_user.lower() in ('y', 'n'):
          return ask_user.lower()
      else:
          print('Error! Your input is wrong.')

def get_operands(func, last_result):
    input_count = len(inspect.signature(func).parameters)
    input_list = []

    for i in range(input_count):
        if i == 0:
            if last_result is not None:

                use_previous = get_yes_no('Use previous result? (Y/N)')

                if use_previous == 'y':
                    print(f'Your previous result is {last_result} ')
                    input_list.append(last_result)

                elif use_previous == 'n':
                    input_list.append(get_number(f'Enter your number {i+1}: '))

            else:
                input_list.append(get_number(f'Enter your number {i+1}: '))
        else:
            input_list.append(get_number(f'Enter your  number {i+1}: '))

    return input_list

def result_is_valid(result):
    return isinstance(result, (int, float))

def format_history_item(item):
    time = item['time']
    operation = item['operation']
    inputs = item['inputs']
    result = item['result']

    return f'[{time}] {operation}:  {" -> ".join(str(i) for i in inputs)}  =  {result}'

def show_history(history):
    if not history:
        print('No history available.')
    else:
        for index, item in enumerate(history, start=1):
            print(f'{index}. {format_history_item(item)}')


def save_history(history, filename):
    with open(filename, "w") as file:
        for item in history:
            file.write(format_history_item(item) + "\n")

def load_history(filename):
    history_text = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                item = parse_history_line(line)
                    
                history_text.append(item)
        return history_text
    
    except FileNotFoundError:
        return []
    
def parse_history_line(line):
    
    time_split = line.split("]")

    time = time_split[0].strip("[")
    parts = time_split[1].split(":", 1)


    operation = parts[0].strip()
    rest = parts[1].strip()

    parts2 = rest.split("=")
    
    rest2 = parts2[0].strip()
    result_text = parts2[1].strip()

    try:
        result = float(result_text)
    except ValueError:
        result = result_text
    
    inputs = rest2.split("->")

    new_inputs = []

    for i in inputs:
        new_inputs.append(float(i.strip()))

    return {
        'time': time,
        'operation': operation,
        'inputs': new_inputs,
        'result': result
    }

def save_operation(history, operation, operands, result):
    history.append({
        'time': datetime.now().strftime("%H:%M:%S"),
        'operation': operation,
        'inputs': operands,
        'result': result
    })

    save_history(history, HISTORY_FILE)

def show_menu():
    for key,value in function_map.items():
        print(key + ')' + value['label'])
    
    print('9) EXIT')
    print('10) Show history')
    print('11) Clear history')

def run_operation(func, last_result):
    operands = get_operands(func, last_result)
    result = func(*operands)
    return operands, result 

def load_last_result(history):
        for item in reversed(history):
            if result_is_valid(item['result']):
                return item['result']
            
        return None

def clear_history():
    return [], None


 #Operation Dict  
function_map = {
    '1': {'func': add, 'label': 'Add'},
    '2': {'func': subtract, 'label': 'Subtract'}, 
    '3': {'func': multiply, 'label': 'Multiply'}, 
    '4': {'func': divide, 'label': 'Divide'},
    '5': {'func': power, 'label': 'Power'},
    '6': {'func': mod, 'label': 'Mod'},
    '7': {'func': square, 'label': 'Square'},
    '8': {'func': square_root, 'label': 'Square_Root'},
    }

def execute_operation(selected_operation, history, last_result):
    func = selected_operation['func']
    operands, result = run_operation(func, last_result) 

    operation = selected_operation['label']

    save_operation(history, operation, operands, result) 

    if result_is_valid(result):
        last_result = result 

    return result, last_result

def main():
    last_result = None
    history = []

    menu_actions = {
    '10': lambda: show_history(history),
    #'11': lambda: clear_history()
}

    history = load_history(HISTORY_FILE)
    last_result = load_last_result(history)

    if history:
        print('History loaded successfully.')

    while True:

        show_menu()

        choice = input('Choose one of the operators from Menu: ').strip()

        if choice == '9':
            break

        if choice in menu_actions:
            menu_actions[choice]() 
            continue

        elif choice == '11':
            history, last_result = clear_history()
            save_history(history, HISTORY_FILE)  
            print('History cleared.')
            continue    

        elif choice in function_map:
            selected_operation = function_map[choice]

            result, last_result = execute_operation(selected_operation, history, last_result)

            print(result)

        else:
            print('Invalid input')


if __name__ == "__main__":
    main()

  
 




