import tkinter as tk

def on_scroll(*args):
    text_widget.yview(*args)
    update_entry_positions()

def update_entry_positions():
    for index, entry in entries:
        bbox = text_widget.bbox(index)
        if bbox is not None:
            # Entry is visible, update position
            entry_width = entry.winfo_reqwidth()  # Get the width of the entry
            entry.place(x=bbox[0], y=bbox[1], width=entry_width)
            entry.lift()  # Ensure the entry is on top of the text widget
        else:
            # Entry is out of view, hide it
            entry.place_forget()

def on_mouse_wheel(event):
    if event.delta:  # Handle Windows and Mac scroll
        text_widget.yview_scroll(-1 * int(event.delta / 120), "units")
    else:  # Linux uses event.num
        if event.num == 4:
            text_widget.yview_scroll(-1, "units")
        elif event.num == 5:
            text_widget.yview_scroll(1, "units")
    update_entry_positions()

root = tk.Tk()

# Create Text widget and Scrollbar
text_widget = tk.Text(root, wrap='word', height=10, width=40)
scrollbar = tk.Scrollbar(root, command=on_scroll)
text_widget.config(yscrollcommand=scrollbar.set)

text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Add some text
for i in range(50):
    text_widget.insert('end', f"Line {i+1}\n")

# Create Entry widgets and place them on specific lines
entries = []
for i in range(10, 20):  # Place entries between line 10 and 20
    entry = tk.Entry(root)
    entry_width = i * 2  # Give each entry a different width for demonstration
    entry.config(width=entry_width)  # Set the width of the entry
    index = f"{i}.0"  # Line number in the Text widget
    bbox = text_widget.bbox(index)
    if bbox:
        entry.place(x=bbox[0], y=bbox[1], width=entry.winfo_reqwidth())
    entries.append((index, entry))

# Bind the mousewheel scrolling event
root.bind_all('<MouseWheel>', on_mouse_wheel)  # For Windows and MacOS
root.bind_all('<Button-4>', on_mouse_wheel)    # For Linux (scroll up)
root.bind_all('<Button-5>', on_mouse_wheel)    # For Linux (scroll down)

root.mainloop()