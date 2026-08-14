import tkinter as tk
import operations
from history import HistoryManager
import inspect



class Calculator:
    def __init__(self):

        self.history_manager = HistoryManager()

        self.last_result = self.history_manager.get_last_result()

        self.window = tk.Tk()

        self.window.title("My Python Calculator")
        self.window.geometry("400x500")

        self.button_map = {
            'Add':operations.add,
            'Subtract': operations.subtract, 
            'Multiply': operations.multiply, 
            'Divide': operations.divide,
            'Power': operations.power,
            'Mod': operations.mod,
            'Square': operations.square,
            'Square_Root': operations.square_root
    }
        
        self.create_widgets()
        self.create_buttons()
        self.bind_events()

    def create_widgets(self):
        
        self.input_entry1 = tk.Entry(self.window)
        self.input_entry1.grid(row=0, column=0)
        self.input_entry1.focus_set()
        
        self.input_entry2 = tk.Entry(self.window)
        self.input_entry2.grid(row=0, column=1)
        
        self.label = tk.Label(self.window, text="")
        self.label.grid(row=1, column=0, columnspan=2)

    def create_buttons(self):

        button_style = {
                    "width": 12,
                    "height": 2,
                    "font": ("Arial", 11)
                }
        for index, (text, func) in enumerate(self.button_map.items()):
        
                   button = tk.Button(
                   self.window, 
                   text= text,
                   command = lambda text=text, func = func: self.handle_operation(text, func),
                   **button_style
               )
        
                   button.grid(row = index // 2 + 2, column = index % 2)
        
        clear_button = tk.Button(
                   self.window, 
                   text = 'Clear',
                   command= self.clear,
                   **button_style
               )
        clear_button.grid(row = 6, column = 0, columnspan = 1)


        history_button = tk.Button(
            self.window,
            text = 'History',
            command = self.show_history,
            **button_style
        )
        history_button.grid(row=6, column=1, columnspan=2)

        Ans_button = tk.Button(
                    self.window,
                    text = 'Ans',
                    command = self.insert_last_result,
                    **button_style
                )
        Ans_button.grid(row=7, column=0, columnspan=1)

    def bind_events(self):
        
        self.window.bind(
                    "<Escape>",
                    lambda event: self.window.destroy()
                ) 

        self.input_entry1.bind("<Right>", self.move_right)

        self.input_entry2.bind("<Left>", self.move_left)

    def move_right(self, event):
        self.input_entry2.focus_set()
        return 'break'

    def move_left(self, event):
        self.input_entry1.focus_set()
        return 'break'
    
    def clear(self):
        self.input_entry1.delete(0, tk.END)
        self.input_entry2.delete(0, tk.END)
        self.show_result("", 'black')
        self.input_entry1.focus_set()

    def show_history(self):
        history = self.history_manager.show_history()

        history_window = tk.Toplevel(self.window)
        history_window.title('History')
        history_window.geometry('500x400')

        history_text = tk.Text(history_window)
        history_text.pack(fill = tk.BOTH, expand=True)

        if not history:
            history_text.insert(tk.END, 'No History available!')
        else:
            for item in reversed(history):
                history_text.insert(
                    tk.END,
                    self.history_manager.format_history_item(item) + '\n'
                )
    def show_result(self, text, color):
        self.label.config(
        text = text,
        fg = color
      )
        
    def execute_operation(self, operation_func, operands):

        return operation_func(*operands)
        
    def get_result_color(self, result):
        return 'green' if self.result_is_valid(result) else 'red'

    def get_operands(self, operation_func):
        operands = []

        parameter_counts = len(inspect.signature(operation_func).parameters)
        num1 = float(self.input_entry1.get())
        operands.append(num1)

        if parameter_counts == 2:
            num2_text = self.input_entry2.get()
            if not num2_text:
                raise ValueError('Second_input required')
            num2 = float(num2_text)
            operands.append(num2)

        return operands
        
    def handle_operation(self, text, operation_func):

        try:

            operands = self.get_operands(operation_func)
            result = self.execute_operation(operation_func, operands)   

            color = self.get_result_color(result)

            self.show_result(result, color)

            if self.result_is_valid(result):
                self.last_result = result 

            self.history_manager.save_operation(
                text, 
                operands,
                result
            )

        except ValueError:
            self.show_result('Invalid Input!', 'red')

    def result_is_valid(self, result):
        return isinstance(result, (int, float))

    def insert_last_result(self):
        if self.last_result is None:
            return
        else:
            self.input_entry1.delete(0, tk.END)
            self.input_entry1.insert(0, self.last_result)
            self.input_entry2.delete(0, tk.END)
            self.input_entry2.focus_set()
