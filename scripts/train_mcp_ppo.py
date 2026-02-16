# Copyright (c) 2026, NVIDIA CORPORATION.  All rights reserved.
# NeMo RLHF Training Entry Point for MCP Capability Improvement

from nemo.core.config import hydra_runner
from nemo_aligner.models.nlp.gpt.gpt_ppo_model import GPTPPOModel
from nemo_aligner.utils.train_utils import setup_trainer
from scripts.mcp_reward_model import MCPRewardModel

class AtlassianRewardServer:
    """
    Simulation of an external reward server that uses our MCPRewardModel
    to provide the scalar signal for the PPO loop.
    """
    def __init__(self):
        self.rm = MCPRewardModel()

    def get_reward(self, response_text):
        return self.rm.score_response(response_text)

@hydra_runner(config_path="configs", config_name="ppo_mcp_config")
def main(cfg):
    """
    Main loop for post-training an LLM to master the Atlassian Model Context Protocol.
    """
    print("--- 🚀 Starting NeMo RL Post-Training: Atlassian MCP Expertise ---")
    
    # 1. Setup Distributed Trainer
    trainer = setup_trainer(cfg)

    # 2. Initialize the PPO Model
    # In a live run, this loads the base policy (e.g. Llama-3) and the critic
    model = GPTPPOModel(cfg.model, trainer=trainer)

    # 3. Define the Post-Training Objective
    print(f"🎯 Goal: Maximize reward for valid multi-hop Jira/Confluence MCP calls.")
    
    # 4. Fit/Train
    # The NeMo-Aligner framework will:
    # - Rollout: Generate responses to prompts in data/mcp_preference_pairs.jsonl
    # - Score: Query the reward signal (simulated via MCPRewardModel)
    # - Update: Adjust the policy to favor precise tool calls and sequential reasoning
    trainer.fit(model)

    print("--- ✅ Post-Training Complete: Model is now an MCP Specialist ---")

if __name__ == "__main__":
    main()
