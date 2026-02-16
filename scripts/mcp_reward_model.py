# Copyright (c) 2026, NVIDIA CORPORATION.  All rights reserved.
# NeMo RL Reward Model for Atlassian MCP Tool Use

import re
import json

class MCPRewardModel:
    """
    A custom reward logic provider that scores LLM outputs based on their
    adherence to Atlassian MCP (Model Context Protocol) schemas and reasoning depth.
    """

    def __init__(self):
        # Define expected tool schemas (simplified for demo)
        self.valid_tools = {
            "jira.update_issue": ["id", "comment"],
            "confluence.search": ["query"],
            "confluence.create_content": ["title", "space", "body"]
        }

    def score_response(self, text):
        """
        Returns a scalar reward score between -1 and 1.
        """
        reward = 0.0
        
        # 1. Check for Tool Call syntax (e.g., calling a method)
        tool_calls = re.findall(r"(\w+\.\w+)\((.*?)\)", text)
        
        if not tool_calls:
            # Penalize lack of action when action is requested
            return -0.5

        for tool_name, args_str in tool_calls:
            # 2. Reward known Atlassian MCP tools
            if tool_name in self.valid_tools:
                reward += 0.3
                
                # 3. Check for mandatory parameter presence
                required = self.valid_tools[tool_name]
                if all(param in args_str for param in required):
                    reward += 0.4
                else:
                    reward -= 0.2 # Missing params
            else:
                reward -= 0.3 # Hallucinated tool

        # 4. Reward Multi-step Reasoning (Chain of Thought)
        if "1." in text and "2." in text and len(tool_calls) > 1:
            # Reward for sequential tool use (e.g., search before update)
            reward += 0.3

        return min(max(reward, -1.0), 1.0)

def main():
    rm = MCPRewardModel()
    
    # Test cases for the Reward Model
    good_response = "1. Call confluence.search(query='incident')\n2. jira.update_issue(id='PROJ-1', comment='Fixed')"
    bad_response = "I will fix the Jira ticket for you now."
    hallucinated = "atlassian.fix_everything(now=true)"

    print(f"Reward (Good): {rm.score_response(good_response)}")
    print(f"Reward (Vague): {rm.score_response(bad_response)}")
    print(f"Reward (Fake): {rm.score_response(hallucinated)}")

if __name__ == "__main__":
    main()
