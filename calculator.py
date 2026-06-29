import tkinter as tk
from tkinter import ttk

BUTTONS = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "=", ""],
]


def evaluate_expression(expression):
    sanitized = expression.replace("×", "*").replace("÷", "/")
    if not sanitized or not all(ch in "0123456789.+-*/()% " for ch in sanitized):
        return "Error"

    try:
        result = eval(sanitized)
        return result
    except Exception:
        return "Error"


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nova Calculator")
        self.geometry("372x560")
        self.resizable(False, False)
        self.configure(bg="#07111f")

        self.value = tk.StringVar(value="0")
        self._create_widgets()

    def _create_widgets(self):
        display = ttk.Entry(
            self,
            textvariable=self.value,
            justify="right",
            font=("Inter", 28, "bold"),
            state="readonly",
            width=16,
        )
        display.grid(row=0, column=0, columnspan=4, padx=18, pady=(18, 12), sticky="nsew")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TEntry", fieldbackground="#0f172a", foreground="#f8fafc", borderwidth=0)
        style.configure("TButton", padding=16, font=("Inter", 16), borderwidth=0)

        for row_index, row in enumerate(BUTTONS, start=1):
            for col_index, label in enumerate(row):
                if not label:
                    continue
                button = ttk.Button(self, text=label, command=lambda l=label: self.on_button_press(l))
                button.grid(row=row_index, column=col_index, padx=8, pady=8, sticky="nsew")

                if label in {"+", "-", "×", "÷", "="}:
                    button.configure(style="Operator.TButton")
                elif label in {"C", "⌫", "%"}:
                    button.configure(style="Function.TButton")

        style.configure("Operator.TButton", background="#6366f1", foreground="white")
        style.map("Operator.TButton", background=[("active", "#4f46e5")])
        style.configure("Function.TButton", background="#334155", foreground="#f8fafc")
        style.map("Function.TButton", background=[("active", "#475569")])

        for i in range(1, 6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def on_button_press(self, label):
        if label == "C":
            self.value.set("0")
            return
        if label == "⌫":
            current = self.value.get()
            self.value.set(current[:-1] if len(current) > 1 else "0")
            return
        if label == "%":
            self.handle_percent()
            return
        if label == "=":
            self.calculate()
            return
        self.append_value(label)

    def append_value(self, label):
        current = self.value.get()
        if current == "0" and label != ".":
            self.value.set(label)
        else:
            self.value.set(current + label)

    def handle_percent(self):
        result = evaluate_expression(self.value.get())
        if result == "Error":
            self.value.set("Error")
        else:
            self.value.set(str(result / 100))

    def calculate(self):
        result = evaluate_expression(self.value.get())
        self.value.set(str(result) if result != "Error" else "Error")


if __name__ == "__main__":
    Calculator().mainloop()
