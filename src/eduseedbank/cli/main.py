"""
Command-line interface for EduSeedbank.
Provides tools for content packaging and network management.
"""

import click
import os
import sys

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from eduseedbank.packaging.core import PackagingSystem, SeedPackage
from eduseedbank.packaging.html_generator import HTMLGenerator
from eduseedbank.compression.video import VideoCompressor
from eduseedbank.network.lora import LoRaNetwork, LoRaNode, MessageType, Message
from eduseedbank.server.local_server import LocalServer


@click.group()
def main():
    """EduSeedbank CLI - Generate and distribute offline educational content."""
    pass


@main.command()
@click.option("--title", prompt="Title", help="Title of the educational content")
@click.option("--description", prompt="Description", help="Description of the content")
@click.option("--curriculum", prompt="Curriculum", help="Regional curriculum")
@click.option("--subject", prompt="Subject", help="Educational subject")
@click.option("--output", prompt="Output path", help="Output path for the seed package")
def create_package(title: str, description: str, curriculum: str, subject: str, output: str):
    """Create a new educational content package."""
    try:
        packaging_system = PackagingSystem()
        package = packaging_system.create_package(title, description, curriculum, subject)
        
        # For now, we'll just save an empty package
        # In a real implementation, we would add files to the package
        package_path = package.save(output)
        click.echo(f"Package created successfully: {package_path}")
    except Exception as e:
        click.echo(f"Error creating package: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--input", prompt="Input video path", help="Path to input video file")
@click.option("--output", prompt="Output video path", help="Path for compressed video")
@click.option("--size", default=5, help="Target size in MB (default: 5)")
def compress_video(input: str, output: str, size: int):
    """Compress a video for LoRa transmission."""
    try:
        compressor = VideoCompressor()
        if compressor.compress_video(input, output, size):
            click.echo(f"Video compressed successfully: {output}")
        else:
            click.echo("Error compressing video", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error compressing video: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--title", prompt="Page title", help="Title of the HTML page")
@click.option("--content", prompt="Content", help="Main content (HTML format)")
@click.option("--output", prompt="Output path", help="Output path for HTML file")
def create_html(title: str, content: str, output: str):
    """Create an interactive HTML educational page."""
    try:
        generator = HTMLGenerator()
        html_content = generator.create_interactive_page(title, content)
        if generator.save_page(html_content, output):
            click.echo(f"HTML page created successfully: {output}")
        else:
            click.echo("Error creating HTML page", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error creating HTML page: {e}", err=True)
        sys.exit(1)


@main.command()
def simulate_network():
    """Simulate a LoRa mesh network with sample nodes."""
    try:
        # Create a network
        network = LoRaNetwork()
        
        # Create nodes
        gateway = LoRaNode("gateway", is_gateway=True)
        school1 = LoRaNode("school1")
        school2 = LoRaNode("school2")
        farmer_node = LoRaNode("farmer")
        
        # Add nodes to network
        network.add_node(gateway)
        network.add_node(school1)
        network.add_node(school2)
        network.add_node(farmer_node)
        
        # Connect nodes (simplified mesh)
        gateway.connect_to_node(school1)
        gateway.connect_to_node(school2)
        gateway.connect_to_node(farmer_node)
        school1.connect_to_node(gateway)
        school2.connect_to_node(gateway)
        farmer_node.connect_to_node(gateway)
        
        # Store a sample seed in the gateway
        sample_seed = {
            "title": "Sample Educational Content",
            "description": "A sample seed for demonstration",
            "subject": "Science",
            "files": ["content1.html", "video1.mp4"]
        }
        gateway.store_seed("sample1", sample_seed)
        
        # Simulate a seed request from a school
        request_payload = {
            "seed_id": "sample1"
        }
        
        request_msg = Message(
            msg_type=MessageType.SEED_REQUEST,
            source="school1",
            destination="gateway",
            payload=request_payload,
            timestamp=1000
        )
        
        school1.send_message(request_msg)
        network.simulate_network_traffic()
        
        click.echo("Network simulation completed successfully")
        click.echo(f"School1 now has seeds: {list(school1.seed_storage.keys())}")
        
    except Exception as e:
        click.echo(f"Error in network simulation: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--host", default="127.0.0.1", help="Host to run the server on")
@click.option("--port", default=8080, help="Port to run the server on")
def run_server(host: str, port: int):
    """Run the local EduSeedbank server."""
    try:
        server = LocalServer(host=host, port=port)
        click.echo(f"Starting EduSeedbank server on {host}:{port}")
        server.run()
    except Exception as e:
        click.echo(f"Error starting server: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()