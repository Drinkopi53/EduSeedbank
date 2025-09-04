"""
LoRa mesh networking functionality for EduSeedbank.
Handles communication between nodes in the network.

This is a simplified simulation of LoRa networking functionality.
In a real implementation, this would interface with actual LoRa hardware.
"""

import time
import random
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    SEED_REQUEST = "seed_request"
    SEED_RESPONSE = "seed_response"
    SEED_DATA = "seed_data"
    NETWORK_PING = "network_ping"
    NETWORK_PONG = "network_pong"


@dataclass
class Message:
    """Represents a message in the LoRa network."""
    msg_type: MessageType
    source: str
    destination: str
    payload: Dict
    timestamp: float


class LoRaNode:
    """Represents a node in the LoRa mesh network."""
    
    def __init__(self, node_id: str, is_gateway: bool = False):
        self.node_id = node_id
        self.is_gateway = is_gateway
        self.connected_nodes = []
        self.message_queue = []
        self.seed_storage = {}
        self.network = None  # Reference to the network this node belongs to
        
    def connect_to_node(self, node: 'LoRaNode'):
        """Connect to another node in the network."""
        if node not in self.connected_nodes:
            self.connected_nodes.append(node)
            
    def send_message(self, message: Message):
        """Send a message to the network."""
        # In a real implementation, this would send via LoRa radio
        # For simulation, we route through the network
        print(f"[{self.node_id}] Sending {message.msg_type.value} to {message.destination}")
        if self.network:
            self.network.route_message(message)
        
    def receive_message(self, message: Message):
        """Receive a message from the network."""
        print(f"[{self.node_id}] Received {message.msg_type.value} from {message.source}")
        
        if message.msg_type == MessageType.SEED_REQUEST:
            self._handle_seed_request(message)
        elif message.msg_type == MessageType.SEED_DATA:
            self._handle_seed_data(message)
        elif message.msg_type == MessageType.NETWORK_PING:
            self._handle_ping(message)
            
    def _handle_seed_request(self, message: Message):
        """Handle a seed request message."""
        seed_id = message.payload.get("seed_id")
        if seed_id in self.seed_storage:
            # Send the seed data back
            response_payload = {
                "seed_id": seed_id,
                "seed_data": self.seed_storage[seed_id]
            }
            
            response = Message(
                msg_type=MessageType.SEED_DATA,
                source=self.node_id,
                destination=message.source,
                payload=response_payload,
                timestamp=time.time()
            )
            
            self.send_message(response)
            
    def _handle_seed_data(self, message: Message):
        """Handle seed data message."""
        seed_id = message.payload.get("seed_id")
        seed_data = message.payload.get("seed_data")
        if seed_id and seed_data:
            self.seed_storage[seed_id] = seed_data
            print(f"[{self.node_id}] Stored seed {seed_id}")
            
    def _handle_ping(self, message: Message):
        """Handle network ping message."""
        # Respond with pong
        pong_payload = {
            "timestamp": message.payload.get("timestamp", time.time())
        }
        
        pong = Message(
            msg_type=MessageType.NETWORK_PONG,
            source=self.node_id,
            destination=message.source,
            payload=pong_payload,
            timestamp=time.time()
        )
        
        self.send_message(pong)
        
    def broadcast_message(self, message: Message):
        """Broadcast a message to all connected nodes."""
        for node in self.connected_nodes:
            # In a real implementation, this would use LoRa broadcast
            # For simulation, we directly call receive_message
            node.receive_message(message)
            
    def store_seed(self, seed_id: str, seed_data: Dict):
        """Store a seed in this node's storage."""
        self.seed_storage[seed_id] = seed_data
        print(f"[{self.node_id}] Stored seed {seed_id}")


class LoRaNetwork:
    """Manages the LoRa mesh network."""
    
    def __init__(self):
        self.nodes = {}
        
    def add_node(self, node: LoRaNode):
        """Add a node to the network."""
        self.nodes[node.node_id] = node
        node.network = self  # Set reference to this network
        
    def route_message(self, message: Message):
        """Route a message to its destination."""
        # In a simple simulation, we directly deliver to the destination
        if message.destination in self.nodes:
            self.nodes[message.destination].receive_message(message)
        else:
            print(f"Warning: Destination {message.destination} not found in network")
            
    def simulate_network_traffic(self):
        """Simulate network traffic by processing message queues."""
        # In this simple implementation, messages are delivered immediately
        # This method is kept for compatibility with the previous design
        pass
            
    def get_node(self, node_id: str) -> Optional[LoRaNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)