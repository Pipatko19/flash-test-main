import tkinter as tk
from tkinter import messagebox

class BlacklistApp:
    def __init__(self, master):
        self.master = master
        master.title("Blacklist Manager")

        self.blacklist = []

        # Entry widget for new blacklist word
        self.word_entry = tk.Entry(master, width=30)
        self.word_entry.pack(pady=10)

        # Add button
        self.add_button = tk.Button(master, text="Add", command=self.add_word)
        self.add_button.pack(pady=5)

        # Listbox to display blacklist words
        self.listbox = tk.Listbox(master, selectmode=tk.SINGLE, width=30)
        self.listbox.pack(pady=10)

        # Remove button
        self.remove_button = tk.Button(master, text="Remove", command=self.remove_word)
        self.remove_button.pack(pady=5)

    def add_word(self):
        word = self.word_entry.get().strip()
        if word and word not in self.blacklist:
            self.blacklist.append(word)
            self.listbox.insert(tk.END, word)
            self.word_entry.delete(0, tk.END)  # Clear the entry
        else:
            messagebox.showwarning("Warning", "Word is empty or already in the blacklist.")

    def remove_word(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            word = self.listbox.get(selected_index)
            self.blacklist.remove(word)
            self.listbox.delete(selected_index)
        else:
            messagebox.showwarning("Warning", "Select a word to remove.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlacklistApp(root)
    root.mainloop()