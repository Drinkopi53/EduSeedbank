"""
Complete workflow demonstration of EduSeedbank system.

This script demonstrates the entire workflow from content creation to distribution
and planting of educational seeds.
"""

import os
import sys
import tempfile
import shutil

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from eduseedbank.packaging.core import PackagingSystem, SeedPackage
from eduseedbank.packaging.html_generator import HTMLGenerator
from eduseedbank.network.lora import LoRaNetwork, LoRaNode, MessageType, Message
from eduseedbank.server.local_server import LocalServer


def create_educational_content():
    """Create educational content and package it as a seed."""
    print("=== Step 1: Creating Educational Content ===")
    
    # Create packaging system
    packaging_system = PackagingSystem()
    
    # Create a sample package
    package = packaging_system.create_package(
        title="Pengenalan Pertanian Berkelanjutan",
        description="Materi pengenalan tentang pertanian berkelanjutan dan praktik terbaik",
        curriculum="Jawa Barat",
        subject="Pertanian"
    )
    
    print(f"Created package: {package.title}")
    
    # Create HTML content
    generator = HTMLGenerator()
    
    content = """
    <h2>Apa itu Pertanian Berkelanjutan?</h2>
    <p>Pertanian berkelanjutan adalah pendekatan untuk menghasilkan pangan, serat, dan produk pertanian lainnya 
    dengan cara yang memenuhi kebutuhan saat ini tanpa membahayakan kemampuan generasi mendatang untuk 
    memenuhi kebutuhan mereka.</p>
    
    <h2>Prinsip Utama Pertanian Berkelanjutan</h2>
    <ul>
        <li><strong>Kelestarian Lingkungan:</strong> Melindungi kualitas tanah, air, dan udara</li>
        <li><strong>Ekonomi yang Menguntungkan:</strong> Menciptakan profit yang dapat dipertahankan</li>
        <li><strong>Kesejahteraan Sosial:</strong> Meningkatkan kualitas hidup petani dan masyarakat</li>
    </ul>
    """
    
    # Create exercises
    exercises = [
        {
            "question": "Apa tujuan utama dari pertanian berkelanjutan?",
            "options": [
                "Meningkatkan produksi sebanyak mungkin",
                "Memenuhi kebutuhan saat ini tanpa membahayakan generasi mendatang",
                "Mengurangi biaya produksi sepenuhnya",
                "Mengabaikan kualitas lingkungan"
            ],
            "correct_answer": "Memenuhi kebutuhan saat ini tanpa membahayakan generasi mendatang"
        }
    ]
    
    # Generate HTML
    html_content = generator.create_interactive_page(
        "Pengenalan Pertanian Berkelanjutan", 
        content, 
        exercises
    )
    
    # Save HTML to temporary file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(html_content)
        html_file_path = f.name
    
    # Add file to package
    package.add_file(html_file_path, "index.html")
    print(f"Added interactive HTML content to package")
    
    # Save package
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "pertanian_berkelanjutan")
        package_path = package.save(output_path)
        
        # Copy the package to a permanent location for the demo
        final_package_path = os.path.join(os.path.dirname(__file__), "pertanian_berkelanjutan.seed")
        shutil.copy2(package_path, final_package_path)
        print(f"Package saved as: {final_package_path}")
    
    # Clean up temporary files
    os.unlink(html_file_path)
    
    return final_package_path


def distribute_via_lora(package_path):
    """Simulate distribution of the seed package via LoRa network."""
    print("\n=== Step 2: Distributing via LoRa Network ===")
    
    # Create a network
    network = LoRaNetwork()
    
    # Create nodes
    gateway = LoRaNode("gateway", is_gateway=True)
    school = LoRaNode("sdn_1_cigadung")
    farmer_node = LoRaNode("petani_kopi")
    
    # Add nodes to network
    network.add_node(gateway)
    network.add_node(school)
    network.add_node(farmer_node)
    
    # Connect nodes
    gateway.connect_to_node(school)
    gateway.connect_to_node(farmer_node)
    school.connect_to_node(gateway)
    farmer_node.connect_to_node(gateway)
    
    # Store the seed in the gateway
    seed_data = {
        "title": "Pengenalan Pertanian Berkelanjutan",
        "description": "Materi pengenalan tentang pertanian berkelanjutan dan praktik terbaik",
        "subject": "Pertanian",
        "curriculum": "Jawa Barat",
        "files": ["index.html"]
    }
    gateway.store_seed("pertanian_berkelanjutan_v1", seed_data)
    print(f"Seed stored in gateway: pertanian_berkelanjutan_v1")
    
    # Simulate a seed request from a school
    request_payload = {
        "seed_id": "pertanian_berkelanjutan_v1"
    }
    
    request_msg = Message(
        msg_type=MessageType.SEED_REQUEST,
        source="sdn_1_cigadung",
        destination="gateway",
        payload=request_payload,
        timestamp=1000
    )
    
    school.send_message(request_msg)
    network.simulate_network_traffic()
    
    print(f"School now has seeds: {list(school.seed_storage.keys())}")
    if "pertanian_berkelanjutan_v1" in school.seed_storage:
        print("Seed successfully transferred to school!")
        return True
    else:
        print("Failed to transfer seed to school.")
        return False


def plant_seed_in_local_server():
    """Simulate planting the seed in a local school server."""
    print("\n=== Step 3: Planting Seed in Local Server ===")
    
    # Create a local server
    server = LocalServer()
    
    # Simulate planting the seed
    seed_data = {
        "title": "Pengenalan Pertanian Berkelanjutan",
        "description": "Materi pengenalan tentang pertanian berkelanjutan dan praktik terbaik",
        "subject": "Pertanian",
        "curriculum": "Jawa Barat",
        "files": ["index.html"]
    }
    
    server.plant_seed("pertanian_berkelanjutan_v1", seed_data)
    
    print("Seed planted successfully in local server!")
    print("Students can now access the educational content offline.")
    
    return True


def main():
    """Run the complete EduSeedbank workflow demonstration."""
    print("EduSeedbank Complete Workflow Demonstration")
    print("=" * 50)
    
    try:
        # Step 1: Create educational content
        package_path = create_educational_content()
        
        # Step 2: Distribute via LoRa
        distribution_success = distribute_via_lora(package_path)
        
        # Step 3: Plant in local server
        if distribution_success:
            planting_success = plant_seed_in_local_server()
            
            if planting_success:
                print("\n=== Workflow Completed Successfully! ===")
                print("The educational content is now available for students in the local school.")
                print("\nTo access the content:")
                print("1. Run the local server: python -m eduseedbank.cli.main run-server")
                print("2. Open a web browser and go to http://127.0.0.1:8080")
                print("3. Students can access the educational content without internet connection")
            else:
                print("\nError: Failed to plant seed in local server.")
        else:
            print("\nError: Failed to distribute seed via LoRa network.")
            
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()