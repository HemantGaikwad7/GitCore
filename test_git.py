#!/usr/bin/env python3

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the output"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def test_git_client():
    """Test the Git client implementation"""
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir) / "test_repo"
        test_dir.mkdir()
        
        print(f"Testing in directory: {test_dir}")
        
        # Copy the git client to the test directory
        git_client_path = test_dir / "ccgit.py"
        with open("ccgit.py", "r") as src, open(git_client_path, "w") as dst:
            dst.write(src.read())
        
        # Make it executable
        os.chmod(git_client_path, 0o755)
        
        # Test 1: Initialize repository
        print("\n=== Test 1: Initialize Repository ===")
        code, out, err = run_command("python ccgit.py init", cwd=test_dir)
        print(f"Output: {out}")
        if err:
            print(f"Error: {err}")
        
        # Verify .git directory was created
        git_dir = test_dir / ".git"
        if git_dir.exists():
            print("✓ .git directory created successfully")
        else:
            print("✗ .git directory not found")
            return
        
        # Test with real git
        code, out, err = run_command("git status", cwd=test_dir)
        print(f"Git status: {out}")
        
        # Test 2: Add a file
        print("\n=== Test 2: Add File ===")
        test_file = test_dir / "hello-coding-challenges.txt"
        test_file.write_text("Hello World!")
        
        code, out, err = run_command("python ccgit.py add hello-coding-challenges.txt", cwd=test_dir)
        print(f"Add output: {out}")
        if err:
            print(f"Add error: {err}")
        
        # Verify with real git
        code, out, err = run_command("git status", cwd=test_dir)
        print(f"Git status after add: {out}")
        
        # Test 3: Our status command
        print("\n=== Test 3: Status Command ===")
        code, out, err = run_command("python ccgit.py status", cwd=test_dir)
        print(f"Our status: {out}")
        if err:
            print(f"Status error: {err}")
        
        # Test 4: Create another file (untracked)
        print("\n=== Test 4: Untracked File ===")
        another_file = test_dir / "another-coding-challenge.txt"
        another_file.write_text("Another file!")
        
        code, out, err = run_command("python ccgit.py status", cwd=test_dir)
        print(f"Status with untracked file: {out}")
        
        # Test 5: Commit
        print("\n=== Test 5: Commit ===")
        code, out, err = run_command('python ccgit.py commit "Add Hello CC"', cwd=test_dir)
        print(f"Commit output: {out}")
        if err:
            print(f"Commit error: {err}")
        
        # Verify with real git
        code, out, err = run_command("git log --oneline", cwd=test_dir)
        print(f"Git log: {out}")
        
        # Test 6: Modify file and diff
        print("\n=== Test 6: Diff ===")
        test_file.write_text("Hello World!\nHello Diff Step")
        
        code, out, err = run_command("python ccgit.py diff", cwd=test_dir)
        print(f"Diff output: {out}")
        if err:
            print(f"Diff error: {err}")
        
        print("\n=== All Tests Completed ===")

if __name__ == "__main__":
    test_git_client()