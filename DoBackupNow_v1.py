# Project: Python Backup System using 7zip
# Name: DoBackupNow
# Author: Francisco Barboza
# Date: 05/16/2024 - 11:15
# Release:
#   1.0 - Backup
#   1.0.1 - Incremental added

import os
import json
import datetime
import subprocess

# Full path to the 7-Zip executable
SEVEN_ZIP_PATH = r"C:/Program Files/7-Zip/7z.exe"

def get_absolute_path(file_name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

def load_config(config_file):
    config_path = get_absolute_path(config_file)
    if not os.path.exists(config_path):
        print(f"Configuration file {config_path} not found.")
        return None
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

def load_last_backup(last_backup_file):
    if os.path.exists(last_backup_file):
        with open(last_backup_file, 'r') as file:
            last_backup_info = json.load(file)
        return datetime.datetime.fromisoformat(last_backup_info.get("last_backup"))
    return None

def save_last_backup(last_backup_file, timestamp):
    with open(last_backup_file, 'w') as file:
        json.dump({"last_backup": timestamp.isoformat()}, file)

def get_modified_files(source_dirs, last_backup_time):
    modified_files = []
    for source_dir in source_dirs:
        if os.path.exists(source_dir):
            for foldername, subfolders, filenames in os.walk(source_dir):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_mtime > last_backup_time:
                        modified_files.append(file_path)
    return modified_files

def create_backup(source_dirs, backup_dest, incremental, last_backup_time):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_name = f"backup_{timestamp}.7z"
    backup_path = os.path.join(backup_dest, backup_name)
    
    if incremental:
        modified_files = get_modified_files(source_dirs, last_backup_time)
        if not modified_files:
            for source_dir in source_dirs:
                log_backup(f"No files modified since the last backup from the {source_dir}.")
            return
        files_to_backup = modified_files
    else:
        files_to_backup = []
        for source_dir in source_dirs:
            if os.path.exists(source_dir):
                for foldername, subfolders, filenames in os.walk(source_dir):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        files_to_backup.append(file_path)

    files_to_backup_str = " ".join(f'"{file}"' for file in files_to_backup)
    command = f'"{SEVEN_ZIP_PATH}" a "{backup_path}" {files_to_backup_str}'
    try:
        subprocess.run(command, check=True, shell=True)
        log_backup(f"Successfully backed up to {backup_path} from {source_dir}")
    except subprocess.CalledProcessError as e:
        log_backup(f"Error during backup: {e}")

    return backup_path

def log_backup(message):
    with open("backup.log", "a") as log_file:
        log_file.write(f"{datetime.datetime.now()}: {message}\n")

def main():
    config = load_config("config.json")
    last_backup_time = load_last_backup("last_backup.json") or datetime.datetime.min
    backup_groups = config.get("backup_groups", [])

    if not backup_groups:
        print("Configuration is missing backup groups.")
        return

    for group in backup_groups:
        source_dirs = group.get("source_directories", [])
        backup_dest = group.get("backup_destination", "")
        incremental = group.get("incremental", False)

        if source_dirs and backup_dest:
            create_backup(source_dirs, backup_dest, incremental, last_backup_time)
        else:
            log_backup("Invalid configuration for group: " + str(group))
    
    save_last_backup("last_backup.json", datetime.datetime.now())

if __name__ == "__main__":
    main()
