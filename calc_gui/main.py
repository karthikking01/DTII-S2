import re
import os
import tkinter as tk

root = tk.Tk()
root.geometry('400x550')
root.title('Calculator')
root.resizable(False, False)
try:
    icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'image.ico')
    root.iconbitmap(icon_path)
except Exception:
    pass

prim = "#daa6bb"
sec = '#b7ffdd'
tert = "#F09FCF"
for c in range(4):
    root.grid_columnconfigure(c, weight=1)
for r in range(6):
    root.grid_rowconfigure(r, weight=1)

btns = {}
entry = tk.Entry(root, font=('Helvetica', 20), justify='right')

def get_last_number(expr):
    parts = re.split(r'([+\-*/])', expr)
    if not parts:
        return ''
    for token in reversed(parts):
        if token and token not in '+-*/':
            return token
    return ''

def add_text(text):
    entry.insert(tk.END, text)

def add_digit(d):
    add_text(str(d))

def add_double0():
    add_text('00')

def add_dot():
    expr = entry.get()
    last = get_last_number(expr)
    if '.' not in last:
        if last == '':
            add_text('0.')
        else:
            add_text('.')

operators = set('+-*/')

def add_operator(op):
    expr = entry.get()
    if expr == '' and op == '-': 
        add_text(op)
        return
    if expr.endswith(tuple(operators)):
        entry.delete(len(expr)-1, tk.END)
        add_text(op)
    else:
        add_text(op)

def clear_entry():
    entry.delete(0, tk.END)

def backspace():
    expr = entry.get()
    if expr:
        entry.delete(len(expr)-1, tk.END)

def percent():
    expr = entry.get()
    try:
        value = eval(expr, {"__builtins__": None}, {})
        result = value / 100
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

def calculate():
    expr = entry.get()
    try:
        result = eval(expr, {"__builtins__": None}, {})
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

clear = tk.Button(root, text='C', font=('Arial', 25), bg=prim, command=clear_entry)
perc = tk.Button(root, text="%", font=('Arial', 25), bg=prim, command=percent)
bksp = tk.Button(root, text="<", font=('Arial', 25), bg=prim, command=backspace)

div = tk.Button(root, text="/", font=('Arial', 25), bg=sec, command=lambda: add_operator('/'))
add = tk.Button(root, text='+', font=('Arial', 25), bg=sec, command=lambda: add_operator('+'))
sub = tk.Button(root, text='-', font=('Arial', 25), bg=sec, command=lambda: add_operator('-'))
mul = tk.Button(root, text='*', font=('Arial', 25), bg=sec, command=lambda: add_operator('*'))
eq = tk.Button(root, text='=', font=('Arial', 25), bg=sec, command=calculate)

dot = tk.Button(root, text='.', font=('Arial', 25), command=add_dot)
double0 = tk.Button(root, text='00', font=('Arial', 25), command=add_double0)

for i in range(0,10):
    btns[i] = tk.Button(root, text=str(i), font=('Arial', 25), bg=tert, command=lambda x=i: add_digit(x))

entry.grid(row=0, column=0, columnspan=4, sticky='nsew')
clear.grid(row=1, column=0, sticky='nsew')
perc.grid(row=1, column=1, sticky='nsew')
bksp.grid(row=1, column=2, sticky='nsew')

order = [7, 8, 9, 4, 5, 6, 1, 2, 3]
row = 2
col = 0
for n in order:
    btns[n].grid(row=row, column=col, sticky='nsew')
    col += 1
    if col > 2:
        col = 0
        row += 1

div.grid(row=1, column=3, sticky='nsew')
mul.grid(row=2, column=3, sticky='nsew')
sub.grid(row=3, column=3, sticky='nsew')
add.grid(row=4, column=3, sticky='nsew')
eq.grid(row=5, column=3, sticky='nsew')

double0.grid(row=5,column=0, sticky='nsew')
btns[0].grid(row=5,column=1, sticky='nsew')
dot.grid(row=5,column=2, sticky='nsew')
root.mainloop()