import os
import json
import datetime
import subprocess

# Project: Sistema de Backup em Python usando o 7zip
# Name: DoBackupNow
# Author: Francisco Barboza
# Date: 16/05/2024 - 11:15
# Release: 
# 1.0 - Backup
# 1.0.1 - Inserido incremental


# Caminho completo para o executável do 7-Zip
SEVEN_ZIP_PATH = r"C:/Program Files/7-Zip/7z.exe"

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def get_backup_state(state_file):
    # Carrega o estado do último backup de um arquivo JSON
    if os.path.exists(state_file):
        with open(state_file, 'r') as file:
            return json.load(file)
    else:
        return {}

def update_backup_state(state_file, last_backup_time):
    # Atualiza o estado do último backup em um arquivo JSON
    state = {"last_backup_time": last_backup_time.isoformat()}
    with open(state_file, 'w') as file:
        json.dump(state, file)

def get_modified_files(source_dirs, last_backup_time):
    modified_files = []
    for source_dir in source_dirs:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if last_backup_time is None or os.path.getmtime(file_path) > last_backup_time.timestamp():
                    modified_files.append(file_path)
    return modified_files

def create_backup(source_dirs, backup_dest, state_file, incremental=False):
    timestamp = datetime.datetime.now()
    backup_name = f"backup_{timestamp.strftime('%Y%m%d%H%M%S')}.7z"
    backup_path = os.path.join(backup_dest, backup_name)

    state = get_backup_state(state_file)
    last_backup_time = datetime.datetime.fromisoformat(state.get("last_backup_time")) if "last_backup_time" in state else None
    
    source_files = get_modified_files(source_dirs, last_backup_time) if incremental else source_dirs
    
    if incremental and not source_files:
        log_backup("Nenhum arquivo modificado para backup.")
        return
    
    source_files_str = " ".join(f'"{source_file}"' for source_file in source_files if os.path.exists(source_file))
    if not source_files_str:
        log_backup("Diretório origem inválido ou nenhum arquivo modificado.")
        return
    
    command = f'"{SEVEN_ZIP_PATH}" a "{backup_path}" {source_files_str}'
    try:
        subprocess.run(command, check=True, shell=True)
        log_backup(f"Backup realizado com sucesso {source_dirs} para {backup_path}")
        update_backup_state(state_file, timestamp)
    except subprocess.CalledProcessError as e:
        log_backup(f"Erro durante o backup: {e}")

def log_backup(message):
    with open("backup.log", "a") as log_file:
        log_file.write(f"{datetime.datetime.now()}: {message}\n")

def main():
    config = load_config("config.json")
    backup_groups = config.get("backup_groups", [])

    if not backup_groups:
        print("Configuração faltando para o grupo de backup.")
        return

    for group in backup_groups:
        source_dirs = group.get("source_directories", [])
        backup_dest = group.get("backup_destination", "")
        state_file = os.path.join(backup_dest, "backup_state.json")

        if source_dirs and backup_dest:
            create_backup(source_dirs, backup_dest, state_file, incremental=True)
        else:
            log_backup("Configuração inválida do grupo: " + str(group))

if __name__ == "__main__":
    main()
