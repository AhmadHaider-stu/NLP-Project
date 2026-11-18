# Import the tkinter lib
import tkinter as tk
from tkinter import ttk
# initialize TKinter app
root = tk.Tk()
# IDK random name
root.title("AA GUI")

# Grid funtion : To locate the element on the screen
# the screen divided into row and columns 


# 1) Side list of options (left side)
options = tk.Listbox(root, height=10, exportselection=False)
for item in ["Option A", "Option B", "Option C", "Option D"]:
    options.insert(tk.END, item)
options.grid(row=0, column=0, rowspan=4, padx=10, pady=10)

# 2) Text input 
entry = tk.Entry(root, width=100)
entry.grid(row=0, column=5, padx=10, pady=10)

# Numbers 1-10 dropdown
number = ttk.Combobox(root, values=list(range(1, 11)),width=5)
number.current(0)
number.grid(row=0, column=6, padx=10, pady=5, sticky="w")

# 3) Output under the text input
output = tk.Label(root, text="", fg="blue")
output.grid(row=1, column=5, padx=10, pady=5, sticky="w")


def show():
    global side_option, text_value, number_value

    sel = options.curselection()
    side_option = options.get(sel[0]) if sel else "Option A"   # str
    text_value = entry.get()                            # str
    number_value = int(number.get())                    # int
   
    

tk.Button(root, text="Search", command=show).grid(row=0, column=5, padx=10, pady=5, sticky="w")

root.mainloop()