import file_backup

source_directory = ''
backup_directory_path = ''
file_backup.perform_backup(source_directory, backup_directory_path, compress=True, compression_format='zip')