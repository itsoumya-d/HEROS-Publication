# SPDX-License-Identifier: MIT
import json
from pathlib import Path
import gradio as gr
from graphrag_audit.communities import LeidenDetector
from graphrag_audit.eval import run_evaluation
from graphrag_audit.extract import extract_repository
from graphrag_audit.graph import KnowledgeGraph
from graphrag_audit.query import GraphRAG
from graphrag_audit.summarize import summarize_communities

ROOT = Path(__file__).resolve().parent / "sample_repo"
CORPUS = extract_repository(ROOT)
GRAPH = KnowledgeGraph().from_corpus(CORPUS)
HIERARCHY = LeidenDetector().detect(GRAPH)
REPORTS = summarize_communities(HIERARCHY, CORPUS)
RAG = GraphRAG(CORPUS, GRAPH, REPORTS)
METRICS = run_evaluation(str(ROOT), n=100)

def ask(question, mode):
    result = RAG.query(question, mode=mode)
    return json.dumps({
        "answer": result.answer,
        "citations": result.citations,
        "communities": result.communities,
        "method": HIERARCHY.method,
        "communities_total": len(HIERARCHY.communities),
        "eval": {"graph": METRICS["graph"], "flat": METRICS["flat"], "win_rate": METRICS["win_rate"]},
    }, indent=2)

with gr.Blocks(title="GraphRAG CodeAudit Explorer") as demo:
    gr.Markdown("# GraphRAG CodeAudit Explorer\nAsk a local or global question over the synthetic sample repository.")
    question = gr.Textbox(label="Question", value="What security risks exist in auth.py?")
    mode = gr.Radio(["global", "local"], value="global", label="Search mode")
    button = gr.Button("Ask")
    output = gr.Code(label="GraphRAG response", language="json")
    button.click(ask, inputs=[question, mode], outputs=output)
    demo.load(ask, inputs=[question, mode], outputs=output)

if __name__ == "__main__":
    demo.launch()
