# GitCore---Custom-Git-Version-Control-System

# Build Your Own Git Client

A fully functional Git client implementation in Python that demonstrates how Git works internally. This project creates a Git-compatible version control system from scratch, implementing core Git functionality including repository initialization, file staging, commits, status tracking, and diff generation.

## 🎯 Project Overview

This Git client implements Git's internal mechanisms and data structures, providing a deep understanding of how distributed version control systems work. The implementation is fully compatible with real Git repositories and can be used alongside standard Git commands.

## ✨ Features

### Core Functionality
- **Repository Initialization** - Create new Git repositories with proper `.git` directory structure
- **File Staging** - Add files to the staging area (index) with SHA-1 hashing
- **Status Tracking** - Show repository status including staged, modified, and untracked files
- **Commit Creation** - Create commits with proper tree and commit objects
- **Diff Generation** - Display differences between working directory and staged files

### Technical Implementation
- **Object Storage** - Implements Git's object database with SHA-1 hashing and zlib compression
- **Index Management** - Reads and writes Git's binary index format
- **Tree Objects** - Creates proper Git tree objects for directory structures
- **Commit Objects** - Generates commit objects with metadata and parent references
- **Full Git Compatibility** - Works seamlessly with standard Git commands

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

### Installation
1. Clone or download the project files
2. Ensure you have Python installed: `python --version`
3. Make the script executable (optional): `chmod +x ccgit.py`

### Basic Usage

```bash
# Initialize a new repository
python ccgit.py init my_project
cd my_project

# Create and add files
echo "Hello World!" > hello.txt
python ccgit.py add hello.txt

# Check repository status
python ccgit.py status

# Create a commit
python ccgit.py commit "Initial commit"

# View differences after editing
echo "More content" >> hello.txt
python ccgit.py diff
```

## 📖 Command Reference

### `init [directory]`
Initialize a new Git repository
```bash
python ccgit.py init                    # Initialize in current directory
python ccgit.py init my_project         # Initialize in new directory
```

### `add <files...>`
Add files to the staging area
```bash
python ccgit.py add file1.txt           # Add single file
python ccgit.py add file1.txt file2.txt # Add multiple files
```

### `status`
Show repository status
```bash
python ccgit.py status
```
Shows:
- Current branch
- Files staged for commit
- Modified files not staged
- Untracked files

### `commit <message>`
Create a new commit
```bash
python ccgit.py commit "Your commit message"
```

### `diff [file]`
Show differences between working directory and staged files
```bash
python ccgit.py diff                    # Show all changes
python ccgit.py diff filename.txt       # Show changes for specific file
```

## 🧪 Testing

### Automated Testing
Run the comprehensive test suite:
```bash
python test_git.py
```

This will test all functionality including:
- Repository initialization
- File staging and status
- Commit creation
- Diff generation
- Git compatibility verification

### Manual Testing
Test interoperability with real Git:
```bash
# After using ccgit commands
git status          # Should show clean working directory
git log --oneline   # Should display your commits
git show HEAD       # Should show your latest commit
```

## 🔧 Technical Architecture

### File Structure
```
project/
├── ccgit.py           # Main Git client implementation
├── test_git.py        # Automated test suite
└── README.md          # This file
```

### Git Repository Structure
When you run `ccgit.py init`, it creates:
```
.git/
├── HEAD               # Points to current branch
├── config             # Repository configuration
├── description        # Repository description
├── objects/           # Object database (blobs, trees, commits)
├── refs/              # Branch and tag references
├── hooks/             # Git hooks directory
└── info/              # Additional repository info
```

### Object Storage Format
The implementation follows Git's object storage specification:
- **Blob objects**: Store file contents
- **Tree objects**: Store directory structures
- **Commit objects**: Store commit metadata and references

All objects are:
1. Hashed with SHA-1
2. Compressed with zlib
3. Stored in `.git/objects/xx/xxxxx...` format

### Index Format
The staging area uses Git's binary index format with:
- File metadata (timestamps, permissions, size)
- SHA-1 hashes of file contents
- Filename information
- Proper padding and checksums

## 🎓 Learning Outcomes

This project demonstrates understanding of:

- **Version Control Principles**: How Git tracks changes and manages history
- **Data Structures**: Hash tables, trees, and graph structures in version control
- **Cryptographic Hashing**: SHA-1 usage for content addressing
- **File System Operations**: Binary file formats and compression
- **Software Architecture**: Modular design and command-line interfaces

## 🔄 Git Compatibility

This implementation is fully compatible with standard Git:

- ✅ **Repository format**: Uses identical `.git` directory structure
- ✅ **Object storage**: SHA-1 hashing and zlib compression match Git's format
- ✅ **Index format**: Binary index file follows Git's specification
- ✅ **Commands interoperate**: Can use `git status`, `git log`, etc. on repositories created with ccgit

## 🛠️ Example Workflow

Complete example demonstrating all features:

```bash
# 1. Initialize repository
python ccgit.py init my_project
cd my_project

# 2. Create some files
echo "# My Project" > README.md
echo "print('Hello World!')" > main.py

# 3. Stage files
python ccgit.py add README.md
python ccgit.py add main.py

# 4. Check status
python ccgit.py status
# Output: Shows both files staged for commit

# 5. Create initial commit
python ccgit.py commit "Initial project setup"

# 6. Modify a file
echo "print('Updated version')" > main.py

# 7. View changes
python ccgit.py diff
# Output: Shows unified diff of changes

# 8. Stage and commit changes
python ccgit.py add main.py
python ccgit.py commit "Update main.py"

# 9. Verify with real Git
git log --oneline
# Output: Shows both commits created by ccgit
```

## 🐛 Troubleshooting

### Common Issues

**"python: command not found"**
- Try `python3` instead of `python`
- Ensure Python is installed and in your PATH

**"Permission denied"**
- Make script executable: `chmod +x ccgit.py`
- Or always use: `python ccgit.py` instead of `./ccgit.py`

**"No such file or directory"**
- Ensure you're in the correct directory
- Use relative paths: `python ../ccgit.py` if needed

### Verification Steps
1. Check Python version: `python --version` (requires 3.6+)
2. Test with simple repository:
   ```bash
   python ccgit.py init test
   cd test
   echo "test" > file.txt
   python ccgit.py add file.txt
   python ccgit.py status
   ```

## 🚧 Future Enhancements

Potential extensions to explore:
- **Branch Management**: Create, switch, and merge branches
- **Remote Repositories**: Push and pull from remote Git servers
- **Advanced Diff**: Directory diffs and binary file handling
- **Performance**: Optimize for large repositories
- **Git Hooks**: Support for pre-commit and post-commit hooks

## 📚 References

- [Git Internals Documentation](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain)
- [Git Object Storage](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)
- [Git Index Format](https://git-scm.com/docs/index-format)
- [Pro Git Book](https://git-scm.com/book)

## 📄 License

This project is created for educational purposes. Feel free to use, modify, and distribute as needed for learning and development.

---

**Built with ❤️ for understanding Git internals**
