#!/usr/bin/env python3

import os
import sys
import hashlib
import zlib
import struct
import time
import stat
import argparse
from pathlib import Path
import difflib
import urllib.request
import urllib.parse
import base64
import json

class GitClient:
    def __init__(self, repo_path='.'):
        self.repo_path = Path(repo_path)
        self.git_dir = self.repo_path / '.git'
        
    def init(self, directory=None):
        """Initialize a new git repository"""
        if directory:
            self.repo_path = Path(directory)
            self.git_dir = self.repo_path / '.git'
            
        # Check if git repo already exists
        if self.git_dir.exists():
            print(f"Reinitialized existing Git repository in {self.git_dir.absolute()}")
            return
            
        # Create directory if it doesn't exist
        self.repo_path.mkdir(parents=True, exist_ok=True)
        
        # Create .git directory structure
        self.git_dir.mkdir(exist_ok=True)
        (self.git_dir / 'objects').mkdir(exist_ok=True)
        (self.git_dir / 'refs').mkdir(exist_ok=True)
        (self.git_dir / 'refs' / 'heads').mkdir(exist_ok=True)
        (self.git_dir / 'hooks').mkdir(exist_ok=True)
        (self.git_dir / 'info').mkdir(exist_ok=True)
        
        # Create HEAD file
        with open(self.git_dir / 'HEAD', 'w') as f:
            f.write('ref: refs/heads/master\n')
            
        # Create config file
        config_content = """[core]
\trepositoryformatversion = 0
\tfilemode = true
\tbare = false
\tlogallrefupdates = true
"""
        with open(self.git_dir / 'config', 'w') as f:
            f.write(config_content)
            
        # Create description file
        with open(self.git_dir / 'description', 'w') as f:
            f.write('Unnamed repository; edit this file \'description\' to name the repository.\n')
            
        # Create excludes file
        (self.git_dir / 'info' / 'exclude').touch()
        
        print(f"Initialized empty Git repository in {self.git_dir.absolute()}")
        
    def hash_object(self, content, obj_type='blob'):
        """Create a hash for git object"""
        # Git object format: "<type> <size>\0<content>"
        if isinstance(content, str):
            content = content.encode('utf-8')
            
        header = f"{obj_type} {len(content)}\0".encode('utf-8')
        full_content = header + content
        
        # Calculate SHA-1
        sha1 = hashlib.sha1(full_content).hexdigest()
        
        # Compress with zlib
        compressed = zlib.compress(full_content)
        
        # Store in objects directory
        obj_dir = self.git_dir / 'objects' / sha1[:2]
        obj_dir.mkdir(exist_ok=True)
        obj_file = obj_dir / sha1[2:]
        
        with open(obj_file, 'wb') as f:
            f.write(compressed)
            
        return sha1
        
    def read_object(self, sha1):
        """Read an object from the git database"""
        obj_file = self.git_dir / 'objects' / sha1[:2] / sha1[2:]
        
        if not obj_file.exists():
            raise FileNotFoundError(f"Object {sha1} not found")
            
        with open(obj_file, 'rb') as f:
            compressed = f.read()
            
        decompressed = zlib.decompress(compressed)
        null_index = decompressed.find(b'\0')
        header = decompressed[:null_index].decode('utf-8')
        content = decompressed[null_index + 1:]
        
        obj_type, size = header.split(' ')
        return obj_type, content
        
    def read_index(self):
        """Read the git index file"""
        index_file = self.git_dir / 'index'
        if not index_file.exists():
            return []
            
        entries = []
        with open(index_file, 'rb') as f:
            # Read header
            signature = f.read(4)
            if signature != b'DIRC':
                raise ValueError("Invalid index file")
                
            version = struct.unpack('>I', f.read(4))[0]
            num_entries = struct.unpack('>I', f.read(4))[0]
            
            for _ in range(num_entries):
                # Read index entry (simplified)
                ctime_sec = struct.unpack('>I', f.read(4))[0]
                ctime_nsec = struct.unpack('>I', f.read(4))[0]
                mtime_sec = struct.unpack('>I', f.read(4))[0]
                mtime_nsec = struct.unpack('>I', f.read(4))[0]
                dev = struct.unpack('>I', f.read(4))[0]
                ino = struct.unpack('>I', f.read(4))[0]
                mode = struct.unpack('>I', f.read(4))[0]
                uid = struct.unpack('>I', f.read(4))[0]
                gid = struct.unpack('>I', f.read(4))[0]
                file_size = struct.unpack('>I', f.read(4))[0]
                sha1 = f.read(20).hex()
                flags = struct.unpack('>H', f.read(2))[0]
                
                # Read filename
                name_length = flags & 0xfff
                name = f.read(name_length).decode('utf-8')
                
                # Padding to 8-byte boundary
                total_read = 62 + name_length
                padding = (8 - (total_read % 8)) % 8
                f.read(padding)
                
                entries.append({
                    'name': name,
                    'sha1': sha1,
                    'mode': mode,
                    'size': file_size,
                    'mtime': mtime_sec
                })
                
        return entries
        
    def write_index(self, entries):
        """Write the git index file"""
        index_file = self.git_dir / 'index'
        
        with open(index_file, 'wb') as f:
            # Write header
            f.write(b'DIRC')  # signature
            f.write(struct.pack('>I', 2))  # version
            f.write(struct.pack('>I', len(entries)))  # number of entries
            
            for entry in entries:
                name_bytes = entry['name'].encode('utf-8')
                
                # Write entry
                f.write(struct.pack('>I', 0))  # ctime_sec
                f.write(struct.pack('>I', 0))  # ctime_nsec
                f.write(struct.pack('>I', entry['mtime']))  # mtime_sec
                f.write(struct.pack('>I', 0))  # mtime_nsec
                f.write(struct.pack('>I', 0))  # dev
                f.write(struct.pack('>I', 0))  # ino
                f.write(struct.pack('>I', entry['mode']))  # mode
                f.write(struct.pack('>I', 0))  # uid
                f.write(struct.pack('>I', 0))  # gid
                f.write(struct.pack('>I', entry['size']))  # file_size
                f.write(bytes.fromhex(entry['sha1']))  # sha1
                f.write(struct.pack('>H', len(name_bytes)))  # flags
                f.write(name_bytes)  # filename
                
                # Padding to 8-byte boundary
                total_written = 62 + len(name_bytes)
                padding = (8 - (total_written % 8)) % 8
                f.write(b'\0' * padding)
                
    def add(self, filename):
        """Add a file to the index"""
        file_path = self.repo_path / filename
        
        if not file_path.exists():
            print(f"fatal: pathspec '{filename}' did not match any files")
            return
            
        # Read file content and create hash
        with open(file_path, 'rb') as f:
            content = f.read()
            
        sha1 = self.hash_object(content, 'blob')
        
        # Get file statistics
        file_stat = file_path.stat()
        
        # Read current index
        try:
            entries = self.read_index()
        except:
            entries = []
            
        # Update or add entry
        entry = {
            'name': filename,
            'sha1': sha1,
            'mode': file_stat.st_mode,
            'size': file_stat.st_size,
            'mtime': int(file_stat.st_mtime)
        }
        
        # Remove existing entry if present
        entries = [e for e in entries if e['name'] != filename]
        entries.append(entry)
        entries.sort(key=lambda x: x['name'])
        
        # Write updated index
        self.write_index(entries)
        
    def status(self):
        """Show repository status"""
        # Get current branch
        try:
            with open(self.git_dir / 'HEAD', 'r') as f:
                head_content = f.read().strip()
                if head_content.startswith('ref: '):
                    branch = head_content[5:].split('/')[-1]
                else:
                    branch = head_content[:7]  # detached HEAD
        except:
            branch = 'master'
            
        print(f"On branch {branch}")
        
        # Check if there are any commits
        master_ref = self.git_dir / 'refs' / 'heads' / 'master'
        if not master_ref.exists():
            print("\nNo commits yet")
            
        # Read index
        try:
            staged_files = self.read_index()
        except:
            staged_files = []
            
        # Get all files in working directory
        working_files = {}
        for file_path in self.repo_path.rglob('*'):
            if file_path.is_file() and not str(file_path).startswith(str(self.git_dir)):
                rel_path = file_path.relative_to(self.repo_path)
                working_files[str(rel_path)] = file_path
                
        # Categorize files
        staged = []
        modified = []
        untracked = []
        
        staged_names = {entry['name'] for entry in staged_files}
        
        for entry in staged_files:
            if entry['name'] in working_files:
                # Check if file has been modified
                file_path = working_files[entry['name']]
                with open(file_path, 'rb') as f:
                    current_content = f.read()
                current_hash = self.hash_object(current_content, 'blob')
                
                if current_hash != entry['sha1']:
                    modified.append(entry['name'])
                else:
                    staged.append(entry['name'])
            else:
                staged.append(entry['name'])  # File was deleted
                
        for filename, file_path in working_files.items():
            if filename not in staged_names:
                untracked.append(filename)
                
        # Print status
        if staged:
            print("\nChanges to be committed:")
            print("  (use \"git restore --staged <file>...\" to unstage)")
            for filename in staged:
                print(f"\tnew file:   {filename}")
                
        if modified:
            print("\nChanges not staged for commit:")
            print("  (use \"git add <file>...\" to update what will be committed)")
            for filename in modified:
                print(f"\tmodified:   {filename}")
                
        if untracked:
            print("\nUntracked files:")
            print("  (use \"git add <file>...\" to include in what will be committed)")
            for filename in untracked:
                print(f"\t{filename}")
                
        if not staged and not modified and not untracked:
            print("\nnothing to commit, working tree clean")
            
    def create_tree_object(self, entries):
        """Create a tree object from index entries"""
        tree_content = b''
        
        for entry in sorted(entries, key=lambda x: x['name']):
            # Format: <mode> <name>\0<20-byte-sha1>
            mode = oct(entry['mode'])[-6:]  # Get last 6 digits of octal
            name = entry['name'].encode('utf-8')
            sha1_bytes = bytes.fromhex(entry['sha1'])
            
            tree_content += f"{mode} {entry['name']}\0".encode('utf-8') + sha1_bytes
            
        return self.hash_object(tree_content, 'tree')
        
    def create_commit_object(self, tree_sha1, message, parent=None):
        """Create a commit object"""
        timestamp = int(time.time())
        timezone = "+0000"  # UTC
        author = "CCGit User <user@example.com>"
        
        commit_content = f"tree {tree_sha1}\n"
        if parent:
            commit_content += f"parent {parent}\n"
        commit_content += f"author {author} {timestamp} {timezone}\n"
        commit_content += f"committer {author} {timestamp} {timezone}\n"
        commit_content += f"\n{message}\n"
        
        return self.hash_object(commit_content.encode('utf-8'), 'commit')
        
    def commit(self, message):
        """Create a commit"""
        # Read staged files
        try:
            entries = self.read_index()
        except:
            print("fatal: no changes added to commit")
            return
            
        if not entries:
            print("fatal: no changes added to commit")
            return
            
        # Create tree object
        tree_sha1 = self.create_tree_object(entries)
        
        # Get parent commit if exists
        master_ref = self.git_dir / 'refs' / 'heads' / 'master'
        parent = None
        if master_ref.exists():
            with open(master_ref, 'r') as f:
                parent = f.read().strip()
                
        # Create commit object
        commit_sha1 = self.create_commit_object(tree_sha1, message, parent)
        
        # Update master reference
        (self.git_dir / 'refs' / 'heads').mkdir(exist_ok=True)
        with open(master_ref, 'w') as f:
            f.write(commit_sha1 + '\n')
            
        print(f"committed to master: {commit_sha1}")
        
    def diff(self, filename=None):
        """Show differences between working directory and index"""
        try:
            staged_files = self.read_index()
        except:
            staged_files = []
            
        staged_dict = {entry['name']: entry for entry in staged_files}
        
        # Get files to diff
        if filename:
            files_to_check = [filename] if filename in staged_dict else []
        else:
            # Check all staged files
            files_to_check = []
            for file_path in self.repo_path.rglob('*'):
                if file_path.is_file() and not str(file_path).startswith(str(self.git_dir)):
                    rel_path = str(file_path.relative_to(self.repo_path))
                    if rel_path in staged_dict:
                        files_to_check.append(rel_path)
                        
        for filename in files_to_check:
            file_path = self.repo_path / filename
            
            if not file_path.exists():
                continue
                
            # Get current content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                current_lines = f.readlines()
                
            # Get staged content
            entry = staged_dict[filename]
            _, staged_content = self.read_object(entry['sha1'])
            staged_lines = staged_content.decode('utf-8', errors='ignore').splitlines(keepends=True)
            
            # Generate diff
            diff = difflib.unified_diff(
                staged_lines, 
                current_lines,
                fromfile=f'a/{filename}',
                tofile=f'b/{filename}',
                lineterm=''
            )
            
            diff_output = ''.join(diff)
            if diff_output:
                print(f"diff --git a/{filename} b/{filename}")
                print(f"index {entry['sha1'][:7]}..{self.hash_object(open(file_path, 'rb').read())[:7]} 100644")
                print(diff_output)


def main():
    parser = argparse.ArgumentParser(description='A simple Git client implementation')
    subparsers = parser.add_subparsers(dest='command', help='Git commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize a new repository')
    init_parser.add_argument('directory', nargs='?', help='Directory to initialize')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add files to index')
    add_parser.add_argument('files', nargs='+', help='Files to add')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show repository status')
    
    # Commit command
    commit_parser = subparsers.add_parser('commit', help='Create a commit')
    commit_parser.add_argument('message', help='Commit message')
    
    # Diff command
    diff_parser = subparsers.add_parser('diff', help='Show differences')
    diff_parser.add_argument('file', nargs='?', help='File to diff')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    git = GitClient()
    
    if args.command == 'init':
        git.init(args.directory)
    elif args.command == 'add':
        for filename in args.files:
            git.add(filename)
    elif args.command == 'status':
        git.status()
    elif args.command == 'commit':
        git.commit(args.message)
    elif args.command == 'diff':
        git.diff(args.file)


if __name__ == '__main__':
    main()