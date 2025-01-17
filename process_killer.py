import psutil
import sys
import os
import time


def log_message(message, to_file=False):
    """Log messages for better user experience and debugging."""
    print(message)
    if to_file:
        with open("process_killer.log", "a") as log_file:
            log_file.write(f"{time.ctime()} - {message}\n")


def kill_process_by_pid(pid, force=False):
    """Kill a process by its PID. Force kill if specified."""
    try:
        process = psutil.Process(pid)
        if force:
            process.kill()
            log_message(f"Force killed process with PID {pid}.")
        else:
            process.terminate()
            process.wait()
            log_message(f"Process with PID {pid} has been terminated.")
    except psutil.NoSuchProcess:
        log_message(f"No process found with PID {pid}.")
    except psutil.AccessDenied:
        log_message(f"Access denied to kill process with PID {pid}. Try running the script as an administrator or root.")
    except psutil.ZombieProcess:
        log_message(f"Process with PID {pid} is a zombie and cannot be terminated.")
    except Exception as e:
        log_message(f"An error occurred: {e}")


def get_process_info(pid):
    """Get detailed information of a process."""
    try:
        process = psutil.Process(pid)
        info = {
            "PID": pid,
            "Name": process.name(),
            "CPU": process.cpu_percent(interval=1),
            "Memory": process.memory_info().rss / (1024 * 1024),
            "Start Time": time.ctime(process.create_time()),
            "Command Line": " ".join(process.cmdline())
        }
        return info
    except psutil.NoSuchProcess:
        log_message(f"No process found with PID {pid}.")
        return None


def list_processes_by_name(name):
    """List all processes matching the given name with extra details."""
    log_message(f"Listing all processes with the name: {name}")
    found = False
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() == name.lower():
            process_info = get_process_info(process.info['pid'])
            if process_info:
                log_message(f"Process Info: {process_info}")
                found = True
    if not found:
        log_message(f"No processes found with the name {name}.")


def list_all_processes():
    """List all running processes."""
    log_message("Listing all running processes:")
    for process in psutil.process_iter(['pid', 'name']):
        log_message(f"PID: {process.info['pid']}, Name: {process.info['name']}")


def check_system_resources():
    """Check system resource usage."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    log_message(f"System Resources - CPU: {cpu_percent}%, Memory: {memory_percent}%, Disk: {disk_percent}%")


def shutdown_system():
    """Shutdown the system."""
    log_message("Shutting down the system...")
    if os.name == 'nt':
        os.system("shutdown /s /t 1")
    else:
        os.system("sudo shutdown now")


def check_psutil_version():
    """Check if the installed psutil version is compatible."""
    required_version = (5, 9, 0)
    installed_version = tuple(map(int, psutil.__version__.split('.')))
    if installed_version < required_version:
        log_message(f"Warning: The installed psutil version {psutil.__version__} is older than the required version {'.'.join(map(str, required_version))}.")
    else:
        log_message(f"psutil version {psutil.__version__} is compatible.")


def check_os_and_warn():
    """Check the operating system and provide appropriate warnings."""
    if os.name == 'nt':
        log_message("Running on Windows. Ensure you have Administrator privileges to kill certain processes.")
    elif os.name == 'posix':
        log_message("Running on a POSIX-based OS (Linux/macOS). You may need root access to kill some processes.")
    else:
        log_message(f"Running on an unrecognized OS: {os.name}. Ensure you have appropriate permissions.")


def interactive_mode():
    """Interactive mode for managing processes with additional functionality."""
    options = {
        "1": kill_process_by_pid_interactive,
        "2": kill_process_by_name_interactive,
        "3": list_all_processes,
        "4": check_memory_usage_by_pid_interactive,
        "5": check_memory_usage_by_name_interactive,
        "6": check_system_resources,
        "7": shutdown_system_and_exit,
        "8": exit_interactive_mode
    }

    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ")
        if choice in options:
            options[choice]()
        else:
            log_message("Invalid choice. Please choose a valid option.")


def display_menu():
    """Display the main menu options."""
    log_message("\nChoose an option:")
    log_message("1. Kill process by PID")
    log_message("2. Kill process by name")
    log_message("3. List all processes")
    log_message("4. Check memory usage by PID")
    log_message("5. Check memory usage by name")
    log_message("6. View system resources usage")
    log_message("7. Shutdown system")
    log_message("8. Exit")


def kill_process_by_pid_interactive():
    """Interactive process kill by PID."""
    pid = int(input("Enter PID to kill: "))
    force = input("Force kill? (y/n): ").lower() == 'y'
    kill_process_by_pid(pid, force)


def kill_process_by_name(name, force=False):
    """Kill all processes matching the given name. Force kill if specified."""
    try:
        found = False
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'].lower() == name.lower():
                process_info = get_process_info(process.info['pid'])
                if process_info:
                    if force:
                        process.kill()
                        log_message(f"Force killed process with name {name} (PID: {process.info['pid']}).")
                    else:
                        process.terminate()
                        process.wait()
                        log_message(f"Process with name {name} (PID: {process.info['pid']}) has been terminated.")
                    found = True
        if not found:
            log_message(f"No processes found with the name {name}.")
    except psutil.NoSuchProcess:
        log_message(f"No process found with the name {name}.")
    except psutil.AccessDenied:
        log_message(f"Access denied to kill process with name {name}. Try running the script as an administrator or root.")
    except psutil.ZombieProcess:
        log_message(f"Process with name {name} is a zombie and cannot be terminated.")
    except Exception as e:
        log_message(f"An error occurred: {e}")


def kill_process_by_name_interactive():
    """Interactive process kill by name."""
    name = input("Enter process name to kill: ")
    force = input("Force kill? (y/n): ").lower() == 'y'
    kill_process_by_name(name, force)


def check_memory_usage_by_pid_interactive():
    """Check memory usage by PID interactively."""
    pid = int(input("Enter PID to check memory usage: "))
    process_info = get_process_info(pid)
    if process_info:
        log_message(f"Memory usage of PID {pid}: {process_info['Memory']} MB")


def check_memory_usage_by_name_interactive():
    """Check memory usage by process name interactively."""
    name = input("Enter process name to check memory usage: ")
    list_processes_by_name(name)


def shutdown_system_and_exit():
    """Shutdown system and exit interactive mode."""
    shutdown_system()
    log_message("Exiting interactive mode.")


def exit_interactive_mode():
    """Exit interactive mode."""
    log_message("Exiting interactive mode.")
    sys.exit(0)


def main():
    """Main function to choose whether to kill by PID or name."""
    if len(sys.argv) < 3:
        log_message("Usage: python process_killer.py <name_or_pid> <kill_type>")
        sys.exit(1)

    target = sys.argv[1]
    kill_type = sys.argv[2].lower()

    if kill_type == 'pid':
        try:
            pid = int(target)
            kill_process_by_pid(pid)
        except ValueError:
            log_message("Invalid PID value. Please enter a valid PID.")
    elif kill_type == 'name':
        kill_process_by_name(target)
    else:
        log_message("Invalid kill type. Use 'pid' or 'name'.")


if __name__ == '__main__':
    check_psutil_version()
    check_os_and_warn()

    if len(sys.argv) == 1:
        interactive_mode()
    else:
        main()
