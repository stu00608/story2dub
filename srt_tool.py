#!/usr/bin/env python3
"""
SRT Tool - A command-line utility for manipulating SRT subtitle files.

This script provides various functions to modify SRT (SubRip Subtitle) files.
Current features include:
1. Shifting timestamps in SRT files forward or backward.

Usage:
    python srt_tool.py <command> [options]

Available commands:
    shift - Shift subtitle timestamps

For more information on each command, use:
    python srt_tool.py <command> --help

Author: [Your Name]
Version: 1.0
Date: [Current Date]
"""

import argparse
import re
import os
from datetime import datetime, timedelta

def parse_time(time_str):
    """
    Parse a timestamp string into a datetime object.

    Args:
        time_str (str): A timestamp string in the format 'HH:MM:SS,mmm'.

    Returns:
        datetime.datetime: A datetime object representing the parsed time.
    """
    return datetime.strptime(time_str, '%H:%M:%S,%f')

def format_time(dt):
    """
    Format a datetime object into a timestamp string.

    Args:
        dt (datetime.datetime): A datetime object to be formatted.

    Returns:
        str: A formatted timestamp string in the format 'HH:MM:SS,mmm'.
    """
    return dt.strftime('%H:%M:%S,%f')[:-3]

def shift_timestamp(timestamp, shift_delta, negative=False):
    """
    Shift a single timestamp by the specified delta.

    Args:
        timestamp (str): The original timestamp string.
        shift_delta (datetime.timedelta): The amount of time to shift.
        negative (bool): If True, shift backward; if False, shift forward.

    Returns:
        str: The shifted timestamp string.
    """
    time = parse_time(timestamp)
    if negative:
        shifted_time = time - shift_delta
        if shifted_time < datetime.min.time():
            return '00:00:00,000'
    else:
        shifted_time = time + shift_delta
    return format_time(shifted_time)

def shift_subtitles(file_path, hours, minutes, seconds, negative=False, output_path=None):
    """
    Shift all subtitles in an SRT file by the specified amount of time.

    Args:
        file_path (str): Path to the input SRT file.
        hours (int): Number of hours to shift.
        minutes (int): Number of minutes to shift.
        seconds (int): Number of seconds to shift.
        negative (bool): If True, shift backward; if False, shift forward.
        output_path (str, optional): Path to save the output SRT file. If not provided,
                                     the original file will be overwritten.

    This function reads the input SRT file, shifts all timestamps, and writes the
    result to either a new file or replaces the original file.
    """
    shift_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    def replace_timestamp(match):
        start, end = match.groups()
        new_start = shift_timestamp(start, shift_delta, negative)
        new_end = shift_timestamp(end, shift_delta, negative)
        return f"{new_start} --> {new_end}"
    
    shifted_content = re.sub(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', replace_timestamp, content)
    
    if output_path:
        # Ensure the output file has .srt extension
        output_path = os.path.splitext(output_path)[0] + '.srt'
    else:
        # If no output path is specified, replace the original file
        output_path = file_path
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(shifted_content)
    
    print(f"Shifted subtitles saved to: {output_path}")

def main():
    """
    Main function to handle command-line interface and dispatch commands.

    This function sets up the argument parser, defines the available commands
    and their respective options, and calls the appropriate function based on
    the user's input.
    """
    parser = argparse.ArgumentParser(description="SRT Tool - A command-line tool for manipulating SRT subtitle files.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Shift command
    shift_parser = subparsers.add_parser('shift', help='Shift subtitle timestamps')
    shift_parser.add_argument('file', help='Path to the input SRT file')
    shift_parser.add_argument('--hours', type=int, default=0, help='Number of hours to shift')
    shift_parser.add_argument('--minutes', type=int, default=0, help='Number of minutes to shift')
    shift_parser.add_argument('--seconds', type=int, default=0, help='Number of seconds to shift')
    shift_parser.add_argument('--minus', action='store_true', help='Shift backwards instead of forwards')
    shift_parser.add_argument('--output', help='Path to the output SRT file (optional)')

    args = parser.parse_args()

    if args.command == 'shift':
        shift_subtitles(args.file, args.hours, args.minutes, args.seconds, args.minus, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()