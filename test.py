import tkinter as tk

root = tk.Tk()
var = tk.StringVar(value="Hello, Tkinter!")

num = tk.IntVar(value=1)
not_num = tk.BooleanVar(value=False)

# Label displays the variable's value
label = tk.Label(root, textvariable=var)
label.pack()

# Change the variable's value programmatically
var.set("Updated text")
if not_num:
    print(True)
else:
    print(False)
root.mainloop()