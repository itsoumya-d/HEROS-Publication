# SPDX-License-Identifier: MIT
import json
import gradio as gr
from heros_rl.prompts import build_prompt
from heros_rl.rewards import RewardFunction, extract_sections

CASES = [
    {
        "id": "drop-column",
        "hazard": "drop_column",
        "old_schema": "TABLE users\nCOLUMN id bigint NOT_NULL\nCOLUMN email text NOT_NULL\nCOLUMN legacy_note text NULLABLE",
        "target_schema": "TABLE users\nCOLUMN id bigint NOT_NULL\nCOLUMN email text NOT_NULL",
        "data_loss": True,
        "requires_expand_contract": True,
    },
    {
        "id": "rename-column",
        "hazard": "rename_column",
        "old_schema": "TABLE users\nCOLUMN full_name text NULLABLE",
        "target_schema": "TABLE users\nCOLUMN display_name text NULLABLE",
        "data_loss": False,
        "requires_expand_contract": True,
    },
    {
        "id": "safe-add",
        "hazard": "add_nullable_column",
        "old_schema": "TABLE users\nCOLUMN id bigint NOT_NULL",
        "target_schema": "TABLE users\nCOLUMN id bigint NOT_NULL\nCOLUMN bio text NULLABLE",
        "data_loss": False,
        "requires_expand_contract": False,
    },
]
REWARD = RewardFunction()

def prompt_for(name):
    case = next(item for item in CASES if item["id"] == name)
    return build_prompt(case)

def score(name, completion):
    case = next(item for item in CASES if item["id"] == name)
    result = REWARD(completion, case)
    return json.dumps(result.to_dict(), indent=2)

with gr.Blocks(title="HEROS-RL Migration Reward Lab") as demo:
    gr.Markdown("# HEROS-RL Migration Reward Lab\nScore a migration rewrite with the deterministic format + SQL safety reward.")
    with gr.Row():
        case = gr.Dropdown([item["id"] for item in CASES], value="drop-column", label="Migration case")
    prompt = gr.Textbox(label="Prompt", lines=10, interactive=False)
    completion = gr.Textbox(label="Model completion", lines=12, value="""<answer>
MIGRATION:
ALTER TABLE users ADD COLUMN legacy_note_backup text;
ROLLBACK:
ALTER TABLE users DROP COLUMN legacy_note_backup;
</answer>""")
    button = gr.Button("Score completion")
    output = gr.Code(label="Reward breakdown", language="json")
    case.change(prompt_for, inputs=case, outputs=prompt)
    button.click(score, inputs=[case, completion], outputs=output)
    demo.load(prompt_for, inputs=case, outputs=prompt)

if __name__ == "__main__":
    demo.launch()
