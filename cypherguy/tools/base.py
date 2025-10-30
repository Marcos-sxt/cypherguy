"""
Base classes for agent tools
"""

from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class Tool(ABC):
    """Base class for all agent tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        logger.info(f"🔧 Tool initialized: {name}")
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool and return results
        
        Returns:
            Dict with at least:
            - success (bool): Whether execution succeeded
            - Additional fields depending on the tool
        """
        pass
    
    def __str__(self):
        return f"Tool({self.name})"
    
    def __repr__(self):
        return f"<Tool name='{self.name}' description='{self.description}'>"


class ToolRegistry:
    """Central registry for all tools"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        logger.info("🏭 ToolRegistry initialized")
    
    def register(self, tool: Tool) -> None:
        """Register a new tool"""
        self.tools[tool.name] = tool
        logger.info(f"✅ Registered tool: {tool.name}")
    
    async def execute(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool by name
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Arguments to pass to the tool
        
        Returns:
            Tool execution result
        
        Raises:
            ValueError: If tool not found
        """
        if tool_name not in self.tools:
            available = ", ".join(self.tools.keys())
            raise ValueError(
                f"Tool '{tool_name}' not found. "
                f"Available tools: {available}"
            )
        
        logger.info(f"⚙️ Executing tool: {tool_name}")
        
        try:
            result = await self.tools[tool_name].execute(**kwargs)
            logger.info(f"✅ Tool {tool_name} completed successfully")
            return result
        except Exception as e:
            logger.error(f"❌ Tool {tool_name} failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name
            }
    
    def list_tools(self) -> List[Dict[str, str]]:
        """List all available tools"""
        return [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in self.tools.values()
        ]
    
    def has_tool(self, tool_name: str) -> bool:
        """Check if a tool is registered"""
        return tool_name in self.tools
    
    def __len__(self):
        return len(self.tools)
    
    def __repr__(self):
        return f"<ToolRegistry tools={len(self.tools)}>"

