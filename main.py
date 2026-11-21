# Import the tkinter lib
import tkinter as tk
from tkinter import ttk
from preprocessing import func
from tkinter import scrolledtext
# initialize TKinter app
root = tk.Tk()
# IDK random name
root.title("AA GUI")

# Grid funtion : To locate the element on the screen
# the screen divided into row and columns 


# 1) Side list of options (left side)
options = tk.Listbox(root, height=10, exportselection=False)
for item in ["IMDB_reviews", "hotel_reviews", "food_reviews"]:
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
output = scrolledtext.ScrolledText(root, width=100, height=15, wrap=tk.WORD, fg="blue")
output.grid(row=1, column=5, padx=10, pady=5, sticky="w")


def show():
    global side_option, text_value, number_value

    sel = options.curselection()
    side_option = options.get(sel[0]) if sel else "IMDB_reviews" 
    text_value = entry.get()                            
    number_value = int(number.get())    
    result = func(number_value, side_option, text_value)
    output.delete("1.0", tk.END)
    output.insert(tk.END, result)    
   
    

tk.Button(root, text="Search", command=show).grid(row=0, column=8, padx=10, pady=5, sticky="w")

root.mainloop()