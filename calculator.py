import tkinter as tk
from tkinter import ttk

BUTTONS = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "=", ""],
]


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("360x520")
        self.resizable(False, False)
        self['bg'] = '#f5f7fb'

        self.value = tk.StringVar(value='0')
        self._create_widgets()

    def _create_widgets(self):
        display = ttk.Entry(
            self,
            textvariable=self.value,
            justify='right',
            font=('Inter', 28),
            state='readonly',
            width=14,
        )
        display.grid(row=0, column=0, columnspan=4, padx=16, pady=(16, 8), sticky='nsew')

        style = ttk.Style(self)
        style.configure('TButton', padding=16, font=('Inter', 16))

        for row_index, row in enumerate(BUTTONS, start=1):
            for col_index, label in enumerate(row):
                if not label:
                    continue
                button = ttk.Button(self, text=label, command=lambda l=label: self.on_button_press(l))
                button.grid(row=row_index, column=col_index, padx=8, pady=8, sticky='nsew')

                if label in {'+', '-', '×', '÷', '='}:
                    button.configure(style='Operator.TButton')
                elif label in {'C', '⌫', '%'}:
                    button.configure(style='Function.TButton')

        style.configure('Operator.TButton', background='#4338ca', foreground='white')
        style.map('Operator.TButton', background=[('active', '#312e81')])
        style.configure('Function.TButton', background='#e2e8f0', foreground='#1e293b')
        style.map('Function.TButton', background=[('active', '#cbd5e1')])

        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def on_button_press(self, label):
        if label == 'C':
            self.value.set('0')
            return
        if label == '⌫':
            current = self.value.get()
            self.value.set(current[:-1] if len(current) > 1 else '0')
            return
        if label == '%':
            self.handle_percent()
            return
        if label == '=':
            self.calculate()
            return
        self.append_value(label)

    def append_value(self, label):
        current = self.value.get()
        if current == '0' and label != '.':
            self.value.set(label)
        else:
            self.value.set(current + label)

    def handle_percent(self):
        expression = self._sanitize_expression(self.value.get())
        try:
            result = eval(expression)
            self.value.set(str(result / 100))
        except Exception:
            self.value.set('Error')

    def calculate(self):
        expression = self._sanitize_expression(self.value.get())
        if not self._is_valid_expression(expression):
            self.value.set('Error')
            return
        try:
            result = eval(expression)
            self.value.set(str(result))
        except Exception:
            self.value.set('Error')

    @staticmethod
    def _sanitize_expression(expression):
        return expression.replace('×', '*').replace('÷', '/')

    @staticmethod
    def _is_valid_expression(expression):
        return bool(expression) and all(ch in '0123456789.+-*/()% ' for ch in expression)


if __name__ == '__main__':
    Calculator().mainloop()
