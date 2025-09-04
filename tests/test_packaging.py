"""
Tests for EduSeedbank packaging system.
"""

import os
import sys
import tempfile
import pytest

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from eduseedbank.packaging.core import PackagingSystem, SeedPackage


def test_create_package():
    """Test creating a new seed package."""
    packaging_system = PackagingSystem()
    package = packaging_system.create_package(
        title="Test Package",
        description="A test educational package",
        curriculum="Jawa Barat",
        subject="Science"
    )
    
    assert package.title == "Test Package"
    assert package.description == "A test educational package"
    assert package.curriculum == "Jawa Barat"
    assert package.subject == "Science"
    assert len(package.files) == 0


def test_add_file_to_package():
    """Test adding a file to a package."""
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("Test content")
        temp_file_path = f.name
    
    try:
        package = SeedPackage(
            title="Test Package",
            description="A test educational package",
            curriculum="Jawa Barat",
            subject="Science"
        )
        
        package.add_file(temp_file_path, "test.txt")
        assert len(package.files) == 1
        assert package.files[0]["source"] == temp_file_path
        assert package.files[0]["destination"] == "test.txt"
    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)


def test_save_package():
    """Test saving a package as a zip file."""
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("Test content")
        temp_file_path = f.name
    
    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            package = SeedPackage(
                title="Test Package",
                description="A test educational package",
                curriculum="Jawa Barat",
                subject="Science"
            )
            
            package.add_file(temp_file_path, "test.txt")
            output_path = os.path.join(temp_dir, "test_package")
            package_path = package.save(output_path)
            
            # Check that the package file was created
            assert os.path.exists(package_path)
            assert package_path.endswith(".seed")
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)