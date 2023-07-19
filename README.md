# twins

## Duplicate Video File Finder

The **Duplicate Video File Finder** is a Python application that helps you find duplicate video files in one or more directories. It uses the [MoviePy](https://zulko.github.io/moviepy/) library to efficiently calculate the MD5 hash of the first 5 seconds of each video file and identifies duplicates based on the hash values.

### Features

- Allows you to select one or more directories to search for duplicate video files.
- Supports searching for duplicate video files in subdirectories as well (optional).
- Displays the duplicate video files and their locations in the user interface.
- Provides an option to save the results to a text file.
- Utilizes a progress bar to indicate the ongoing search process.

### Prerequisites

Before running the Duplicate Video File Finder application, make sure you have the following requirements installed:

- Python 3.x (Tested with Python 3.6+)
- MoviePy library (Install with `pip install moviepy`)

### Usage

1. Clone or download the source code from the [GitHub repository](https://github.com/your-username/duplicate_video_finder).
2. Install the required libraries using `pip`:

```bash
pip install moviepy
```
3.  Run the Python script to start the Duplicate Video File Finder application:
```bash
`python video.py`
```

4.  The application window will open, and you can start using the tool.

### User Interface

The user interface of the Duplicate Video File Finder application consists of the following elements:

* **"Select Directories"**: Use this button to select one or more directories from which you want to search for duplicate video files.
    
* **"Search Subfolders"**: If checked, the application will search for duplicate video files in the subdirectories of the selected directories.
    
* **"Find Duplicates"**: Click this button to start the search for duplicate video files based on your selected criteria.
    
* **"Save Output to File"**: Check this box if you want to save the duplicate video file results to a text file.
    
* **"Results"**: The text box displays the found duplicate video files along with their locations.
    

### How It Works

1.  The user selects one or more directories and specifies whether to search for duplicate video files in subfolders.
    
2.  The application uses the `moviepy` library to calculate the MD5 hash of the first 5 seconds of each video file in the selected directories.
    
3.  The application identifies duplicate video files based on the hash values.
    
4.  If the "Save Output to File" checkbox is checked, the application saves the duplicate video file results to a text file.
    
5.  The results are displayed in the user interface, showing the duplicate video files and their locations.
    

### Performance Optimization

The Duplicate Video File Finder application is optimized to handle large video files more efficiently:

* **Batch Processing**: The application processes video files in small chunks, improving performance for large files.
    
* **Multithreading**: The application uses multithreading to handle the search process separately, preventing the user interface from freezing during the search.
    
* **Progress Bar**: The application displays a progress bar to indicate ongoing processing without affecting performance.
    

### Logging

The application logs information and debug messages to both the console and a log file named "duplicate\_file\_finder.log" in the same directory as the script. The log level is set to INFO for the console and DEBUG for the log file.

### Note

* The application currently supports video files with extensions `.mp4`, `.avi`, `.mkv`, `.mov`, and `.wmv`. You can add more supported extensions as needed.
    
* The MD5 hash is used for efficiency, but keep in mind that it is not cryptographically secure. For cryptographic purposes, consider using a stronger hash algorithm.
    

### License

The Duplicate Video File Finder application is licensed under the <ins>MIT License</ins>.

### Author

The application was created by <ins>Your Name</ins>.

### Contributing

Contributions to the project are welcome. To contribute, please fork the repository and submit a pull request.