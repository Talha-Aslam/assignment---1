"""
File Manager utility for handling data persistence
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, List, Any


class FileManager:
    """
    Handles file operations for the portal system.
    Manages data persistence, backup, and recovery.
    """
    
    def __init__(self, data_directory="data"):
        """
        Initialize FileManager.
        
        Args:
            data_directory (str): Directory to store data files
        """
        self.data_dir = data_directory
        self.file_paths = {
            'users': os.path.join(data_directory, 'users.json'),
            'courses': os.path.join(data_directory, 'courses.json'),
            'records': os.path.join(data_directory, 'academic_records.json'),
            'salary_slips': os.path.join(data_directory, 'salary_slips.json'),
            'system_logs': os.path.join(data_directory, 'system_logs.json'),
            'config': os.path.join(data_directory, 'config.json')
        }
        self.backup_dir = os.path.join(data_directory, 'backups')
        self.initialize_files()
    
    def initialize_files(self):
        """Create data directory and initialize files if they don't exist."""
        # Create data directory
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Initialize files with empty data structures
        default_data = {
            'users': [],
            'courses': [],
            'records': {},
            'salary_slips': [],
            'system_logs': [],
            'config': {
                'version': '1.0',
                'created': datetime.now().isoformat(),
                'last_backup': None
            }
        }
        
        for file_type, file_path in self.file_paths.items():
            if not os.path.exists(file_path):
                self.save_data(file_type, default_data[file_type])
                print(f"Initialized {file_path}")
    
    def save_data(self, file_type: str, data: Any) -> bool:
        """
        Save data to specified file.
        
        Args:
            file_type (str): Type of file ('users', 'courses', etc.)
            data: Data to save
            
        Returns:
            bool: True if save successful, False otherwise
        """
        if file_type not in self.file_paths:
            print(f"Unknown file type: {file_type}")
            return False
        
        try:
            file_path = self.file_paths[file_type]
            
            # Create backup before saving
            if os.path.exists(file_path):
                self._create_backup(file_type)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False, default=str)
            
            return True
            
        except Exception as e:
            print(f"Error saving {file_type} data: {e}")
            return False
    
    def load_data(self, file_type: str) -> Any:
        """
        Load data from specified file.
        
        Args:
            file_type (str): Type of file to load
            
        Returns:
            Data from file, or empty structure if file doesn't exist
        """
        if file_type not in self.file_paths:
            print(f"Unknown file type: {file_type}")
            return None
        
        try:
            file_path = self.file_paths[file_type]
            
            if not os.path.exists(file_path):
                print(f"File {file_path} does not exist. Initializing with empty data.")
                return [] if file_type != 'records' else {}
            
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
                
        except Exception as e:
            print(f"Error loading {file_type} data: {e}")
            return [] if file_type != 'records' else {}
    
    def _create_backup(self, file_type: str) -> bool:
        """
        Create backup of specified file.
        
        Args:
            file_type (str): Type of file to backup
            
        Returns:
            bool: True if backup successful, False otherwise
        """
        try:
            source_path = self.file_paths[file_type]
            if not os.path.exists(source_path):
                return False
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{file_type}_{timestamp}.json"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            shutil.copy2(source_path, backup_path)
            return True
            
        except Exception as e:
            print(f"Error creating backup for {file_type}: {e}")
            return False
    
    def backup_data(self) -> bool:
        """
        Create backup of all data files.
        
        Returns:
            bool: True if all backups successful, False otherwise
        """
        print("Creating system backup...")
        success_count = 0
        
        for file_type in self.file_paths.keys():
            if file_type != 'config':  # Skip config file
                if self._create_backup(file_type):
                    success_count += 1
        
        # Update config with backup timestamp
        config_data = self.load_data('config')
        config_data['last_backup'] = datetime.now().isoformat()
        self.save_data('config', config_data)
        
        total_files = len(self.file_paths) - 1  # Exclude config
        print(f"Backup completed: {success_count}/{total_files} files backed up")
        
        return success_count == total_files
    
    def restore_from_backup(self, file_type: str, backup_timestamp: str) -> bool:
        """
        Restore file from backup.
        
        Args:
            file_type (str): Type of file to restore
            backup_timestamp (str): Timestamp of backup to restore
            
        Returns:
            bool: True if restore successful, False otherwise
        """
        try:
            backup_filename = f"{file_type}_{backup_timestamp}.json"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            if not os.path.exists(backup_path):
                print(f"Backup file {backup_filename} not found")
                return False
            
            current_path = self.file_paths[file_type]
            shutil.copy2(backup_path, current_path)
            
            print(f"Restored {file_type} from backup {backup_timestamp}")
            return True
            
        except Exception as e:
            print(f"Error restoring {file_type} from backup: {e}")
            return False
    
    def list_backups(self, file_type: str = None) -> List[str]:
        """
        List available backups.
        
        Args:
            file_type (str): Filter by file type (optional)
            
        Returns:
            list: List of backup files
        """
        try:
            if not os.path.exists(self.backup_dir):
                return []
            
            backup_files = []
            for filename in os.listdir(self.backup_dir):
                if filename.endswith('.json'):
                    if file_type is None or filename.startswith(f"{file_type}_"):
                        backup_files.append(filename)
            
            return sorted(backup_files, reverse=True)  # Most recent first
            
        except Exception as e:
            print(f"Error listing backups: {e}")
            return []
    
    def cleanup_old_backups(self, days_to_keep: int = 30) -> int:
        """
        Remove backups older than specified days.
        
        Args:
            days_to_keep (int): Number of days to keep backups
            
        Returns:
            int: Number of files deleted
        """
        try:
            if not os.path.exists(self.backup_dir):
                return 0
            
            cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
            deleted_count = 0
            
            for filename in os.listdir(self.backup_dir):
                file_path = os.path.join(self.backup_dir, filename)
                if os.path.isfile(file_path):
                    file_time = os.path.getmtime(file_path)
                    if file_time < cutoff_time:
                        os.remove(file_path)
                        deleted_count += 1
            
            print(f"Cleaned up {deleted_count} old backup files")
            return deleted_count
            
        except Exception as e:
            print(f"Error cleaning up backups: {e}")
            return 0
    
    def get_file_info(self, file_type: str) -> Dict[str, Any]:
        """
        Get information about a data file.
        
        Args:
            file_type (str): Type of file
            
        Returns:
            dict: File information
        """
        if file_type not in self.file_paths:
            return {}
        
        file_path = self.file_paths[file_type]
        
        if not os.path.exists(file_path):
            return {'exists': False}
        
        try:
            stat = os.stat(file_path)
            return {
                'exists': True,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'path': file_path
            }
        except Exception as e:
            return {'exists': True, 'error': str(e)}
    
    def export_data(self, export_path: str) -> bool:
        """
        Export all data to a single file.
        
        Args:
            export_path (str): Path to export file
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'data': {}
            }
            
            for file_type in self.file_paths.keys():
                export_data['data'][file_type] = self.load_data(file_type)
            
            with open(export_path, 'w', encoding='utf-8') as file:
                json.dump(export_data, file, indent=2, ensure_ascii=False, default=str)
            
            print(f"Data exported to {export_path}")
            return True
            
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
    
    def import_data(self, import_path: str) -> bool:
        """
        Import data from exported file.
        
        Args:
            import_path (str): Path to import file
            
        Returns:
            bool: True if import successful, False otherwise
        """
        try:
            if not os.path.exists(import_path):
                print(f"Import file {import_path} not found")
                return False
            
            with open(import_path, 'r', encoding='utf-8') as file:
                import_data = json.load(file)
            
            if 'data' not in import_data:
                print("Invalid import file format")
                return False
            
            # Create backup before import
            self.backup_data()
            
            # Import data
            for file_type, data in import_data['data'].items():
                if file_type in self.file_paths:
                    self.save_data(file_type, data)
            
            print(f"Data imported from {import_path}")
            return True
            
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
