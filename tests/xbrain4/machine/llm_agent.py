import time
import json
import socket
import os
from dotenv import load_dotenv

load_dotenv()

class LLMAgent:
    def __init__(self, target=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if target is None:
            host = os.getenv("AGENT_TARGET_HOST", "127.0.0.1")
            port = int(os.getenv("AGENT_TARGET_PORT", 9999))
            self.target = (host, port)
        else:
            self.target = target

    def think_and_send(self):
        # Placeholder for real LLM logic
        decision = {"linear": 0.2, "angular": 0.0}
        self.sock.sendto(json.dumps(decision).encode(), self.target)
