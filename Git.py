#!/usr/bin/env python3

import os
import json
import hashlib
import argparse
import sys
from datetime import datetime
from pathlib import Path
import difflib
from typing import Optional, Dict, List, Any

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    GREY = '\033[90m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class Git:
    def __init__(self, repo_path: str = '.'):
        self.repo_path = Path(repo_path) / '.git'
        self.objects_path = self.repo_path / 'objects'
        self.head_path = self.repo_path / 'HEAD'
        self.index_path = self.repo_path / 'index'
        
    def init(self) -> None:
        """Initialize the git repository"""
        try:
            # Create directories
            self.objects_path.mkdir(parents=True, exist_ok=True)
            
            # Create HEAD file if it doesn't exist
            if not self.head_path.exists():
                self.head_path.write_text('')
                
            # Create index file if it doesn't exist  
            if not self.index_path.exists():
                self.index_path.write_text('[]')
                
            print("Initialized empty Git repository in .git/")
            
        except Exception as e:
            print(f"Error initializing repository: {e}")
            
    def hash_object(self, content: str) -> str:
        """Create SHA-1 hash of content"""
        return hashlib.sha1(content.encode('utf-8')).hexdigest()
        
    def get_object_path(self, hash_value: str) -> Path:
        """Get the path for storing object with folder structure (first 2 chars as folder)"""
        folder = hash_value[:2]
        filename = hash_value[2:]
        folder_path = self.objects_path / folder
        folder_path.mkdir(exist_ok=True)
        return folder_path / filename
        
    def add(self, file_path: str) -> None:
        """Add file to staging area"""
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                print(f"Error: File '{file_path}' does not exist")
                return
                
            # Read file content
            file_data = file_path_obj.read_text(encoding='utf-8')
            file_hash = self.hash_object(file_data)
            
            print(f"Hash: {file_hash}")
            
            # Store file object with folder structure
            object_path = self.get_object_path(file_hash)
            object_path.write_text(file_data)
            
            # Update staging area
            self.update_staging_area(file_path, file_hash)
            print(f"Added {file_path}")
            
        except Exception as e:
            print(f"Error adding file: {e}")
            
    def update_staging_area(self, file_path: str, file_hash: str) -> None:
        """Update the staging area (index) with file information"""
        try:
            # Read current index
            index_data = json.loads(self.index_path.read_text())
            
            # Remove existing entry for this file path if it exists
            index_data = [item for item in index_data if item['path'] != file_path]
            
            # Add new entry
            index_data.append({'path': file_path, 'hash': file_hash})
            
            # Write updated index
            self.index_path.write_text(json.dumps(index_data, indent=2))
            
        except Exception as e:
            print(f"Error updating staging area: {e}")
            
    def commit(self, message: str) -> None:
        """Create a commit with staged files"""
        try:
            # Read staging area
            index_data = json.loads(self.index_path.read_text())
            
            if not index_data:
                print("Nothing to commit (staging area is empty)")
                return
                
            # Get parent commit
            parent_commit = self.get_current_head()
            
            # Create commit data
            commit_data = {
                'timestamp': datetime.now().isoformat(),
                'message': message,
                'files': index_data,
                'parent': parent_commit
            }
            
            # Hash and store commit
            commit_hash = self.hash_object(json.dumps(commit_data, sort_keys=True))
            commit_path = self.get_object_path(commit_hash)
            commit_path.write_text(json.dumps(commit_data, indent=2))
            
            # Update HEAD
            self.head_path.write_text(commit_hash)
            
            # Clear staging area
            self.index_path.write_text('[]')
            
            print(f"Commit successfully created: {commit_hash}")
            
        except Exception as e:
            print(f"Error creating commit: {e}")
            
    def get_current_head(self) -> Optional[str]:
        """Get the current HEAD commit hash"""
        try:
            head_content = self.head_path.read_text().strip()
            return head_content if head_content else None
        except:
            return None
            
    def log(self) -> None:
        """Show commit history"""
        try:
            current_commit_hash = self.get_current_head()
            
            if not current_commit_hash:
                print("No commits found")
                return
                
            while current_commit_hash:
                commit_data = self.get_commit_data(current_commit_hash)
                if not commit_data:
                    break
                    
                print("-" * 50)
                print(f"{Colors.BOLD}Commit: {current_commit_hash}{Colors.RESET}")
                print(f"Date: {commit_data['timestamp']}")
                print(f"\n    {commit_data['message']}\n")
                
                current_commit_hash = commit_data.get('parent')
                
        except Exception as e:
            print(f"Error showing log: {e}")
            
    def status(self) -> None:
        """Show repository status"""
        try:
            # Read staging area
            index_data = json.loads(self.index_path.read_text())
            
            if index_data:
                print("Changes to be committed:")
                for file_info in index_data:
                    print(f"  {Colors.GREEN}modified: {file_info['path']}{Colors.RESET}")
            else:
                print("Nothing staged for commit")
                
        except Exception as e:
            print(f"Error showing status: {e}")
            
    def show_commit_diff(self, commit_hash: str) -> None:
        """Show diff for a specific commit"""
        try:
            commit_data = self.get_commit_data(commit_hash)
            if not commit_data:
                print("Commit not found")
                return
                
            print(f"Changes in commit {commit_hash}:")
            print("-" * 50)
            
            for file_info in commit_data['files']:
                print(f"\nFile: {file_info['path']}")
                file_content = self.get_file_content(file_info['hash'])
                
                if commit_data.get('parent'):
                    # Get parent commit data
                    parent_commit_data = self.get_commit_data(commit_data['parent'])
                    parent_file_content = self.get_parent_file_content(parent_commit_data, file_info['path'])
                    
                    if parent_file_content is not None:
                        print("\nDiff:")
                        self.show_diff(parent_file_content, file_content)
                    else:
                        print(f"{Colors.GREEN}New file in this commit{Colors.RESET}")
                else:
                    print(f"{Colors.GREEN}First commit{Colors.RESET}")
                    
        except Exception as e:
            print(f"Error showing commit diff: {e}")
            
    def show_diff(self, old_content: str, new_content: str) -> None:
        """Show colored diff between two contents"""
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        diff = difflib.unified_diff(old_lines, new_lines, lineterm='')
        
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                print(f"{Colors.GREEN}{line}{Colors.RESET}", end='')
            elif line.startswith('-') and not line.startswith('---'):
                print(f"{Colors.RED}{line}{Colors.RESET}", end='')
            elif line.startswith('@@'):
                print(f"{Colors.BOLD}{line}{Colors.RESET}", end='')
            else:
                print(f"{Colors.GREY}{line}{Colors.RESET}", end='')
                
    def get_parent_file_content(self, parent_commit_data: Dict, file_path: str) -> Optional[str]:
        """Get file content from parent commit"""
        if not parent_commit_data:
            return None
            
        for file_info in parent_commit_data['files']:
            if file_info['path'] == file_path:
                return self.get_file_content(file_info['hash'])
        return None
        
    def get_commit_data(self, commit_hash: str) -> Optional[Dict[str, Any]]:
        """Get commit data by hash"""
        try:
            commit_path = self.get_object_path(commit_hash)
            if commit_path.exists():
                return json.loads(commit_path.read_text())
            return None
        except Exception as e:
            print(f"Failed to read commit data: {e}")
            return None
            
    def get_file_content(self, file_hash: str) -> str:
        """Get file content by hash"""
        object_path = self.get_object_path(file_hash)
        return object_path.read_text(encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description='Git - A simple version control system')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    subparsers.add_parser('init', help='Initialize a new repository')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add file to staging area')
    add_parser.add_argument('file', help='File to add')
    
    # Commit command
    commit_parser = subparsers.add_parser('commit', help='Create a commit')
    commit_parser.add_argument('-m', '--message', required=True, help='Commit message')
    
    # Log command
    subparsers.add_parser('log', help='Show commit history')
    
    # Status command
    subparsers.add_parser('status', help='Show repository status')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show commit diff')
    show_parser.add_argument('hash', help='Commit hash')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    git = Git()
    
    if args.command == 'init':
        git.init()
    elif args.command == 'add':
        git.add(args.file)
    elif args.command == 'commit':
        git.commit(args.message)
    elif args.command == 'log':
        git.log()
    elif args.command == 'status':
        git.status()
    elif args.command == 'show':
        git.show_commit_diff(args.hash)

if __name__ == '__main__':
    main()