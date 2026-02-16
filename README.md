# NeMo RL: Model Context Protocol (MCP) Alignment for Atlassian 🚀🧠

This project demonstrates how to use **NVIDIA NeMo RL** (PPO/DPO) to post-train an LLM, specifically improving its ability to utilize the **Atlassian Model Context Protocol (MCP)** for complex enterprise workflows.

## 🏦 The Mission
Standard LLMs often struggle with the precise JSON schemas, multi-step tool chaining, and "human-in-the-loop" requirements of enterprise MCP servers (Jira, Confluence). 

**NeMo RL** allows us to:
1.  **Reward correct tool calls:** Penalize hallucinated parameters.
2.  **Optimize multi-hop reasoning:** Reward the model for finding the right data across Confluence before taking action in Jira.
3.  **Align with Enterprise Safety:** Ensure tool use adheres to permissions and rate limits.

## 🛠️ Components
- `data/mcp_preference_pairs.jsonl`: Training data comparing "vague" vs "precise" MCP tool usage.
- `configs/ppo_mcp_config.yaml`: NeMo-Aligner config tuned for code/tool-use alignment.
- `scripts/train_mcp_ppo.py`: Training entry point using `nemo_aligner`.
- `scripts/mcp_reward_model.py`: Custom reward logic that validates Jira/Confluence API schema adherence.

## 🚀 Scenario: The "Strategic Incident Fixer"
We align a model to:
1.  **Search** Confluence for similar past incidents using MCP.
2.  **Analyze** the delta between past fixes and current logs.
3.  **Propose** a precise Jira ticket update with the correct labels and priority.

---
*Post-training models to be better enterprise citizens.*
