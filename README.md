# Process Killer App

A Python application to manage system processes. The app provides functionality to list, kill, and manage processes based on their PID (Process ID) or name. It also includes features to monitor system resources and shutdown the system.

## Features

- **Kill Process by PID**: Terminate a process using its PID (Process ID).
- **Kill Process by Name**: Terminate all processes with a specific name.
- **List All Processes**: Display all running processes with their PID and name.
- **View System Resource Usage**: Check CPU, memory, and disk usage.
- **Shutdown the System**: Shutdown the system using the appropriate command.
- **Check Process Memory Usage**: View the memory usage of a process by its PID or name.
- **Interactive Mode**: A user-friendly interactive mode for managing processes and system resources.

## Requirements

- Python 3.x
- `psutil` library (install via `pip install psutil`)

## Installation

1. Clone or download this repository.
2. Install the required Python library:

   ```bash
   pip install psutil
   ```

## Usage

### Command-Line Usage

Run the script with either a PID or process name and the type of kill operation (either pid or name).

Example:

```bash
python process_killer.py <name_or_pid> <kill_type>
```

- `<name_or_pid>`: The process name or PID.
- `<kill_type>`: Either pid (to kill by PID) or name (to kill by process name).

Example to kill a process by PID:

```bash
python process_killer.py 1234 pid
```

Example to kill a process by name:

```bash
python process_killer.py my_process_name name
```

### Interactive Mode

If no arguments are passed, the script will enter an interactive mode, allowing you to choose from the following options:

- Kill process by PID
- Kill process by name
- List all processes
- Check memory usage by PID
- Check memory usage by process name
- View system resources usage
- Shutdown the system
- Exit interactive mode

To start interactive mode, run the script without any arguments:

```bash
python process_killer.py
```

Then, choose an option from the menu displayed.

### Functions

- `log_message(message, to_file=False)`: Logs messages to the console and optionally to a log file (process_killer.log).
- `kill_process_by_pid(pid, force=False)`: Terminates the process with the given PID.
- `kill_process_by_name(name, force=False)`: Terminates all processes with the given name.
- `get_process_info(pid)`: Retrieves detailed information about the process with the given PID.
- `list_processes_by_name(name)`: Lists all processes with the given name.
- `list_all_processes()`: Lists all running processes.
- `check_system_resources()`: Displays system resource usage (CPU, memory, disk).
- `shutdown_system()`: Shuts down the system.
- `check_psutil_version()`: Checks if the installed psutil version is compatible.
- `check_os_and_warn()`: Warns about OS-specific considerations.
- `interactive_mode()`: Runs the app in interactive mode, allowing users to manage processes.
- `display_menu()`: Displays the main menu in interactive mode.

### Logging

Logs are saved in a file named process_killer.log. The log includes messages related to process management and system resource usage.

### Troubleshooting

- Access Denied: On some operating systems, you may need administrator/root privileges to kill certain processes.
- Zombie Processes: Some processes may be in a "zombie" state and cannot be killed.
- Compatibility: Ensure that psutil is installed and is the correct version (5.9.0 or higher).

### License

This project is licensed under the MIT License - see the LICENSE file for details.

Copyright 2025, Max Base


