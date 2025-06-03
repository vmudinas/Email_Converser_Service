#!/usr/bin/env python3
"""
PST to MBOX Converter

A batch conversion tool that converts Microsoft Outlook PST files to MBOX format
using the readpst utility. Each PST file is converted to a separate subdirectory
containing the corresponding MBOX files.

Requirements:
- readpst utility (from pst-utils package) must be installed
- Python 3.6 or higher

Usage:
    python pst_to_mbox.py <source_folder> <output_folder>

Example:
    python pst_to_mbox.py /path/to/pst_files /path/to/output
"""

import os
import subprocess
import argparse
import sys
from pathlib import Path


def convert_pst_to_mbox(src_folder, out_folder):
    """
    Convert all PST files in source folder to MBOX format in output folder.
    
    Args:
        src_folder (str): Path to folder containing PST files
        out_folder (str): Path to output folder for MBOX files
    
    Returns:
        tuple: (success_count, failed_count)
    """
    # Ensure output folder exists
    os.makedirs(out_folder, exist_ok=True)
    
    # Find all PST files in source folder
    src_path = Path(src_folder)
    if not src_path.exists():
        print(f"[ERROR] Source folder does not exist: {src_folder}")
        return 0, 0
    
    pst_files = [f for f in os.listdir(src_folder) if f.lower().endswith('.pst')]
    
    if not pst_files:
        print(f"[INFO] No PST files found in {src_folder}")
        return 0, 0
    
    print(f"[INFO] Found {len(pst_files)} PST file(s) to convert")
    
    success_count = 0
    failed_count = 0
    
    for filename in pst_files:
        src_path = os.path.join(src_folder, filename)
        # Create output subdirectory named after the PST file (without extension)
        pst_basename = os.path.splitext(filename)[0]
        out_dir = os.path.join(out_folder, pst_basename)
        
        # Ensure output subdirectory exists
        os.makedirs(out_dir, exist_ok=True)
        
        print(f"[INFO] Converting {src_path}...")
        print(f"[INFO] Output directory: {out_dir}")
        
        # Build readpst command
        # -r: recursive (process subfolders)
        # -M: output in MBOX format (rfc822)
        # -o: output directory
        cmd = ['readpst', '-r', '-M', '-o', out_dir, src_path]
        
        try:
            # Execute readpst command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
            
            if result.returncode == 0:
                print(f"[OK] Success: {src_path} → {out_dir}")
                if result.stdout.strip():
                    print(f"[INFO] readpst output: {result.stdout.strip()}")
                success_count += 1
            else:
                print(f"[ERROR] Failed to convert {src_path}")
                print(f"[ERROR] Return code: {result.returncode}")
                if result.stderr.strip():
                    print(f"[ERROR] Error output: {result.stderr.strip()}")
                if result.stdout.strip():
                    print(f"[ERROR] Standard output: {result.stdout.strip()}")
                failed_count += 1
                
        except subprocess.TimeoutExpired:
            print(f"[ERROR] Timeout expired while converting {src_path}")
            failed_count += 1
        except FileNotFoundError:
            print(f"[ERROR] readpst command not found. Please install pst-utils package.")
            print(f"[ERROR] On Ubuntu/Debian: sudo apt install pst-utils")
            failed_count += 1
        except Exception as e:
            print(f"[ERROR] Unexpected error converting {src_path}: {e}")
            failed_count += 1
    
    return success_count, failed_count


def main():
    """Main function to parse arguments and run conversion."""
    parser = argparse.ArgumentParser(
        description='Batch convert PST files to MBOX format.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /home/user/pst_files /home/user/mbox_output
  %(prog)s "C:\\PST Files" "C:\\MBOX Output"

This tool requires the 'readpst' utility to be installed.
On Ubuntu/Debian: sudo apt install pst-utils
        """
    )
    
    parser.add_argument(
        'src_folder',
        help='Source folder containing PST files'
    )
    
    parser.add_argument(
        'out_folder', 
        help='Output folder for MBOX files'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not os.path.isdir(args.src_folder):
        print(f"[ERROR] Source folder does not exist or is not a directory: {args.src_folder}")
        sys.exit(1)
    
    print(f"[INFO] Starting PST to MBOX conversion")
    print(f"[INFO] Source folder: {args.src_folder}")
    print(f"[INFO] Output folder: {args.out_folder}")
    print("-" * 60)
    
    # Run conversion
    success_count, failed_count = convert_pst_to_mbox(args.src_folder, args.out_folder)
    
    print("-" * 60)
    print(f"[SUMMARY] Conversion completed")
    print(f"[SUMMARY] Successfully converted: {success_count}")
    print(f"[SUMMARY] Failed conversions: {failed_count}")
    print(f"[SUMMARY] Total PST files processed: {success_count + failed_count}")
    
    if failed_count > 0:
        print(f"[WARNING] {failed_count} file(s) failed to convert. Check error messages above.")
        sys.exit(1)
    else:
        print(f"[INFO] All files converted successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()