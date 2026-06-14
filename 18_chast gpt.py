from tkinter import *

# Create window
root = Tk()
root.title("Calculator")
root.geometry("350x500")
root.resizable(False, False)

# Entry field
entry = Entry(root, font=("Arial", 24), bd=10, relief=RIDGE, justify="right")
entry.pack(fill=BOTH, ipadx=8, ipady=15, padx=10, pady=10)

# Function to insert values
def click(value):
    entry.insert(END, value)

# Function to clear screen
def clear():
    entry.delete(0, END)

# Function to calculate result
def calculate():
    try:
        expression = entry.get()
        result = eval(expression)
        entry.delete(0, END)
        entry.insert(END, str(result))
    except:
        entry.delete(0, END)
        entry.insert(END, "Error")

# Frame for buttons
frame = Frame(root)
frame.pack()

# Button layout
buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
]

# Create buttons
for row in buttons:
    row_frame = Frame(frame)
    row_frame.pack(expand=True, fill="both")

    for btn in row:
        if btn == "=":
            Button(
                row_frame,
                text=btn,
                font=("Arial", 18),
                command=calculate,
                width=5,
                height=2
            ).pack(side=LEFT, expand=True, fill="both")
        else:
            Button(
                row_frame,
                text=btn,
                font=("Arial", 18),
                command=lambda b=btn: click(b),
                width=5,
                height=2
            ).pack(side=LEFT, expand=True, fill="both")

# Clear button
Button(
    root,
    text="C",
    font=("Arial", 18),
    command=clear,
    height=2
).pack(fill="both", padx=10, pady=10)

# Run application
root.mainloop()