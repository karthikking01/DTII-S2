import math
import tkinter as tk
from tkinter import ttk


class ScientificCalculator(tk.Tk):
	def __init__(self) -> None:
		super().__init__()
		self.title("Scientific Calculator")
		self.resizable(False, False)
		self.configure(bg="#10151f")

		self._create_styles()
		self._expression = tk.StringVar(value="")
		self._create_widgets()

	def _create_styles(self) -> None:
		style = ttk.Style(self)
		style.theme_use("clam")

		style.configure(
			"Display.TEntry",
			font=("Segoe UI", 20),
			padding=12,
			foreground="#e8edf4",
			fieldbackground="#1b2230",
			background="#1b2230",
			borderwidth=0,
		)

		style.configure(
			"Calc.TButton",
			font=("Segoe UI", 12),
			padding=10,
			foreground="#e8edf4",
			background="#222a3a",
			borderwidth=0,
		)

		style.map(
			"Calc.TButton",
			background=[("active", "#2c364a")],
		)

		style.configure(
			"Accent.TButton",
			font=("Segoe UI", 12, "bold"),
			padding=10,
			foreground="#ffffff",
			background="#3b82f6",
			borderwidth=0,
		)

		style.map(
			"Accent.TButton",
			background=[("active", "#2563eb")],
		)

		style.configure(
			"Danger.TButton",
			font=("Segoe UI", 12, "bold"),
			padding=10,
			foreground="#ffffff",
			background="#ef4444",
			borderwidth=0,
		)

		style.map(
			"Danger.TButton",
			background=[("active", "#dc2626")],
		)

	def _create_widgets(self) -> None:
		container = ttk.Frame(self, padding=16)
		container.grid(row=0, column=0)

		display = ttk.Entry(
			container,
			textvariable=self._expression,
			justify="right",
			style="Display.TEntry",
			width=24,
		)
		display.grid(row=0, column=0, columnspan=6, sticky="ew", pady=(0, 12))
		display.focus_set()

		for col in range(6):
			container.grid_columnconfigure(col, weight=1)

		buttons = [
			("C", self._clear, "Danger.TButton"),
			("⌫", self._backspace, "Danger.TButton"),
			("(", lambda: self._append("("), "Calc.TButton"),
			(")", lambda: self._append(")"), "Calc.TButton"),
			("π", lambda: self._append("pi"), "Calc.TButton"),
			("e", lambda: self._append("e"), "Calc.TButton"),
			("sin", lambda: self._append("sin("), "Calc.TButton"),
			("cos", lambda: self._append("cos("), "Calc.TButton"),
			("tan", lambda: self._append("tan("), "Calc.TButton"),
			("asin", lambda: self._append("asin("), "Calc.TButton"),
			("acos", lambda: self._append("acos("), "Calc.TButton"),
			("atan", lambda: self._append("atan("), "Calc.TButton"),
			("xʸ", lambda: self._append("**"), "Calc.TButton"),
			("x²", lambda: self._append("**2"), "Calc.TButton"),
			("x³", lambda: self._append("**3"), "Calc.TButton"),
			("√", lambda: self._append("sqrt("), "Calc.TButton"),
			("∛", lambda: self._append("cbrt("), "Calc.TButton"),
			("n√", lambda: self._append("root("), "Calc.TButton"),
			("7", lambda: self._append("7"), "Calc.TButton"),
			("8", lambda: self._append("8"), "Calc.TButton"),
			("9", lambda: self._append("9"), "Calc.TButton"),
			("/", lambda: self._append("/"), "Calc.TButton"),
			("%", lambda: self._append("%"), "Calc.TButton"),
			("!", lambda: self._append("!"), "Calc.TButton"),
			("4", lambda: self._append("4"), "Calc.TButton"),
			("5", lambda: self._append("5"), "Calc.TButton"),
			("6", lambda: self._append("6"), "Calc.TButton"),
			("*", lambda: self._append("*"), "Calc.TButton"),
			("ln", lambda: self._append("ln("), "Calc.TButton"),
			("log", lambda: self._append("log("), "Calc.TButton"),
			("1", lambda: self._append("1"), "Calc.TButton"),
			("2", lambda: self._append("2"), "Calc.TButton"),
			("3", lambda: self._append("3"), "Calc.TButton"),
			("-", lambda: self._append("-"), "Calc.TButton"),
			("10ˣ", lambda: self._append("10**"), "Calc.TButton"),
			("eˣ", lambda: self._append("exp("), "Calc.TButton"),
			("0", lambda: self._append("0"), "Calc.TButton"),
			(".", lambda: self._append("."), "Calc.TButton"),
			("±", self._toggle_sign, "Calc.TButton"),
			("+", lambda: self._append("+"), "Calc.TButton"),
			("Ans", self._use_answer, "Calc.TButton"),
			("=", self._evaluate, "Accent.TButton"),
		]

		row = 1
		col = 0
		for label, command, style in buttons:
			btn = ttk.Button(container, text=label, command=command, style=style)
			btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
			col += 1
			if col == 6:
				col = 0
				row += 1

		self.bind("<Return>", lambda _event: self._evaluate())
		self.bind("<BackSpace>", lambda _event: self._backspace())
		self.bind("<Escape>", lambda _event: self._clear())

	def _append(self, value: str) -> None:
		self._expression.set(self._expression.get() + value)

	def _clear(self) -> None:
		self._expression.set("")

	def _backspace(self) -> None:
		current = self._expression.get()
		self._expression.set(current[:-1])

	def _toggle_sign(self) -> None:
		current = self._expression.get().strip()
		if not current:
			self._expression.set("-")
			return
		if current.startswith("-"):
			self._expression.set(current[1:])
		else:
			self._expression.set(f"-{current}")

	def _use_answer(self) -> None:
		if hasattr(self, "_last_answer"):
			self._append(str(self._last_answer))

	def _evaluate(self) -> None:
		raw = self._expression.get()
		if not raw.strip():
			return

		try:
			result = self._safe_eval(raw)
		except Exception:
			self._expression.set("Error")
			return

		self._last_answer = result
		self._expression.set(self._format_result(result))

	def _format_result(self, value: float) -> str:
		if isinstance(value, float) and value.is_integer():
			return str(int(value))
		return str(value)

	def _safe_eval(self, expression: str) -> float:
		expression = expression.replace("^", "**")
		expression = self._replace_factorial(expression)

		allowed = {
			"sin": math.sin,
			"cos": math.cos,
			"tan": math.tan,
			"asin": math.asin,
			"acos": math.acos,
			"atan": math.atan,
			"sqrt": math.sqrt,
			"cbrt": lambda x: x ** (1 / 3),
			"root": lambda x, n: x ** (1 / n),
			"ln": math.log,
			"log": lambda x, base=10: math.log(x, base),
			"exp": math.exp,
			"pi": math.pi,
			"e": math.e,
			"abs": abs,
			"factorial": _factorial,
		}

		return eval(expression, {"__builtins__": {}}, allowed)

	def _replace_factorial(self, expression: str) -> str:
		output = ""
		number = ""
		for char in expression:
			if char.isdigit() or char == ".":
				number += char
			elif char == "!":
				if not number:
					raise ValueError("Invalid factorial")
				output += f"factorial({number})"
				number = ""
			else:
				if number:
					output += number
					number = ""
				output += char
		if number:
			output += number
		return output


def _factorial(n: float) -> int:
	if n < 0 or not float(n).is_integer():
		raise ValueError("Invalid factorial")
	return math.factorial(int(n))


if __name__ == "__main__":
	calculator = ScientificCalculator()
	calculator.mainloop()