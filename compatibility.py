from typing import Dict, Any, Optional
from mcp.server.fastmcp import Context

class MCPCompatibilityLayer:
    def __init__(self):
        self.supported_versions = ["1.0", "1.1", "1.6"]
        self.client_version = "1.6"
        self.capabilities = {
            "tools": True,
            "resources": True,
            "prompts": True,
            "streaming": False
        }
    
    def detect_client_version(self, context: Optional[Context] = None) -> str:
        return self.client_version
    
    def negotiate_capabilities(self, client_caps: Dict[str, Any]) -> Dict[str, Any]:
        negotiated = {}
        for cap, supported in self.capabilities.items():
            negotiated[cap] = supported and client_caps.get(cap, False)
        return negotiated
    
    def adapt_response(self, response: Any, version: str) -> Any:
        if version in ["1.0", "1.1"]:
            if isinstance(response, dict) and "metadata" in response:
                response = {k: v for k, v in response.items() if k != "metadata"}
        return response