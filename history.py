from datetime import datetime

class HistoryManager:

    def __init__(self, filename='history.txt'):

        self.history_file = filename
        self.history = self.load_history()

    def save_operation(self, operation_name, operands, result):
        self.history.append({
            'time': datetime.now().strftime("%H:%M:%S"),
            'operation': operation_name,
            'inputs': operands,
            'result': result
    })
        self.save_history()

    def get_last_result(self):
        if not self.history:
            return None
        else:
            return self.history[-1]['result']

    def save_history(self):
        with open(self.history_file, "w") as file:
            for item in self.history:
                file.write(self.format_history_item(item) + "\n")

    def format_history_item(self, item):
        time = item['time']
        operation = item['operation']
        inputs = item['inputs']
        result = item['result']

        return f'[{time}] {operation}:  {" -> ".join(str(i) for i in inputs)}  =  {result}' 

    def load_history(self):
        history = []
        try:
            with open(self.history_file, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    item = self.parse_history_line(line)
                    
                    history.append(item)
            return history
    
        except FileNotFoundError:
            return []

    def parse_history_line(self, line):
    
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

    def show_history(self):
        return self.history
