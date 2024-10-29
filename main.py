"""
Directory Manager - A Command Line Interface for Managing Directory Structures

This program implements a hierarchical directory management system with the following features:
   - Create directories (single or multiple at once)
   - Delete directories (with confirmation for non-empty directories)
   - Move directories (with automatic parent directory creation)
   - List directory structure (with proper indentation and sorting)

Game Plan:
1.DONE: Create Basic Structure
   [x] Create Node class
      [x] Add name property
      [x] Add children dictionary/map property
   [x] Create DirectoryManager class
      [x] Add root node property (empty string as name)

2.DONE: Implement Helper Functions
   [x] Create _get_node_and_parent function
      [x] Take path as input
      [x] Split path by '/'
      [x] Navigate tree to find node
      [x] Return parent node, current node, and last part of path
      [x] Handle cases when path doesn't exist

3.DONE: Implement Core Commands
   [x] CREATE command
      [x] Print CREATE command with path
      [x] Split path into parts
      [x] Start at root node
      [x] Create each missing directory in path
      [x] Link new directories to parents

   [x] DELETE command
      [x] Print DELETE command with path
      [x] Find parent and target nodes
      [x] Check if path exists
      [x] Print error if path not found
      [x] Remove directory from parent's children if exists

   [x] MOVE command
      [x] Print MOVE command with paths
      [x] Find source node and parent
      [x] Create/find destination path
      [x] Move node to new location
      [x] Remove from old location

   [x] LIST command
      [x] Print LIST at start
      [x] Track indentation level
      [x] Sort children alphabetically
      [x] Print each directory with proper indentation
      [x] Recursively list subdirectories

4.DONE: Implement Main Program Loop
   [x] Create DirectoryManager instance
   [x] Process input commands
      [x] Split command into parts
      [x] Identify command type
      [x] Call appropriate function
      [x] Handle invalid commands

5.DONE: Testing
   [x] Test CREATE
      [x] Single directory
      [x] Nested directories
      [x] Existing directories
   [x] Test DELETE
      [x] Existing directory
      [x] Non-existent directory
      [x] Nested directory
   [x] Test MOVE
      [x] Simple move
      [x] Move with subdirectories
      [x] Move to non-existent path
   [x] Test LIST
      [x] Empty directory
      [x] Multiple levels
      [x] Correct indentation

6.DONE: Edge Cases to Handle
   [x] Invalid paths
   [x] Missing parent directories
   [x] Moving directories to their own subdirectories
   [x] Deleting non-existent paths
   [x] Empty commands
   [x] Malformed commands

7.DONE: Output Formatting
   [x] Exact command echo
   [x] Proper indentation (2 spaces per level)
   [x] Error message formatting
   [x] Alphabetical sorting in LIST

8.TODO: Final Touches
   [ ] Add comments/documentation
   [ ] Clean up code
   [x] Test against example input/output

9.TODO: Additional Features
   [x] Add color to CLI app
   [x] Create ASCII art for CLI using Endpoint's logo
   [ ] Add rename command
   [ ] Add search command
   [ ] Add copy command
   [ ] Add history command. Maybe using readline to store commands into an array.
   [ ] Add undo command
   [ ] Add save/load functionality to and from a json file
   [ ] Add auto-completion functionality
   [ ] Able to make directories with spaces in the name
   [x] Able to make multiple directories at once. Thinking of accepting commands like 'c number/odd/1,3,5,7,9'
"""
class EndpointLogo:
   """ASCII art representation of the Endpoint logo used for the loading screen."""
   logo = '''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#,..,#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#,  ,#%%#,  ,#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%/   #%%%%%%%%%%#.  *%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%(.  *%%%%%%%%%%%%%%%%%%/   /%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%,  ,#%%%%%%%%%%%%%%%%%%%%%%%%%*  .#%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%#  &%%%%%%%%%#############%%%%%%%%%. *%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%# .%%%%%%, .//////////////,  #%%%%%# .%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%# ,%%%%%( .%%%%%%%%%%%%%%%%( ,%%%%%% .%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%# ,%%%%%( .%%%%%%%%%%%%%%%%( ,%%%%%% .%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%# .%%%%%( .%%%%%%%%%%%%%%%%( ,%%%%%% .%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%.  ////*  ///////////////.  #%%%%%% .%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%####/ .###############%%%%%%%%%# .%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%( .%%%%%%%%%%%%%%%%%%%%%%%%# .%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%. *%%%%%%%%%%%%%%%%%%%%%#.  #%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(*********************/#%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''

class ANSICodes:
   """
   Handles terminal color formatting using ANSI escape codes.
   
   Provides class methods for:
   - Colorizing text with foreground and background colors
   - Clearing the terminal screen
   """
   
   # ANSI escape codes dictionary for various colors
   colors = {
      # Standard Colors
      'black': '\033[30m',
      'red': '\033[31m',
      'green': '\033[32m',
      'yellow': '\033[33m',
      'blue': '\033[34m',
      'magenta': '\033[35m',
      'cyan': '\033[36m',
      'white': '\033[37m',

      # Background Colors
      'bg_red': '\033[41m',
      'bg_green': '\033[42m',
      'bg_yellow': '\033[43m',
      'bg_blue': '\033[44m',
      'bg_magenta': '\033[45m',
      'bg_cyan': '\033[46m',
      'bg_white': '\033[47m',

      # Reset
      'reset': '\033[0m'
   }
   
   @classmethod
   def print_clear(cls):
      """Clears the terminal screen and scrollback buffer."""
      print('\033[2J\033[H\033[3J', end='')
   
   @classmethod
   def colorize(cls, text, text_color='white', bg_color='black'):
      """
      Applies ANSI color codes to text.
      
      Args:
            text (str): The text to colorize
            text_color (str): Foreground color name
            bg_color (str): Background color name
      
      Returns:
            str: The colorized text string
      """
      text_color_code = cls.colors.get(text_color.lower(), cls.colors['reset'])
      bg_color_code = cls.colors.get(bg_color.lower(), '')
      return f"{bg_color_code}{text_color_code}{text}{cls.colors['reset']}"

# Node class to represent directories in the tree
class Node:
   """
   Represents a directory in the directory tree.
   
   Attributes:
      name (str): Name of the directory
      children (dict): Dictionary of child directories, mapping names to Node objects
   """
   def __init__(self, name):
      self.name = name
      self.children = {}

# DirectoryManager class to manage the directory tree
class DirectoryManager:
   """
   Manages the directory tree structure and operations.
   
   Provides methods for creating, deleting, moving, and listing directories.
   Handles path validation and edge cases for all operations.
   """
   def __init__(self):
      """Initializes the directory manager with an empty root node."""
      self.root = Node("")

   # Helper function to get the node and parent for a given path
   def _get_node_and_parent(self, path):
      """
      Locates a node and its parent in the directory tree.
      
      Args:
            path (str): Path to the target directory
            
      Returns:
            tuple: (parent_node, target_node, target_name) or (None, None, target_name) if not found
      """
      # Handle empty or root path
      if not path or path == "/":
            return None, self.root, ""
      
      # Split path and remove any empty strings
      parts = [p for p in path.split('/') if p]
      
      if not parts:
            return None, self.root, ""
      
      current = self.root
      parent = None
      
      # Navigate through all parts except the last one
      for part in parts[:-1]:
            if part not in current.children:
               return None, None, parts[-1]
            parent = current
            current = current.children[part]
      
      return current, current.children.get(parts[-1]), parts[-1]

   def _is_valid_path(self, path):
      """
      Validates a directory path.
      
      Args:
            path (str): Path to validate
            
      Returns:
            bool: True if path is valid, False otherwise
      """
      # Check if path contains invalid characters or empty directory names
      if not path:
            return False
      
      parts = [p for p in path.split('/') if p]
      
      # Check each directory name
      for part in parts:
            # Check for empty names or names with special characters
            if not part or any(char in part for char in '\/:*?"<>|'):
               return False
      return True

   def _is_subdirectory(self, parent_path, child_path):
      """
      Checks if one path is a subdirectory of another.
      
      Args:
            parent_path (str): Potential parent directory path
            child_path (str): Potential child directory path
            
      Returns:
            bool: True if child_path is a subdirectory of parent_path
      """
      # Check if child_path is a subdirectory of parent_path
      parent_parts = [p for p in parent_path.split('/') if p]
      child_parts = [p for p in child_path.split('/') if p]
      
      if len(parent_parts) >= len(child_parts):
            return False
      
      return all(p == c for p, c in zip(parent_parts, child_parts))

   def _expand_path_list(self, path):
      """
      Expands comma-separated paths into a list of individual paths.
      
      Supports multiple directories at:
      - Root level: 'fruits,family,number'
      - Nested level: 'fruits/citrus/lemon,lime'
      - Mixed levels: 'fruits,veggies/green,red'
      
      Args:
            path (str): Path string potentially containing comma-separated values
            
      Returns:
            list: List of individual paths
      """
      if ',' not in path:
            return [path]
            
      # If comma is in the first part (before any slash)
      if '/' not in path or path.find(',') < path.find('/'):
            return [p.strip() for p in path.split(',') if p.strip()]
            
      # For nested paths with commas
      base_path = path[:path.rindex('/') + 1]
      names = path[len(base_path):].split(',')
      return [f"{base_path}{name.strip()}" for name in names if name.strip()]

   def create(self, path):
      """
      Creates one or more directories.
      
      Args:
            path (str): Path(s) to create, can include comma-separated values
      """
      # Handle comma-separated paths
      paths = self._expand_path_list(path)
      
      created_paths = []
      for single_path in paths:
            # Validate path
            if not self._is_valid_path(single_path):
               print(ANSICodes.colorize(f"Cannot create {single_path} - invalid path name", 'red'))
               continue
               
            parts = [p for p in single_path.split('/') if p]
            current = self.root

            # Create all necessary parent directories
            for part in parts:
               if part not in current.children:
                  current.children[part] = Node(part)
               current = current.children[part]
               
            created_paths.append(single_path)
            print(ANSICodes.colorize(f"Directory {single_path} created successfully", 'green'))
            
      if created_paths:
            self.list()
      print('================================================================================')

   def _confirm_deletion(self, target):
      """Helper method to handle deletion confirmations"""
      confirm = input(ANSICodes.colorize(f"Are you sure you want to delete {target}? (yes/no): ", 'yellow')).strip().lower()
      if confirm not in ["yes", "y"]:
            print(ANSICodes.colorize("Deletion cancelled.", 'yellow'))
            print('================================================================================')
            return False
      return True

   def delete(self, path):      
      # Special case for root/empty paths
      if path in ["", "/", "root", "root/", "list"]:
            if not self._confirm_deletion("root directory and all its contents"):
               return
            self.root.children.clear()
            print(ANSICodes.colorize("Root directory and all its contents have been deleted.", 'red'))
            self.list()
            print('================================================================================')
            return

      # Get the parent and target nodes
      parent, node, target_name = self._get_node_and_parent(path)
      
      # Check if path exists
      if parent is None or target_name not in parent.children:
            print(ANSICodes.colorize(f"Cannot delete {path} - path does not exist", 'red'))
            print('================================================================================')
            return

      # Check if directory has contents and confirm deletion
      target_node = parent.children[target_name]
      if target_node.children and not self._confirm_deletion(f"directory '{path}' and its subdirectories"):
            return
      
      # Perform the deletion using pop()
      removed_node = parent.children.pop(target_name)
      print(ANSICodes.colorize(f"Directory {path} and all its contents have been deleted.", 'red'))
      
      if len(parent.children) > 0:
            self.list()
      print('================================================================================')

   def move(self, source, destination):
      """
      Moves a directory to a new location.
      
      Args:
            source (str): Path of directory to move
            destination (str): Destination path
      """
      # Validate paths
      if not self._is_valid_path(source) or not self._is_valid_path(destination):
            print(ANSICodes.colorize("Cannot move - invalid path name", 'red'))
            return

      # Check if trying to move to same location
      if source == destination:
            print(ANSICodes.colorize(f"Cannot move {source} - source and destination are the same", 'red'))
            return
      
      # Check if source exists
      src_parent, src_node, src_name = self._get_node_and_parent(source)
      if src_parent is None or src_name not in src_parent.children:
            print(ANSICodes.colorize(f"Cannot move {source} - path does not exist", 'red'))
            return
      
      # Check if trying to move to own subdirectory
      if self._is_subdirectory(source, destination):
            print(ANSICodes.colorize(f"Cannot move {source} - cannot move directory into its own subdirectory", 'red'))
            return

      # Get the node to be moved
      node_to_move = src_parent.children[src_name]
      
      # Create destination path if it doesn't exist
      dest_parts = [p for p in destination.split('/') if p]
      current = self.root
      
      # Create all necessary parent directories
      for part in dest_parts:
            if part not in current.children:
               current.children[part] = Node(part)
            current = current.children[part]
      
      # Check if destination already has a directory with the same name
      if src_name in current.children:
            print(ANSICodes.colorize(f"Cannot move {source} - destination already contains a directory named {src_name}", 'red'))
            return
      
      # Move the node
      current.children[src_name] = node_to_move
      del src_parent.children[src_name]
      print(ANSICodes.colorize(f"Moved {source} to {destination}", 'green'))
      self.list()
      print('================================================================================')

   def list(self, node=None, indent=0, prefix=""):
      """
      Displays the directory tree structure.
      
      Args:
            node (Node, optional): Starting node. Defaults to root if None
            indent (int): Current indentation level
            prefix (str): Prefix string for current line
      """
      if node is None:
            print(ANSICodes.colorize("List", 'cyan'))
            node = self.root
            
      children = sorted(node.children.keys())
      for i, name in enumerate(children):
            child = node.children[name]
            is_last = i == len(children) - 1
            
            # Create the branch characters
            current_prefix = "└── " if is_last else "├── "
            next_prefix = "    " if is_last else "│   "
            
            # Print current directory with its branch in cyan
            print(prefix + ANSICodes.colorize(current_prefix + child.name, 'cyan'))
            
            # Recursively print children with updated prefix
            self.list(child, indent + 1, prefix + next_prefix)

def loading_animation():
   """Displays the Endpoint logo with a loading animation effect."""
   lines = EndpointLogo.logo.splitlines()
   for line in lines:
      print(ANSICodes.colorize(line, 'white', 'bg_blue')) 
      for i in range(8000000):
            pass

def print_menu():
   """Displays the main menu with available commands."""
   print('================================================================================')
   print('\t\t\tWelcome to the Directory Manager')
   print('================================================================================')
   print('1.', ANSICodes.colorize('Create Directory', 'green'))
   print('2.', ANSICodes.colorize('Delete Directory', 'red'))
   print('3.', ANSICodes.colorize('Move Directory', 'yellow'))
   print('4.', ANSICodes.colorize('List Directories', 'cyan'))
   print('5.', ANSICodes.colorize('Help', 'magenta'))
   print('6.', ANSICodes.colorize('Exit', 'red'))
   print('================================================================================')

def help_menu():
   """Displays detailed help information for all commands."""
   print('================================================================================')
   print('\t\t\t\tHelp Menu')
   print('================================================================================')
   print(ANSICodes.colorize('Create (C) - Create a new directory', 'green'))
   print(ANSICodes.colorize("  Usage: 'c family' or 'c' then enter path", 'white'))
   print(ANSICodes.colorize("  Multiple directories:", 'white'))
   print(ANSICodes.colorize("    - Root level: 'c fruits,family,number'", 'white'))
   print(ANSICodes.colorize("    - Nested level: 'c fruits/citrus/lemon,lime,orange'", 'white'))
   print(ANSICodes.colorize("    - Mixed levels: 'c fruits,veggies/green,red'", 'white'))
   print()
   print(ANSICodes.colorize('Delete (D) - Remove a directory', 'red'))
   print(ANSICodes.colorize("  Usage: 'd family' or 'd' then enter path", 'white'))
   print()
   print(ANSICodes.colorize('Move (M) - Move a directory to a new location', 'yellow'))
   print(ANSICodes.colorize("  Usage: 'm source destination' or", 'white'))
   print(ANSICodes.colorize("         'm source' then enter destination, or", 'white'))
   print(ANSICodes.colorize("         'm' then enter both paths when prompted", 'white'))
   print()
   print(ANSICodes.colorize('List (L) - Show all directories', 'cyan'))
   print(ANSICodes.colorize('  Usage: Shows directory tree with proper indentation', 'white'))
   print()
   print(ANSICodes.colorize('Help (H) - Show this help message', 'magenta'))
   print()
   print(ANSICodes.colorize('Exit (E) - Exit the program', 'red'))
   print('================================================================================')

def exit_program():
   """Handles program exit with cleanup."""
   print('Thank you for using the Directory Manager! Press any key to exit...')
   print('================================================================================')
   input()
   ANSICodes.print_clear()

def logic_loop():
   """
   Main program loop that handles user input and command execution.
   
   Creates a DirectoryManager instance and processes commands until exit.
   """
   directory_manager = DirectoryManager()
   while True:
      command = input(ANSICodes.colorize('Enter command: ', 'green')).strip().lower().split()
      
      # Handle single command with no arguments
      if not command:
            print(ANSICodes.colorize('Invalid command. Please try again.', 'red'))
            print('================================================================================')
            continue
            
      cmd = command[0]
      args = command[1:] if len(command) > 1 else None

      match cmd:
            case '1' | 'c' | 'create':
               path = args[0] if args else input('Enter path: ')
               directory_manager.create(path)

            case '2' | 'd' | 'delete':
               path = args[0] if args else input('Enter path: ')
               directory_manager.delete(path)

            case '3' | 'm' | 'move':
               if args and len(args) >= 2:
                  # If both source and destination are provided in command
                  source, destination = args[0], args[1]
               elif args:
                  # If only source is provided in command
                  source = args[0]
                  destination = input('Enter destination path: ')
               else:
                  # If no args provided
                  source = input('Enter source path: ')
                  destination = input('Enter destination path: ')
               directory_manager.move(source, destination)

            case '4' | 'l' | 'list':
               directory_manager.list()
               print('================================================================================')

            case '5' | 'h' | 'help':
               ANSICodes.print_clear()
               help_menu()

            case '6' | 'e' | 'exit':
               exit_program()
               break

            case _:
               print(ANSICodes.colorize('Invalid command. Please try again.', 'red'))
               print('================================================================================')

def main():
   """
   Program entry point.
   
   Displays logo, menu, and starts the command loop.
   """
   loading_animation()
   print_menu()
   logic_loop()

if __name__ == '__main__':
   try:
      main()
   except KeyboardInterrupt:
      print('\nProgram terminated by user.')
   except Exception as e:
      print(f'\nAn error occurred: {e}')