import os
import shutil
import tarfile
from datetime import datetime

# Function to perform the backup
def perform_backup(source_dir, backup_dir, compress=False, compression_format='zip'):
    # Create the backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    previous_backup_dir = os.path.join(backup_dir, 'current_backup')
    # Remove the previous backup if it exists
    if os.path.exists(previous_backup_dir):
        shutil.rmtree(previous_backup_dir)
    
    current_backup_dir = os.path.join(backup_dir, 'current_backup')
    # Create the current backup directory
    os.makedirs(current_backup_dir)

    # Walk through the source directory and copy files to the backup directory
    for root, dirs, files in os.walk(source_dir):
        relative_path = os.path.relpath(root, source_dir)
        dest_dir = os.path.join(current_backup_dir, relative_path)

        # Create destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Copy files from source to destination
        for file in files:
            source_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)

            # Only copy the file if it doesn't exist in the destination or if it's been modified
            if not os.path.exists(dest_file) or os.path.getmtime(source_file) > os.path.getmtime(dest_file):
                shutil.copy2(source_file, dest_file)

    # If compression is requested
    if compress:
        # Generate the output filename based on the current timestamp
        output_filename = os.path.join(backup_dir, 'current_backup')
        # Compress the backup
        compress_backup(current_backup_dir, output_filename, compression_format)
        # Remove the uncompressed backup directory
        shutil.rmtree(current_backup_dir)
        print(f"Backup completed successfully. Compressed backup stored in: {output_filename}.{compression_format}")

    else:
        # If no compression, notify that the backup is complete
        print(f"Backup completed successfully. Backup stored in: {current_backup_dir}")



# Function to compress the backup directory
def compress_backup(source_dir, output_filename, compression_format):
    if compression_format == 'zip':
        # Create a zip archive
        shutil.make_archive(output_filename, 'zip', source_dir)
    elif compression_format == 'tar.gz':
        # Create a tar.gz archive
        with tarfile.open(output_filename + '.tar.gz', 'w:gz') as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
    elif compression_format == 'tar.bz2':
        # Create a tar.bz2 archive
        with tarfile.open(output_filename + '.tar.bz2', 'w:bz2') as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
    else:
        # Raise an error if an unsupported compression format is specified
        raise ValueError("Unsupported compression format. Choose 'zip', 'tar.gz', or 'tar.bz2'.")