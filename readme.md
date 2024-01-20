# File Organizer Script

This Python script provides a versatile way to organize files in a directory based on different criteria: file type, modification date, or file size. It also includes features to simulate the organization process, log file movements, and undo the last organization.

## Features

- **Organize by File Type:** Files are moved into subdirectories named after their file types.
- **Organize by Modification Date:** Files are moved into subdirectories named after their modification dates.
- **Organize by File Size:** Files are sorted into 'Small', 'Medium', and 'Large' subdirectories based on size thresholds.
- **Simulation Mode:** Allows users to simulate the organization process without moving files.
- **Logging and Undo:** Movements are logged, and users can undo the last organization.

## Requirements

- Python 3.x
- `pathlib`, `shutil`, `json`, `os`, `argparse`, `datetime` modules (usually included in standard Python installations).

## Usage

To use the script, run it from the command line with the desired options. Ensure that Python 3.x is installed on your system.

### Basic Command

```
python file_organizer.py --path [directory path] [options]
```

### Options

- `--path`: The path to the directory you want to organize.
- `--type`: Organize files by their file type.
- `--date`: Organize files by their modification date.
- `--size`: Organize files by their size.
- `--simulate`: Simulate the organization process without moving any files.
- `--undo`: Undo the last organization performed by the script.
- `--history`: Path to the log file for recording file movements (default is generated with current timestamp).
- `--small`: Upper size limit (in bytes) for a file to be considered 'Small' (default 1MB).
- `--medium`: Upper size limit for 'Medium' files (default 10MB).
- `--large`: Upper size limit for 'Large' files (default 1TB).

### Examples

- Organize a directory by file type:

  ```
  python file_organizer.py --path /your/directory --type
  ```

- Simulate organization by file size:

  ```
  python file_organizer.py --path /your/directory --size --simulate
  ```

- Undo the last organization:

  ```
  python file_organizer.py --path /your/directory --undo
  ```

## License

This script is free software; you can redistribute it and/or modify it under the terms of the MIT License. 

## Disclaimer

This software is provided 'as is', without warranty of any kind, express or implied. Use at your own risk.