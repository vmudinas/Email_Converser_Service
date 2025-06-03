# Email Converter Service

A Python-based service for batch converting Microsoft Outlook PST files to MBOX format using the `readpst` utility.

## Features

- **Batch Processing**: Convert all PST files in a specified folder
- **Robust Handling**: Process large files one at a time to avoid memory issues
- **Organized Output**: Each PST file creates its own subdirectory with MBOX files
- **Comprehensive Logging**: Detailed success/failure reporting with error messages
- **Command-line Interface**: Easy to use with command-line arguments
- **Error Recovery**: Continues processing even if individual files fail

## Requirements

- Python 3.6 or higher
- `readpst` utility (from `pst-utils` package)

### Installing Dependencies

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install pst-utils python3
```

#### CentOS/RHEL/Fedora
```bash
sudo yum install libpst-tools python3
# or for newer versions:
sudo dnf install libpst-tools python3
```

## Usage

### Basic Usage
```bash
python3 pst_to_mbox.py <source_folder> <output_folder>
```

### Examples
```bash
# Convert all PST files from /home/user/pst_files to /home/user/mbox_output
python3 pst_to_mbox.py /home/user/pst_files /home/user/mbox_output

# Windows example
python pst_to_mbox.py "C:\PST Files" "C:\MBOX Output"
```

### Help
```bash
python3 pst_to_mbox.py --help
```

## Output Structure

For each PST file, the tool creates a subdirectory in the output folder:

```
output_folder/
├── email_archive_2023/     # From email_archive_2023.pst
│   ├── Inbox
│   ├── Sent Items
│   └── ...
├── personal_emails/        # From personal_emails.pst
│   ├── Inbox
│   ├── Drafts
│   └── ...
```

## How It Works

1. **Scans** the source folder for `.pst` files
2. **Creates** an output subdirectory for each PST file
3. **Executes** `readpst -r -M -o <output_dir> <pst_file>` for each file
4. **Logs** progress and any errors encountered
5. **Reports** a summary of successful and failed conversions

## Troubleshooting

### Common Issues

1. **readpst not found**
   - Install the `pst-utils` package (see Requirements section)
   - Ensure `readpst` is in your system PATH

2. **Permission errors**
   - Check read permissions on source PST files
   - Check write permissions on output directory

3. **Large file processing**
   - The tool processes files one at a time to avoid memory issues
   - Very large PST files may take considerable time

### Testing Installation

You can test if `readpst` is properly installed:
```bash
readpst -V
```

## Advanced Features

- **Timeout Protection**: Each conversion has a 1-hour timeout to prevent hanging
- **Recursive Processing**: Processes all subfolders within PST files
- **MBOX Format**: Outputs standard RFC822 MBOX format for compatibility
- **Error Isolation**: One failed conversion doesn't stop the entire batch

## License

This project is open source. Please check the repository for license details.
