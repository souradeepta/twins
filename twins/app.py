import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox


def file_hash(filepath):
    """Calculate the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def find_duplicate_files(directory):
    """Find duplicate files in a given directory and its subdirectories."""
    file_hashes = {}
    duplicate_files = []

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_hash_value = file_hash(filepath)

            if file_hash_value in file_hashes:
                duplicate_files.append((file_hashes[file_hash_value], filepath))
            else:
                file_hashes[file_hash_value] = filepath

    return duplicate_files


def browse_directory():
    """Open a directory selection dialog."""
    selected_directory = filedialog.askdirectory()
    directory_var.set(selected_directory)


def find_duplicates():
    """Find and display duplicate files."""
    directory = directory_var.get()
    if not directory:
        messagebox.showwarning("Warning", "Please select a directory.")
        return

    duplicate_files = find_duplicate_files(directory)

    if duplicate_files:
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        for i, (original, duplicate) in enumerate(duplicate_files, start=1):
            result_text.insert(tk.END, f"{i}. Original: {original}\n")
            result_text.insert(tk.END, f"   Duplicate: {duplicate}\n\n")
        result_text.config(state=tk.DISABLED)
    else:
        messagebox.showinfo("Info", "No duplicate files found.")


def save_results_to_file():
    """Save the results to a user-selected file."""
    results = result_text.get("1.0", tk.END)
    if not results.strip():
        messagebox.showwarning("Warning", "No results to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not file_path:
        return

    try:
        with open(file_path, "w") as file:
            file.write(results)
        messagebox.showinfo("Info", "Results saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the file:\n{e}")


app = tk.Tk()
app.title("Duplicate File Finder")
app.geometry("500x400")

directory_var = tk.StringVar()

label = tk.Label(app, text="Select a directory to search for duplicate files:")
label.pack(pady=10)

browse_button = tk.Button(app, text="Browse", command=browse_directory)
browse_button.pack()

directory_entry = tk.Entry(app, textvariable=directory_var, width=40)
directory_entry.pack(pady=10)

find_button = tk.Button(app, text="Find Duplicates", command=find_duplicates)
find_button.pack()

result_text = tk.Text(app, wrap=tk.WORD, state=tk.DISABLED)
result_text.pack(pady=10)

save_button = tk.Button(app, text="Save Results", command=save_results_to_file)
save_button.pack()

app.mainloop()
