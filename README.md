# repo2txt

Convert any local repository into a text representation, perfect for creating context for LLMs (Large Language Models) or documentation purposes.

## Features

- Creates a tree-like visualization of your repository structure
- Includes the content of text files
- Automatically detects and skips binary files
- Configurable file size limits
- Customizable ignore patterns
- Handles virtual environments and common development directories
- Outputs in a format suitable for LLM prompts

## Installation

1. Download the script:
```bash
curl -O https://raw.githubusercontent.com/your-username/repo2txt/main/repo2txt.py
```

2. Make it executable:
```bash
chmod +x repo2txt.py
```

3. Optionally, make it available system-wide:
```bash
sudo mv repo2txt.py /usr/local/bin/repo2txt
```

## Usage

### Basic Usage

Scan the current directory:
```bash
repo2txt
```

Scan a specific directory:
```bash
repo2txt /path/to/your/repo
```

### Advanced Options

Save output to a file:
```bash
repo2txt --output repo_content.txt
```

Set maximum file size (in bytes):
```bash
repo2txt --max-size 500000
```

Add custom ignore patterns:
```bash
repo2txt --ignore "*.log" "temp/*" "*.cache"
```

View version:
```bash
repo2txt --version
```

### Default Ignore Patterns

The script automatically ignores common development-related files and directories:

- Python: `*.pyc`, `*.pyo`, `*.pyd`, `__pycache__`
- JavaScript: `node_modules`, `bower_components`
- Version Control: `.git`, `.svn`, `.hg`, `.gitignore`
- Images: `*.svg`, `*.png`, `*.jpg`, `*.jpeg`, `*.gif`
- Virtual Environments: `venv`, `.venv`, `env`, `*venv*`
- IDEs: `.idea`, `.vscode`
- System: `.DS_Store`, `Thumbs.db`
- Build: `build`, `dist`, `*.egg-info`
- Binary: `*.so`, `*.dylib`, `*.dll`

## Output Format

The script generates one big text output in the following format:

```
Repository Structure:
└── project_name
    ├── src
    │   ├── main.py
    │   └── utils
    │       └── helpers.py
    ├── tests
    │   └── test_main.py
    └── README.md

Files Content:
================================================
File: src/main.py
================================================
[file content here]

================================================
File: src/utils/helpers.py
================================================
[file content here]

...
```

## Features and Limitations

### Features
- Tree-style directory visualization
- Content extraction for text files
- Binary file detection
- Size-based file filtering
- Customizable ignore patterns
- Permission error handling

### Limitations
- Maximum directory depth: No limit (be careful with symbolic links)
- Maximum file size: Configurable via --max-size
- File types: Only text files are included; binary files are marked as [Binary file]

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
