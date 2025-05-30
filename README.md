# Git.py - Simple Version Control System

A lightweight, Python-based implementation of core Git functionality for educational purposes and basic version control needs.

## Features

- **Repository Initialization**: Create new Git repositories
- **File Staging**: Add files to the staging area
- **Commit Creation**: Create commits with messages and timestamps
- **Commit History**: View commit logs with full history
- **Status Checking**: See what files are staged for commit
- **Diff Visualization**: View changes between commits with colored output
- **SHA-1 Hashing**: Content-addressable storage using SHA-1 hashes

## Installation

No external dependencies required - uses only Python standard library.

```bash
# Make the script executable
chmod +x git.py
```

## Usage

### Initialize a Repository
```bash
python git.py init
```
Creates a `.git` directory with the necessary structure for version control.

### Add Files to Staging Area
```bash
python git.py add <filename>
```
Stages a file for the next commit. The file content is hashed and stored in the objects directory.

### Create a Commit
```bash
python git.py commit -m "Your commit message"
```
Creates a new commit with all staged files and the provided message.

### View Commit History
```bash
python git.py log
```
Displays the commit history in reverse chronological order, showing commit hashes, timestamps, and messages.

### Check Repository Status
```bash
python git.py status
```
Shows which files are currently staged for commit.

### View Commit Changes
```bash
python git.py show <commit-hash>
```
Displays the diff for a specific commit, showing what changed compared to its parent commit.

## Examples

```bash
# Initialize a new repository
python git.py init

# Add a file
echo "Hello, World!" > hello.txt
python git.py add hello.txt

# Check status
python git.py status

# Create a commit
python git.py commit -m "Add hello.txt"

# View history
python git.py log

# Modify and add the file again
echo "Hello, Git!" > hello.txt
python git.py add hello.txt
python git.py commit -m "Update greeting"

# View the changes
python git.py show <commit-hash>
```

## Architecture

### Core Components

- **Git Class**: Main class handling all version control operations
- **Colors Class**: ANSI color codes for terminal output formatting
- **Object Storage**: Content-addressable storage using SHA-1 hashes
- **Index/Staging Area**: JSON-based file tracking for staged changes
- **Commit Structure**: JSON objects containing metadata and file references

### Directory Structure
```
.git/
├── objects/          # Content storage (organized by hash prefix)
│   ├── ab/
│   │   └── cdef123...
│   └── cd/
│       └── ef456789...
├── HEAD              # Current commit reference
└── index             # Staging area (JSON array)
```

### Data Structures

**Index Entry:**
```json
{
  "path": "filename.txt",
  "hash": "abc123def456..."
}
```

**Commit Object:**
```json
{
  "timestamp": "2024-01-01T12:00:00",
  "message": "Commit message",
  "files": [{"path": "file.txt", "hash": "hash..."}],
  "parent": "parent_commit_hash"
}
```

## Limitations

- **Text Files Only**: Binary files are not properly supported
- **No Branching**: Single linear history (no branches or merging)
- **No Remote Operations**: Local-only version control
- **Basic Diff**: Simple unified diff without advanced merge capabilities
- **No File Deletion Tracking**: Only tracks file additions and modifications
- **No Symbolic References**: No branch names, only commit hashes

## Technical Details

- **Hashing**: Uses SHA-1 for content addressing
- **Storage**: Files stored in `.git/objects` with Git-like directory structure
- **Encoding**: UTF-8 text encoding throughout
- **Format**: JSON for metadata storage (commits, index)
- **Diff Algorithm**: Python's `difflib.unified_diff`

## Error Handling

The implementation includes basic error handling for:
- Missing files during add operations
- Corrupted or missing Git objects
- Invalid repository states
- File I/O errors

## Contributing

This is an educational implementation. For production use cases, consider using the official Git client or more robust Python Git libraries like GitPython.

## License

Educational/demonstration code - use as needed for learning purposes.
