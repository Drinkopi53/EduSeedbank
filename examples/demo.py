"""
Example usage of EduSeedbank system.

This script demonstrates how to use the EduSeedbank system to create educational content packages,
compress videos, generate HTML content, and simulate network distribution.
"""

import os
import sys
import tempfile

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from eduseedbank.packaging.core import PackagingSystem, SeedPackage
from eduseedbank.packaging.html_generator import HTMLGenerator
from eduseedbank.compression.video import VideoCompressor
from eduseedbank.network.lora import LoRaNetwork, LoRaNode, MessageType, Message


def demonstrate_packaging():
    """Demonstrate the content packaging system."""
    print("=== Demonstrating Content Packaging System ===")
    
    # Create packaging system
    packaging_system = PackagingSystem()
    
    # Create a sample package
    package = packaging_system.create_package(
        title="Matematika Dasar untuk Petani",
        description="Materi matematika dasar yang relevan dengan kegiatan pertanian",
        curriculum="Jawa Tengah",
        subject="Matematika"
    )
    
    print(f"Created package: {package.title}")
    print(f"Description: {package.description}")
    print(f"Curriculum: {package.curriculum}")
    print(f"Subject: {package.subject}")
    
    # Create a temporary file to add to the package
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("Ini adalah contoh materi pendidikan untuk petani.")
        temp_file_path = f.name
    
    try:
        # Add file to package
        package.add_file(temp_file_path, "materi.txt")
        print(f"Added file to package: {len(package.files)} file(s)")
        
        # Save package
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "matematika_dasar")
            package_path = package.save(output_path)
            print(f"Package saved to: {package_path}")
    finally:
        # Clean up temporary file
        os.unlink(temp_file_path)


def demonstrate_html_generation():
    """Demonstrate the HTML content generation."""
    print("\n=== Demonstrating HTML Generation ===")
    
    generator = HTMLGenerator()
    
    # Create sample content
    title = "Pengantar Matematika untuk Pertanian"
    content = """
    <p>Matematika memiliki peran penting dalam kegiatan pertanian, terutama dalam perhitungan:</p>
    <ul>
        <li>Luas lahan</li>
        <li>Jumlah pupuk yang dibutuhkan</li>
        <li>Perkiraan hasil panen</li>
        <li>Analisis keuntungan</li>
    </ul>
    <p>Dengan memahami konsep dasar matematika, petani dapat membuat keputusan yang lebih baik untuk usahanya.</p>
    """
    
    # Create sample exercises
    exercises = [
        {
            "question": "Jika seorang petani memiliki lahan berbentuk persegi panjang dengan panjang 20 meter dan lebar 15 meter, berapa luas lahannya?",
            "options": ["300 m²", "350 m²", "250 m²", "400 m²"],
            "correct_answer": "300 m²"
        },
        {
            "question": "Seorang petani membeli 50 kg pupuk dengan harga Rp100.000. Berapa harga per kilogram pupuk tersebut?",
            "options": ["Rp1.000/kg", "Rp2.000/kg", "Rp1.500/kg", "Rp2.500/kg"],
            "correct_answer": "Rp2.000/kg"
        }
    ]
    
    # Generate HTML
    html_content = generator.create_interactive_page(title, content, exercises)
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(html_content)
        html_file_path = f.name
    
    print(f"HTML content generated and saved to: {html_file_path}")
    print("You can open this file in a web browser to view the interactive content.")
    
    # Clean up
    os.unlink(html_file_path)


def demonstrate_network():
    """Demonstrate the LoRa network simulation."""
    print("\n=== Demonstrating LoRa Network Simulation ===")
    
    # Create a network
    network = LoRaNetwork()
    
    # Create nodes
    gateway = LoRaNode("gateway", is_gateway=True)
    school = LoRaNode("desa_jateng")
    farmer_node = LoRaNode("petani_001")
    
    # Add nodes to network
    network.add_node(gateway)
    network.add_node(school)
    network.add_node(farmer_node)
    
    # Connect nodes
    gateway.connect_to_node(school)
    gateway.connect_to_node(farmer_node)
    school.connect_to_node(gateway)
    farmer_node.connect_to_node(gateway)
    
    # Store a sample seed in the gateway
    sample_seed = {
        "title": "Matematika Dasar untuk Petani",
        "description": "Materi matematika dasar yang relevan dengan kegiatan pertanian",
        "subject": "Matematika",
        "curriculum": "Jawa Tengah",
        "files": ["materi.html", "latihan.html"]
    }
    gateway.store_seed("matematika_dasar_v1", sample_seed)
    
    print(f"Gateway has seeds: {list(gateway.seed_storage.keys())}")
    print(f"School has seeds: {list(school.seed_storage.keys())}")
    
    # Simulate a seed request from a school
    request_payload = {
        "seed_id": "matematika_dasar_v1"
    }
    
    request_msg = Message(
        msg_type=MessageType.SEED_REQUEST,
        source="desa_jateng",
        destination="gateway",
        payload=request_payload,
        timestamp=1000
    )
    
    school.send_message(request_msg)
    network.simulate_network_traffic()
    
    print(f"School now has seeds: {list(school.seed_storage.keys())}")
    if "matematika_dasar_v1" in school.seed_storage:
        print("Seed successfully transferred to school!")


def main():
    """Run all demonstrations."""
    print("EduSeedbank Example Usage")
    print("=" * 50)
    
    try:
        demonstrate_packaging()
        demonstrate_html_generation()
        demonstrate_network()
        
        print("\n=== All demonstrations completed successfully! ===")
        print("\nTo try the CLI interface, run:")
        print("  python -m eduseedbank.cli.main --help")
    except Exception as e:
        print(f"Error during demonstration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()