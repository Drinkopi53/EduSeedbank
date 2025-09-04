"""
Local server implementation for EduSeedbank.
Serves content to school devices and manages user accounts.
"""

import os
import json
from flask import Flask, render_template, send_file, request, jsonify
from typing import Dict, List


class LocalServer:
    """Local server for EduSeedbank that serves educational content."""

    def __init__(self, content_dir: str = "content", host: str = "127.0.0.1", port: int = 8080):
        self.content_dir = content_dir
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.seeds = {}  # In-memory storage of planted seeds
        self._setup_routes()
        
    def _setup_routes(self):
        """Set up Flask routes for the server."""
        
        @self.app.route("/")
        def home():
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>EduSeedbank Local Server</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    h1 { color: #2c3e50; }
                    .seed { 
                        border: 1px solid #ddd; 
                        padding: 15px; 
                        margin: 10px 0; 
                        border-radius: 5px;
                        background-color: #f9f9f9;
                    }
                </style>
            </head>
            <body>
                <h1>EduSeedbank Local Server</h1>
                <p>Server lokal untuk konten edukatif offline.</p>
                
                <h2>Bibit yang Ditanam:</h2>
                <div id="seeds-list">
                    <!-- Seeds will be listed here -->
                </div>
                
                <script>
                    // In a real implementation, this would fetch from the server
                    document.getElementById('seeds-list').innerHTML = '<p>Belum ada bibit yang ditanam.</p>';
                </script>
            </body>
            </html>
            """
            
        @self.app.route("/api/seeds")
        def list_seeds():
            """API endpoint to list all planted seeds."""
            return jsonify(list(self.seeds.keys()))
            
        @self.app.route("/api/seeds/<seed_id>")
        def get_seed(seed_id):
            """API endpoint to get information about a specific seed."""
            if seed_id in self.seeds:
                return jsonify(self.seeds[seed_id])
            else:
                return jsonify({"error": "Seed not found"}), 404
                
        @self.app.route("/api/plant", methods=["POST"])
        def plant_seed():
            """API endpoint to plant a new seed."""
            # In a real implementation, this would handle the actual planting
            # of a seed file
            data = request.get_json()
            seed_id = data.get("seed_id", "unknown")
            seed_data = data.get("seed_data", {})
            
            self.seeds[seed_id] = seed_data
            return jsonify({"status": "success", "message": f"Seed {seed_id} planted successfully"})
            
        @self.app.route("/content/<path:filename>")
        def serve_content(filename):
            """Serve educational content files."""
            # In a real implementation, this would securely serve content
            # from the content directory
            return f"Content file: {filename}"

    def plant_seed(self, seed_id: str, seed_data: Dict):
        """Plant a seed in the local server."""
        self.seeds[seed_id] = seed_data
        print(f"Planted seed: {seed_id}")
        
    def run(self, debug: bool = False):
        """Start the local server."""
        self.app.run(host=self.host, port=self.port, debug=debug)