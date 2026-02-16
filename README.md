# NeMo RL: Model Context Protocol (MCP) Alignment for Atlassian 🚀🧠

This project demonstrates how to use **NVIDIA NeMo RL** (PPO/DPO) to post-train an LLM, specifically improving its ability to utilize the **Atlassian Model Context Protocol (MCP)** for complex enterprise workflows.

## 🏦 The Mission
Standard LLMs often struggle with the precise JSON schemas, multi-step tool chaining, and "human-in-the-loop" requirements of enterprise MCP servers (Jira, Confluence). 

**NeMo RL** allows us to:
1.  **Reward correct tool calls:** Penalize hallucinated parameters.
2.  **Optimize multi-hop reasoning:** Reward the model for finding the right data across Confluence before taking action in Jira.
3.  **Align with Enterprise Safety:** Ensure tool use adheres to permissions and rate limits.

## 🏗️ Real-World Integration
We have successfully seeded a live Atlassian site (`gokang.atlassian.net`) with:
- **Jira Project:** `NEMO` (NeMo RL Training)
- **Incident:** `Critical Latency in Auth Service`
- **Confluence Knowledge:** `Auth Service Recovery Playbook`

This live site serves as the ground truth environment for validating the model's MCP capabilities post-training.

## 🛠️ Components
- `scripts/mcp_reward_model.py`: The "Judge" that enforces Jira/Confluence API schema.
- `scripts/seed_atlassian.py`: Tool used to populate the live test environment.
- `scripts/train_mcp_ppo.py`: NeMo PPO training loop using actual NeMo Aligner APIs.
- `configs/ppo_mcp_config.yaml`: PPO hyperparameters for tool-use alignment.
- `data/mcp_preference_pairs.jsonl`: Preference data comparing weak responses vs. multi-hop MCP expertise.

## 🚀 Scenario: The "Strategic Incident Fixer"
We align a model to:
1.  **Search** Confluence for similar past incidents using MCP.
2.  **Analyze** the delta between past fixes and current logs.
3.  **Propose** a precise Jira ticket update with the correct labels and priority.

---
*Post-training models to be better enterprise citizens.*
