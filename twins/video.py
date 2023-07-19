import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import threading
from tkinter import ttk


def setup_logger():
    logger = logging.getLogger("duplicate_file_finder")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Create a file handler
    fh = logging.FileHandler("duplicate_file_finder.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


# Define the logger globally
logger = setup_logger()


def video_file_hash(filepath):
    # Calculate the MD5 hash of the first 5 seconds of the video file
    try:
        chunk_size = 4096
        hashobj = hashlib.md5()
        total_chunks = 5 * 25  # 25 frames per second for 5 seconds
        current_chunk = 0

        with open(filepath, "rb") as f:
            for _ in range(total_chunks):
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hashobj.update(chunk)
                current_chunk += 1
                update_progress(current_chunk, total_chunks)

        return hashobj.hexdigest()
    except Exception as e:
        print(f"Error while hashing file {filepath}: {e}")
        return None


def find_duplicate_video_files(directories, search_subfolders=True):
    duplicate_files = {}

    for directory in directories:
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)

                # Check if the file is a video file (you can add more video file extensions if needed)
                if filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv')):
                    filehash = video_file_hash(filepath)

                    if filehash:
                        if filehash in duplicate_files:
                            duplicate_files[filehash].append(filepath)
                        else:
                            duplicate_files[filehash] = [filepath]

    # Filter out non-duplicate files
    duplicate_files = {hashval: filelist for hashval, filelist in duplicate_files.items() if len(filelist) > 1}

    return duplicate_files


def delete_file(filepath):
    try:
        os.remove(filepath)
        logger.info(f"File deleted: {filepath}")
    except Exception as e:
        logger.exception(f"Error deleting file: {filepath} exception {e}")


def browse_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        directory_listbox.insert(tk.END, selected_directory)


def update_progress(current, total):
    progress_value = int((current / total) * 100)
    progress_bar["value"] = progress_value
    percentage_label.config(text=f"{progress_value}%")
    app.update_idletasks()


def save_results_to_file(duplicate_files):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w") as f:
                for i, (filehash, filelist) in enumerate(duplicate_files.items(), start=1):
                    f.write(f"{i}. Hash: {filehash}\n")
                    for filepath in filelist:
                        f.write(f"   {filepath}\n")
                    f.write("\n")
            messagebox.showinfo("Save Complete", "Duplicate file results have been saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")


def find_duplicates():
    global logger, subfolders_var, progress_bar, save_checkbox

    selected_directories = list(directory_listbox.get(0, tk.END))
    if not selected_directories:
        messagebox.showwarning("Warning", "Please select one or more directories.")
        return

    search_subfolders = subfolders_var.get()
    save_to_file = save_checkbox_var.get()

    # Logging: Starting the search
    logger.info("Starting search for duplicate files.")
    logger.debug(f"Selected directories: {selected_directories}")
    logger.debug(f"Search in subfolders: {search_subfolders}")

    # Disable the buttons while searching is in progress
    browse_button["state"] = tk.DISABLED
    find_button["state"] = tk.DISABLED

    # Create a rotating wheel (indeterminate progress bar)
    progress_bar = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, mode="indeterminate")
    progress_bar.pack(fill=tk.X, padx=10, pady=5)
    progress_bar.start()

    def search_and_update_progress():
        duplicate_files = {}

        for directory in selected_directories:
            # Logging: Processing the directory
            logger.info(f"Processing directory: {directory}")

            # Actual file processing using os.walk()
            current_duplicates = find_duplicate_video_files([directory], search_subfolders)

            if current_duplicates:
                duplicate_files.update(current_duplicates)

        if duplicate_files:
            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)
            for i, (filehash, filelist) in enumerate(duplicate_files.items(), start=1):
                result_text.insert(tk.END, f"{i}. Hash: {filehash}\n")
                for filepath in filelist:
                    result_text.insert(tk.END, f"   {filepath}\n")
                result_text.insert(tk.END, "\n")
            result_text.config(state=tk.DISABLED)

            # Logging: Duplicate files found
            logger.info(f"Found {len(duplicate_files)} duplicate files.")
            if save_to_file:
                save_results_to_file(duplicate_files)
        else:
            logger.info("No duplicate files found.")

        # Re-enable the buttons and stop the rotating wheel after search is completed
        browse_button["state"] = tk.NORMAL
        find_button["state"] = tk.NORMAL
        progress_bar.stop()
        progress_bar.pack_forget()  # Remove the progress bar from the GUI

    # Start the search process in a separate thread
    search_thread = threading.Thread(target=search_and_update_progress)
    search_thread.start()


