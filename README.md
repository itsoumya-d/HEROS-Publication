# Hugging Face publication package

Published artifacts for the HEROS/edgeinfer portfolio under the
`itssoumyad` Hugging Face account. See `published.json` for live URLs and
runtime status.

## Assets

| Asset | Type | Source | arXiv tags |
|---|---|---|---|
| `heros-rl` | Space | HEROS-RL reward + dataset demo | 2402.03300, 2501.12948 |
| `reflexion-swe` | Space | Reflexion actor/evaluator toy | 2303.11366, 2510.08191, 2310.06770 |
| `graphrag-codeaudit` | Space | GraphRAG sample-repo explorer | 2404.16130 |
| `heros-migration-500` | Dataset | 500 migration cases | 2402.03300, 2501.12948 |
| `graphrag-questions-100` | Dataset | 100 sensemaking questions | 2404.16130 |

## Published

| Asset | URL |
|---|---|
| Portfolio hub | https://huggingface.co/spaces/itssoumyad/portfolio |
| HEROS-RL reward lab | https://huggingface.co/spaces/itssoumyad/heros-rl |
| Reflexion-SWE demo | https://huggingface.co/spaces/itssoumyad/reflexion-swe |
| GraphRAG explorer | https://huggingface.co/spaces/itssoumyad/graphrag-codeaudit |
| edgeinfer-v2 evidence | https://huggingface.co/spaces/itssoumyad/edgeinfer-v2 |
| peervault PQC evidence | https://huggingface.co/spaces/itssoumyad/peervault-pqc |
| HEROS-Firewall evidence | https://huggingface.co/spaces/itssoumyad/heros-firewall |
| PerfBench roofline | https://huggingface.co/spaces/itssoumyad/anthropic-perfbench |
| RouteLLM Pareto | https://huggingface.co/spaces/itssoumyad/routellm-gateway |
| Mobbin compiler boards | https://huggingface.co/spaces/itssoumyad/mobbin-ui-compiler |
| HEROS Cloud PLLB | https://huggingface.co/spaces/itssoumyad/heros-cloud-saas |
| Migration dataset | https://huggingface.co/datasets/itssoumyad/heros-migration-500 |
| Questions dataset | https://huggingface.co/datasets/itssoumyad/graphrag-questions-100 |

## Republish

```bash
python3 -m venv .hf-venv
.hf-venv/bin/pip install huggingface_hub
.hf-venv/bin/hf auth login
.hf-venv/bin/python publish.py --user itssoumyad
```

`publish.py` creates CPU-basic Spaces and datasets, uploads the folders, and
prints the public URLs. It does not request ZeroGPU or paid hardware.

## Honest boundaries

- The HEROS-RL 1.5B training and Reflexion-SWE HumanEval/SWE-bench runs are not
  executed; the Spaces demonstrate the deterministic rewards/harness, not model
  weights.
- The GraphRAG Space uses the synthetic sample repository and deterministic judge,
  not the paper's LLM judge.
- No model weights are uploaded because no GPU training was run.
