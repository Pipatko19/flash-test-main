import tkinter as tk
from tkinter import scrolledtext, font
from ttkbootstrap import Style

def create_font_from_style(style, widget="TLabel"):
    # Get font description from ttk style, e.g., "garamond 13"
    font_description = style.lookup(widget, "font")
    if font_description:
        # Split the font description (e.g., "garamond 13" -> family="garamond", size=13)
        font_parts = font_description.split()
        font_family = font_parts[0]
        font_size = int(font_parts[1])
        
        # Create and return a new Font object with this family and size
        return font.Font(family=font_family, size=font_size)
    else:
        # Fallback if style lookup fails
        return font.Font(size=12)

def get_word_pixel_width(word, font_obj):
    # Calculate width of the word based on the font object
    return font_obj.measure(word)

def create_entry_on_word():
    text_content = scrolled_text.get("1.0", "end-1c")
    words = text_content.split()
    
    # Create a default font object from the ttk style
    default_font = create_font_from_style(style)
    
    for word in words:
        start_index = scrolled_text.search(word, "1.0", tk.END)
        
        if start_index:
            entry_width_px = get_word_pixel_width(word, default_font)
            entry_width_chars = round(entry_width_px / default_font.measure('0'))
            
            entry = tk.Entry(root, width=entry_width_chars)
            entry.insert(0, word)
            entry.pack()  # Replace with positioning as needed

root = tk.Tk()
root.geometry("400x300")

# Initialize ttkbootstrap style
style = Style("cosmo")
scrolled_text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
scrolled_text.pack(expand=True, fill="both")
scrolled_text.insert("1.0", "This is a sample text. Press the button to create entries over each word.")

button = tk.Button(root, text="Create Entry on Word", command=create_entry_on_word)
button.pack()

root.mainloop()