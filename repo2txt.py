#!/usr/bin/env python3
import os
import argparse
from typing import Dict, List, Set
from fnmatch import fnmatch

# Default patterns to ignore
DEFAULT_IGNORE_PATTERNS = [
    '*.pyc', '*.pyo', '*.pyd', '__pycache__',  # Python
    'node_modules', 'bower_components',         # JavaScript
    '.git', '.svn', '.hg', '.gitignore',       # Version control
    '*.svg', '*.png', '*.jpg', '*.jpeg', '*.gif', # Images
    'venv', '.venv', 'env', '*venv*',          # Virtual environments (includes venv, .venv, env, venv_*, *_venv)
    '.idea', '.vscode',                        # IDEs
    '*.log', '*.bak', '*.swp', '*.tmp',       # Temporary files
    '.DS_Store',                              # macOS
    'Thumbs.db',                              # Windows
    'build', 'dist',                          # Build directories
    '*.egg-info',                             # Python egg info
    '*.so', '*.dylib', '*.dll'                # Compiled libraries
]

def is_text_file(file_path: str) -> bool:
    """Determines if a file is likely a text file based on its content."""
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
        return not bool(chunk.translate(None, bytes([7, 8, 9, 10, 12, 13, 27] + list(range(0x20, 0x100)))))
    except IOError:
        return False

def should_exclude(path: str, base_path: str, ignore_patterns: List[str]) -> bool:
    """Check if the path should be excluded based on ignore patterns."""
    rel_path = os.path.relpath(path, base_path)
    basename = os.path.basename(path)
    
    for pattern in ignore_patterns:
        # Check both the relative path and basename against the pattern
        if fnmatch(rel_path, pattern) or fnmatch(basename, pattern):
            return True
        # Handle directory patterns specifically
        if os.path.isdir(path) and (fnmatch(basename, pattern) or fnmatch(basename.lower(), pattern)):
            return True
    return False

def scan_directory(path: str, ignore_patterns: List[str], max_file_size: int) -> Dict:
    """Recursively scan directory and collect file information."""
    result = {
        "name": os.path.basename(path),
        "type": "directory",
        "size": 0,
        "children": [],
        "file_count": 0,
        "dir_count": 0
    }

    try:
        for item in sorted(os.listdir(path)):
            item_path = os.path.join(path, item)
            
            if should_exclude(item_path, path, ignore_patterns):
                continue

            if os.path.isfile(item_path):
                file_size = os.path.getsize(item_path)
                if file_size > max_file_size:
                    content = "[File too large to include]"
                else:
                    is_text = is_text_file(item_path)
                    content = open(item_path, 'r', encoding='utf-8', errors='ignore').read() if is_text else "[Binary file]"

                child = {
                    "name": item,
                    "type": "file",
                    "size": file_size,
                    "content": content
                }
                result["children"].append(child)
                result["size"] += file_size
                result["file_count"] += 1

            elif os.path.isdir(item_path):
                subdir = scan_directory(item_path, ignore_patterns, max_file_size)
                result["children"].append(subdir)
                result["size"] += subdir["size"]
                result["file_count"] += subdir["file_count"]
                result["dir_count"] += 1 + subdir["dir_count"]

    except PermissionError:
        print(f"Permission denied: {path}")

    return result

def create_tree_structure(node: Dict, prefix: str = "", is_last: bool = True) -> str:
    """Creates a tree-like string representation of the file structure."""
    tree = ""
    
    if node["name"]:
        current_prefix = "└── " if is_last else "├── "
        tree += prefix + current_prefix + node["name"] + "\n"
    
    if node["type"] == "directory":
        new_prefix = prefix + ("    " if is_last else "│   ")
        children = sorted(node["children"], key=lambda x: (x["type"] != "directory", x["name"].lower()))
        
        for i, child in enumerate(children):
            tree += create_tree_structure(child, new_prefix, i == len(children) - 1)
    
    return tree

def create_file_content_string(node: Dict, base_path: str = "") -> str:
    """Creates a formatted string of file contents with separators."""
    output = ""
    separator = "=" * 48 + "\n"
    
    if node["type"] == "file":
        rel_path = os.path.join(base_path, node["name"])
        output += separator
        output += f"File: {rel_path}\n"
        output += separator
        output += f"{node['content']}\n\n"
    elif node["type"] == "directory":
        current_path = os.path.join(base_path, node["name"]) if node["name"] else ""
        for child in sorted(node["children"], key=lambda x: x["name"].lower()):
            output += create_file_content_string(child, current_path)
    
    return output

def main():
    parser = argparse.ArgumentParser(description='Generate a text representation of a local repository')
    parser.add_argument('path', nargs='?', default='.', help='Path to the repository (default: current directory)')
    parser.add_argument('--max-size', type=int, default=100000, help='Maximum file size in bytes (default: 100000)')
    parser.add_argument('--ignore', nargs='*', help='Additional patterns to ignore')
    parser.add_argument('--output', '-o', help='Output file path (default: print to stdout)')
    
    args = parser.parse_args()
    
    # Combine default and user-provided ignore patterns
    ignore_patterns = DEFAULT_IGNORE_PATTERNS.copy()
    if args.ignore:
        ignore_patterns.extend(args.ignore)

    # Scan directory
    path = os.path.abspath(args.path)
    root_node = scan_directory(path, ignore_patterns, args.max_size)
    
    # Generate output
    output = "Repository Structure:\n"
    output += create_tree_structure(root_node)
    output += "\nFiles Content:\n"
    output += create_file_content_string(root_node)
    
    # Output results
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Output written to {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()
