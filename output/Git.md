```markdown
# Simple Git Implementation

This Python script implements a simplified version control system, mimicking some of the basic functionalities of Git. It allows users to initialize a repository, add files to the staging area, commit changes, view the commit history, check the repository status, and display the differences introduced by a specific commit.

## Module Overview

The core of the system revolves around the `Git` class, which handles the repository's underlying operations such as object storage, index management, and commit creation. The module also includes helper classes and functions for color-coded terminal output, argument parsing, and data handling.

## Key Classes

### `Colors`

```python
class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    GREY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
```

A utility class to define ANSI color codes for enhancing terminal output with colors and styles. It provides constants for green, red, grey, reset, and bold styles.

### `Git`

```python
class Git:
    def __init__(self, repo_path: str = '.'):
        self.repo_path = Path(repo_path) / '.git'
        self.objects_path = self.repo_path / 'objects'
        self.head_path = self.repo_path / 'HEAD'
        self.index_path = self.repo_path / 'index'
```

The main class responsible for managing the Git repository.

#### Attributes:
- `repo_path` (Path): The path to the `.git` directory. Defaults to `.`.
- `objects_path` (Path): The path to the `objects` directory, where Git objects are stored.
- `head_path` (Path): The path to the `HEAD` file, which points to the current commit.
- `index_path` (Path): The path to the `index` file, which serves as the staging area.

#### Methods:

*   **`__init__(self, repo_path: str = '.')`**:

    *   Initializes a new `Git` object with the specified repository path. If no path is provided, it defaults to the current directory.

*   **`init(self) -> None`**:

    ```python
    def init(self) -> None:
        """Initialize the git repository"""
    ```

    Initializes a new Git repository in the current directory by creating the necessary directory structure (`.git/objects`) and files (`.git/HEAD`, `.git/index`).
    Raises an exception and prints to the console if the initialization fails.

*   **`hash_object(self, content: str) -> str`**:

    ```python
    def hash_object(self, content: str) -> str:
        """Create SHA-1 hash of content"""
    ```

    Computes the SHA-1 hash of a given content string using UTF-8 encoding and returns the hexadecimal representation.  This hash is used to identify and store objects in the repository.

*   **`get_object_path(self, hash_value: str) -> Path`**:

    ```python
    def get_object_path(self, hash_value: str) -> Path:
        """Get the path for storing object with folder structure (first 2 chars as folder)"""
    ```

    Determines the storage path for an object based on its SHA-1 hash.  The first two characters of the hash form a subdirectory within `.git/objects`, and the remaining characters are used as the filename. This structure helps prevent file system limitations with large numbers of files in a single directory.

*   **`add(self, file_path: str) -> None`**:

    ```python
    def add(self, file_path: str) -> None:
        """Add file to staging area"""
    ```

    Adds a file to the staging area (index). It reads the file content, calculates its hash, stores the content in the object database, and updates the index file with the file's path and hash. Prints an error message if the file does not exist or if there's an exception during the process.

*   **`update_staging_area(self, file_path: str, file_hash: str) -> None`**:

    ```python
    def update_staging_area(self, file_path: str, file_hash: str) -> None:
        """Update the staging area (index) with file information"""
    ```

    Updates the staging area (`index` file) with the specified file path and its corresponding hash. If the file already exists in the index, it removes the old entry before adding the new one.  The `index` file is stored in JSON format.

*   **`commit(self, message: str) -> None`**:

    ```python
    def commit(self, message: str) -> None:
        """Create a commit with staged files"""
    ```

    Creates a new commit with the files currently in the staging area. It reads the index, creates a commit object containing a timestamp, commit message, the list of files and their hashes, and the hash of the parent commit. The commit object is then stored in the object database, the `HEAD` file is updated to point to the new commit, and the staging area is cleared.

*   **`get_current_head(self) -> Optional[str]`**:

    ```python
    def get_current_head(self) -> Optional[str]:
        """Get the current HEAD commit hash"""
    ```

    Retrieves the hash of the current HEAD commit by reading the `HEAD` file. Returns `None` if the file is empty or if an error occurs.

*   **`log(self) -> None`**:

    ```python
    def log(self) -> None:
        """Show commit history"""
    ```

    Displays the commit history by traversing the commit chain starting from the current `HEAD`.  For each commit, it prints the commit hash, date, and message.

*   **`status(self) -> None`**:

    ```python
    def status(self) -> None:
        """Show repository status"""
    ```

    Displays the current repository status, showing the files that are staged for commit.

*   **`show_commit_diff(self, commit_hash: str) -> None`**:

    ```python
    def show_commit_diff(self, commit_hash: str) -> None:
        """Show diff for a specific commit"""
    ```

    Displays the differences introduced by a specific commit. It retrieves the commit data, then iterates through the files in the commit. For each file, it compares the content with the content in the parent commit (if any) and shows the diff using the `show_diff` method.

*   **`show_diff(self, old_content: str, new_content: str) -> None`**:

    ```python
    def show_diff(self, old_content: str, new_content: str) -> None:
        """Show colored diff between two contents"""
    ```

    Shows a colored diff between two strings using `difflib.unified_diff`. It highlights added lines in green, removed lines in red, and context lines in grey, using the ANSI color codes defined in the `Colors` class.

*   **`get_parent_file_content(self, parent_commit_data: Dict, file_path: str) -> Optional[str]`**:

    ```python
    def get_parent_file_content(self, parent_commit_data: Dict, file_path: str) -> Optional[str]:
        """Get file content from parent commit"""
    ```

    Retrieves the content of a file from a parent commit's data, given the file path.

*   **`get_commit_data(self, commit_hash: str) -> Optional[Dict[str, Any]]`**:

    ```python
    def get_commit_data(self, commit_hash: str) -> Optional[Dict[str, Any]]:
        """Get commit data by hash"""
    ```

    Retrieves the commit data for a given commit hash by reading the corresponding object file. Returns `None` if the commit is not found or if an error occurs.

*   **`get_file_content(self, file_hash: str) -> str`**:

    ```python
    def get_file_content(self, file_hash: str) -> str:
        """Get file content by hash"""
    ```

    Retrieves the content of a file given its hash by reading the corresponding object file.

## Usage

The script can be executed from the command line to perform Git-like operations.

### Commands

*   **`init`**: Initializes a new Git repository in the current directory.
    ```bash
    python your_script_name.py init
    ```
*   **`add <file>`**: Adds a file to the staging area.
    ```bash
    python your_script_name.py add myfile.txt
    ```
*   **`commit -m "<message>"`**: Creates a new commit with the staged files.
    ```bash
    python your_script_name.py commit -m "Initial commit"
    ```
*   **`log`**: Shows the commit history.
    ```bash
    python your_script_name.py log
    ```
*   **`status`**: Shows the repository status.
    ```bash
    python your_script_name.py status
    ```
*   **`show <hash>`**: Shows the diff for a specific commit.
    ```bash
    python your_script_name.py show <commit_hash>
    ```

### Example Workflow

1.  Initialize a new repository:

    ```bash
    python your_script_name.py init
    ```

2.  Create a file (e.g., `myfile.txt`) and add some content to it.

3.  Add the file to the staging area:

    ```bash
    python your_script_name.py add myfile.txt
    ```

4.  Commit the changes with a message:

    ```bash
    python your_script_name.py commit -m "Add myfile.txt"
    ```

5.  View the commit history:

    ```bash
    python your_script_name.py log
    ```

6.  Check the status:

    ```bash
    python your_script_name.py status
    ```

## Integration into Larger Projects

This script can be integrated into larger projects that require basic version control functionality. It can be used as a standalone tool or as a building block for creating more complex version control systems or automation scripts.  For example, it could be used to track changes in configuration files, documentation, or code in smaller projects where a full-fledged Git repository is not necessary.

## Limitations

This implementation is a simplified version control system and has several limitations:

*   **No branching or merging**: It does not support branching, merging, or other advanced Git features.
*   **Limited error handling**: The error handling is basic and may not cover all possible scenarios.
*   **No remote repository support**: It does not support remote repositories or collaboration features.
*   **Simple data storage**: Uses plain text files for object storage and the index, which is not optimized for large repositories.