def delete_selected_files():
    global logger
    selected_indices = result_text.tag_ranges(tk.SEL)
    if not selected_indices:
        messagebox.showwarning("Warning", "Please select one or more files to delete.")
        return

    for start_index, end_index in zip(selected_indices[::2], selected_indices[1::2]):
        original_path, duplicate_path = result_text.get(start_index, end_index).splitlines()
        original_path = original_path.split("Original: ")[-1].strip()
        duplicate_path = duplicate_path.split("Duplicate: ")[-1].strip()

        if original_var.get():
            delete_file(original_path)
        if duplicate_var.get():
            delete_file(duplicate_path)


def unselect_directory():
    selected_indices = directory_listbox.curselection()
    if selected_indices:
        directory_listbox.delete(selected_indices[-1])


app = tk.Tk()
app.title("Duplicate Video File Finder")

# Create the main frame
main_frame = ttk.Frame(app)
main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Get the screen dimensions for improved responsiveness
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app_width = int(screen_width * 0.6)
app_height = int(screen_height * 0.8)

# Set the application size
app.geometry(f"{app_width}x{app_height}")

# Create a main frame to contain all the widgets
main_frame = ttk.Frame(app)
main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# # Create the main frame
# main_frame = ttk.Frame(app)
# main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Style the widgets using ttk
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), foreground="#333")
style.configure("TCheckbutton", font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12), foreground="#333")
style.configure("TListbox", font=("Helvetica", 12))
style.configure("TText", font=("Courier New", 12))

# Listbox and scrollbar for directories
directory_listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, height=5)
directory_listbox.pack(expand=True, fill=tk.BOTH)
scrollbar = tk.Scrollbar(main_frame, command=directory_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
directory_listbox.config(yscrollcommand=scrollbar.set)

# Buttons frame
buttons_frame = ttk.Frame(main_frame)
buttons_frame.pack(pady=5, fill=tk.X)

# Buttons
browse_button = ttk.Button(buttons_frame, text="Browse", command=browse_directory)
browse_button.pack(side=tk.LEFT, padx=5)

find_button = ttk.Button(buttons_frame, text="Find Duplicates", command=find_duplicates)
find_button.pack(side=tk.LEFT, padx=5)

# Separator
separator = ttk.Separator(main_frame, orient=tk.HORIZONTAL)
separator.pack(fill=tk.X, pady=10)

# Text frame
text_frame = ttk.Frame(main_frame)
text_frame.pack(expand=True, fill=tk.BOTH)

# Text widget for displaying results
result_text = tk.Text(text_frame, wrap=tk.WORD, state=tk.DISABLED)
result_text.pack(expand=True, fill=tk.BOTH)
scrollbar_text = tk.Scrollbar(text_frame, command=result_text.yview)
scrollbar_text.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar_text.set)

# Checkbox frame
checkbox_frame = ttk.Frame(main_frame)
checkbox_frame.pack(pady=5, fill=tk.X)

# Checkboxes
original_var = tk.BooleanVar()
original_checkbox = ttk.Checkbutton(checkbox_frame, text="Delete Original", variable=original_var)
original_checkbox.pack(side=tk.LEFT, padx=5)

duplicate_var = tk.BooleanVar()
duplicate_checkbox = ttk.Checkbutton(checkbox_frame, text="Delete Duplicate", variable=duplicate_var)
duplicate_checkbox.pack(side=tk.LEFT, padx=5)

subfolders_var = tk.BooleanVar()  # Add the subfolders_var
subfolders_checkbutton = ttk.Checkbutton(checkbox_frame, text="Search in subfolders", variable=subfolders_var)
subfolders_checkbutton.pack(side=tk.LEFT, padx=5)

# Buttons frame for delete and unselect
delete_frame = ttk.Frame(main_frame)
delete_frame.pack(pady=5, fill=tk.X)

delete_selected_button = ttk.Button(delete_frame, text="Delete Selected", command=delete_selected_files)
delete_selected_button.pack(side=tk.LEFT, padx=5)

unselect_button = ttk.Button(delete_frame, text="Unselect Directory", command=unselect_directory)
unselect_button.pack(side=tk.LEFT, padx=5)

# # Progress bar
# progress_bar = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, mode="determinate")
# progress_bar.pack(fill=tk.X, padx=10, pady=5)
#
# Percentage label
percentage_label = ttk.Label(main_frame, text="0%")
percentage_label.pack(pady=5)

# Save results to file checkbox
save_checkbox_var = tk.IntVar()
save_checkbox = ttk.Checkbutton(main_frame, text="Save Output to File", variable=save_checkbox_var)
save_checkbox.pack(pady=5)

app.mainloop()
