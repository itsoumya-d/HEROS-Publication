# SPDX-License-Identifier: MIT
import json
import gradio as gr
from reflexion_swe.agent import ReflexionAgent, TemplateReflector
from reflexion_swe.sandbox import SubprocessSandbox
from reflexion_swe.tasks import TOY_TASKS, RepairingActor

def run(task_id):
    task = next(item for item in TOY_TASKS if item.id == task_id)
    agent = ReflexionAgent(
        actor=RepairingActor(),
        reflector=TemplateReflector(),
        sandbox=SubprocessSandbox(timeout=3.0),
        max_attempts=3,
        use_testgen=True,
        use_reflection=True,
    )
    trajectory = agent.run(task)
    final = agent.evaluate_final(task, trajectory.patch)
    return json.dumps({
        "task": task.id,
        "prompt": task.prompt,
        "attempts": trajectory.attempt,
        "reflections": trajectory.metadata.get("reflections", []),
        "evaluator": {"passed": trajectory.observation.passed, "failed": trajectory.observation.failed, "error": trajectory.observation.error},
        "final_hidden_tests": {"success": final.success, "passed": final.passed, "failed": final.failed},
        "patch": trajectory.patch,
    }, indent=2)

with gr.Blocks(title="Reflexion-SWE Repair Loop") as demo:
    gr.Markdown("# Reflexion-SWE Repair Loop\nRun a deterministic repair with executable tests and verbal self-reflection.")
    task = gr.Dropdown([item.id for item in TOY_TASKS], value=TOY_TASKS[0].id, label="Repair task")
    button = gr.Button("Run Reflexion loop")
    output = gr.Code(label="Trace", language="json")
    button.click(run, inputs=task, outputs=output)
    demo.load(run, inputs=task, outputs=output)

if __name__ == "__main__":
    demo.launch()
