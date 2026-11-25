import tkinter as tk
import ast
import operator
operations = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv
}
unary_operations = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg
}
root = tk.Tk()
root.title("Calculator")
root.geometry("450x600")
root.configure(bg="#1e1e2e")
display = tk.Entry(root, font=("Arial", 28),bg="#313244",fg="#ffffff",insertbackground="#ffffff",bd=0 ,justify="right")
display.pack(pady=25, padx=48,ipady=20,fill="x")
button_frame=tk.Frame(root,bg="#1e1e2e")
button_frame.pack()
calculation_done=False
error_shown = False
history=[]
def button_click(value):
    global calculation_done,error_shown
    if calculation_done or error_shown:
        if str(value) in "0123456789.":
          display.delete(0,tk.END)
        calculation_done=False
        error_shown = False

    display.insert(tk.END,str(value))

def clear_display():
    global calculation_done
    display.delete(0,tk.END)
    calculation_done=False
def safe_evaluate(expression):
    if len(expression) > 100:
        raise ValueError("Expression too long")
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        elif isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)

            operation = operations.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operator")

            return operation(left, right)
        elif isinstance(node, ast.UnaryOp):
            operation = unary_operations.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported unary operator")

            return operation(evaluate(node.operand))

        else:
            raise ValueError("Invalid expression")

    return evaluate(tree.body)
def calculate():
    global calculation_done,error_shown
    expression=display.get()
    try:
        result = safe_evaluate(expression)
        history.append(f"{expression} = {result}")
        display.delete(0,tk.END)
        display.insert(tk.END,str(result))
        calculation_done=True
        error_shown=False
    except ZeroDivisionError:
        display.delete(0,tk.END)
        display.insert(tk.END,"Cannot divide by zero")
        calculation_done=False
        error_shown=True
    except (SyntaxError,ValueError,NameError):
        display.delete(0,tk.END)
        display.insert(tk.END,"Invalid Expression")
        calculation_done=False
        error_shown=True

def backspace():
    global calculation_done,error_shown
    current=display.get()
    if current:
        display.delete(len(current)-1,tk.END)
    calculation_done=False
    error_shown=False

def keyboard_input(event):
    key = event.char

    if event.keysym in ("Return", "KP_Enter"):
        calculate()

    elif event.keysym == "BackSpace":
        backspace()

    elif event.keysym == "Escape":
        clear_display()

    elif key and key in "0123456789.+*/-()":
        button_click(key)

def show_history():
    history_window=tk.Toplevel(root)
    history_window.title("History")
    history_window.geometry("350x400")
    history_window.configure(bg="#1e1e2e")
    history_list=tk.Listbox(
        history_window,
        font=("Arial", 14),
        bg="#313244",
        fg="white",
        bd=0
    )
    history_list.pack(fill="both",expand=True,padx=5,pady=5)
    for calculation in history:
        history_list.insert(tk.END,calculation)

def add_hover_effect(button,normal_color,hover_color):
    button.bind("<Enter>",lambda event: button.config(bg=hover_color))
    button.bind("<Leave>",lambda event:button.config(bg=normal_color))
numbers=[7,8,9,4,5,6,1,2,3]
for row in range(3):
    for col in range(3):
        num=numbers[row*3+col]
        button = tk.Button(
            button_frame,
            text=num,
            font=("Arial", 18, "bold"),
            width=5,
            height=2,
            bg="#313244",
            fg="white",
            activebackground="#45475a",
            activeforeground="white",
            bd=0,
            command=lambda n=num: button_click(n)
        )

        button.grid(row=row, column=col, padx=4, pady=4)
        add_hover_effect(button, "#313244", "#45475A")

operators=["+","-","*","/"]
for row ,op in enumerate(operators):
    button=tk.Button(button_frame, text=op, font=("Arial", 20,"bold"), width=5, height=2,bg="#233F8F",fg="white",activebackground="#2563EB",activeforeground="white",bd=0,command= lambda o=op:button_click(o)
                     )
    button.grid(row=row,column=3,padx=4,pady=4)
    add_hover_effect(button, "#233F8F", "#3659B5")

zero =tk.Button(button_frame, text="0", width=5, bg="#313244", fg="white", activebackground="#45475a",
                activeforeground="white", bd=0, font=("Arial", 18, "bold"), height=2, command=lambda: button_click(0))
zero.grid(row=3,column=0)
add_hover_effect(zero, "#313244", "#45475A")

equal=tk.Button(button_frame,
                text="=",
                bg="#2563EB",
                fg="#FFFFFF",
                activebackground="#3B82F6",
                activeforeground="white",
                bd=0,
                font=("Arial", 18, "bold"),
                width=5,
                height=2,
                command=calculate)
equal.grid(row=3,column=1,padx=4,pady=4)
add_hover_effect(equal, "#2563EB", "#3B82F6")

clear=tk.Button(button_frame,
                text="C",
                bg="#493078",
                fg="white",
                activebackground="#7E22CE",
                activeforeground="white",
                bd=0,
                font=("Arial", 18, "bold"),
                width=5,
                height=2,
                command=clear_display)
clear.grid(row=3,column=2,padx=4,pady=4)
add_hover_effect(clear, "#493078", "#64449A")

decimal=tk.Button(button_frame,
                  text=".",
                  bg="#313244",
                  fg="white",
                  activebackground="#45475a",
                  activeforeground="white",
                  bd=0,
                  font=("Arial", 18, "bold"),
                  width=5,
                  height=2,
                  command=lambda: button_click("."))
decimal.grid(row=4,column=0,padx=4,pady=4)

backspace_button=tk.Button(button_frame,
                           text="⌫",
                           bg="#313244",
                           fg="white",
                           activebackground="#45475a",
                           activeforeground="white",
                           bd=0,
                           font=("Arial", 18, "bold"),
                           width=5,
                           height=2,
                           command=backspace)
backspace_button.grid(row=4,column=1)
history_button = tk.Button(
    button_frame,
    text="History",
    font=("Arial", 12, "bold"),
    width=12,
    height=2,
    bg="#493078",
    fg="white",
    activebackground="#7E22CE",
    activeforeground="white",
    bd=0,
    command=show_history
)

history_button.grid(row=4, column=2, columnspan=2, padx=4, pady=4, sticky="nsew")

add_hover_effect(history_button, "#493078", "#64449A")
button_frame.grid_rowconfigure(5, minsize=80)

root.bind("<Key>",keyboard_input)
root.mainloop()