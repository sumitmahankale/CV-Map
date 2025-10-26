"""
Module for simulating WhatsApp message reception
In production, this would use WhatsApp Business API or Twilio
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class WhatsAppMessage:
    """Represent a WhatsApp message with potential file attachment"""
    sender_id: str
    sender_name: str
    message_text: str
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    timestamp: Optional[str] = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class WhatsAppSimulator:
    """
    Simulates WhatsApp message reception
    In production, this would integrate with WhatsApp Business API
    """
    
    def __init__(self):
        """Initialize the WhatsApp simulator"""
        self.message_queue = []
        self.processed_messages = []
    
    def simulate_message_receipt(self, message: WhatsAppMessage) -> bool:
        """Add a simulated WhatsApp message to the queue"""
        self.message_queue.append(message)
        print(f"[WhatsApp Simulator] Received message from {message.sender_name}")
        if message.file_path:
            print(f"[WhatsApp Simulator] File attachment: {message.file_path}")
        return True
    
    def get_next_message(self) -> Optional[WhatsAppMessage]:
        """Get the next message from the queue"""
        if self.message_queue:
            message = self.message_queue.pop(0)
            self.processed_messages.append(message)
            return message
        return None
    
    def get_pending_messages(self) -> List[WhatsAppMessage]:
        """Get all pending messages"""
        return self.message_queue.copy()
    
    def clear_queue(self) -> None:
        """Clear the message queue"""
        self.message_queue.clear()
    
    def get_statistics(self) -> Dict:
        """Get statistics about processed messages"""
        return {
            'pending_messages': len(self.message_queue),
            'processed_messages': len(self.processed_messages),
            'total_messages': len(self.message_queue) + len(self.processed_messages)
        }


class WhatsAppMessageBuilder:
    """Builder class to construct WhatsApp messages"""
    
    def __init__(self):
        self.sender_id = None
        self.sender_name = None
        self.message_text = None
        self.file_path = None
        self.file_type = None
    
    def with_sender(self, sender_id: str, sender_name: str) -> 'WhatsAppMessageBuilder':
        """Set sender information"""
        self.sender_id = sender_id
        self.sender_name = sender_name
        return self
    
    def with_message(self, text: str) -> 'WhatsAppMessageBuilder':
        """Set message text"""
        self.message_text = text
        return self
    
    def with_file(self, file_path: str, file_type: str) -> 'WhatsAppMessageBuilder':
        """Set file attachment"""
        self.file_path = file_path
        self.file_type = file_type
        return self
    
    def build(self) -> WhatsAppMessage:
        """Build and return the WhatsApp message"""
        if not self.sender_id or not self.sender_name:
            raise ValueError("Sender ID and name are required")
        if not self.message_text:
            raise ValueError("Message text is required")
        
        return WhatsAppMessage(
            sender_id=self.sender_id,
            sender_name=self.sender_name,
            message_text=self.message_text,
            file_path=self.file_path,
            file_type=self.file_type
        )
