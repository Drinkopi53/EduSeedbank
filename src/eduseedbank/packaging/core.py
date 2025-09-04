"""
Content packaging system for EduSeedbank.
Handles the creation of educational content packages.
"""

import os
import json
import zipfile
from datetime import datetime
from typing import Dict, List, Optional


class SeedPackage:
    """Represents an educational content package (seed)."""

    def __init__(self, title: str, description: str, curriculum: str, subject: str):
        self.title = title
        self.description = description
        self.curriculum = curriculum  # Regional curriculum
        self.subject = subject
        self.created_at = datetime.now()
        self.files = []
        self.metadata = {
            "title": title,
            "description": description,
            "curriculum": curriculum,
            "subject": subject,
            "created_at": self.created_at.isoformat(),
            "version": "1.0"
        }

    def add_file(self, file_path: str, destination_path: str):
        """Add a file to the seed package."""
        if os.path.exists(file_path):
            self.files.append({
                "source": file_path,
                "destination": destination_path
            })
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    def save(self, output_path: str) -> str:
        """Save the seed package as a zip file."""
        # Create metadata file
        metadata_file = os.path.join(os.path.dirname(output_path), "metadata.json")
        with open(metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

        # Create zip file
        package_path = f"{output_path}.seed"
        with zipfile.ZipFile(package_path, 'w') as zipf:
            # Add metadata
            zipf.write(metadata_file, "metadata.json")
            
            # Add all files
            for file_info in self.files:
                if os.path.exists(file_info["source"]):
                    zipf.write(file_info["source"], file_info["destination"])
        
        # Clean up temporary metadata file
        if os.path.exists(metadata_file):
            os.remove(metadata_file)
            
        return package_path


class PackagingSystem:
    """Main packaging system for EduSeedbank."""

    def __init__(self):
        self.packages = []

    def create_package(self, title: str, description: str, 
                      curriculum: str, subject: str) -> SeedPackage:
        """Create a new seed package."""
        package = SeedPackage(title, description, curriculum, subject)
        self.packages.append(package)
        return package

    def list_packages(self) -> List[Dict]:
        """List all created packages."""
        return [{
            "title": pkg.title,
            "description": pkg.description,
            "curriculum": pkg.curriculum,
            "subject": pkg.subject,
            "created_at": pkg.created_at
        } for pkg in self.packages]