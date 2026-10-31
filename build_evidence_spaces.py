#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSS = """
:root{--paper:#f7f5f2;--ink:#161616;--muted:#6b655d;--line:#e4e0da;--accent:#b42318;--ok:#067647}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 ui-sans-serif,system-ui,sans-serif}
main{max-width:1040px;margin:0 auto;padding:48px 24px}h1{font-size:44px;line-height:1.03;letter-spacing:-.035em;margin:0 0 14px}
.eyebrow{font-family:ui-monospace,SFMono-Regular,monospace;color:var(--accent);font-size:12px;letter-spacing:.18em;text-transform:uppercase;margin:0 0 10px}
.lead{color:var(--muted);max-width:78ch;font-size:17px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:24px 0}
.stat{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px}.stat b{display:block;font-size:28px;letter-spacing:-.02em}.stat span{font-size:12px;color:var(--muted)}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;margin:18px 0;font-size:14px}
th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--line)}th{font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted)}tr:last-child td{border-bottom:0}
code,pre{font-family:ui-monospace,SFMono-Regular,monospace}pre{background:#101114;color:#e7e5e1;padding:16px;border-radius:14px;overflow:auto;font-size:13px}
.card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px;margin:16px 0}.note{font-size:13px;color:var(--muted)}
a{color:var(--accent)}img{max-width:100%;border-radius:14px;border:1px solid var(--line);background:#fff}
.tag{display:inline-block;border:1px solid var(--line);border-radius:99px;padding:2px 8px;font-size:11px;margin:0 6px 6px 0;color:var(--muted)}
.links a{display:inline-flex;min-height:42px;align-items:center;border:1px solid var(--line);border-radius:10px;padding:0 12px;margin:4px 8px 4px 0;font-size:13px;font-weight:650;text-decoration:none;color:var(--ink)}.links a.primary{background:var(--accent);border-color:var(--accent);color:#fff}
"""

def page(folder, title, eyebrow, lead, body, tags="", extra_links=""):
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{CSS}</style></head><body><main>
<p class="eyebrow">{eyebrow}</p><h1>{title}</h1><p class="lead">{lead}</p>{body}
<p class="note">{tags}</p><div class="links"><a class="primary" href="https://github.com/itsoumya-d/{extra_links or ''}">Source & CI</a><a href="https://huggingface.co/spaces/itssoumyad/portfolio">Portfolio hub</a></div>
<p class="note">Measured local evidence only. No deployment, customer, or trained-weight claim is made unless explicitly stated.</p>
</main></body></html>"""
    (ROOT / "spaces" / folder / "index.html").write_text(html)

def readme(folder, title, tags, body):
    tag_lines = "\n".join(f"  - {tag}" for tag in tags)
    (ROOT / "spaces" / folder / "README.md").write_text(f"""---
title: {title}
colorFrom: gray
colorTo: red
sdk: static
pinned: false
license: mit
tags:
{tag_lines}
---

{body}
""")

# edgeinfer
page("edgeinfer-v2", "edgeinfer v2", "edgeinfer · browser inference + retrieval",
     "Two-stage Matryoshka retrieval, speculative decoding, and client-side ONNX inference. All numbers below are synthetic/mock local benchmarks, not MTEB or WebGPU measurements.",
     """<div class="grid"><div class="stat"><b>95/95</b><span>tests</span></div><div class="stat"><b>25.1 ms</b><span>coarse+re-rank p50 · 100k×768</span></div><div class="stat"><b>0.725→1.000</b><span>Recall@10 · d=64→768</span></div><div class="stat"><b>68.4%</b><span>mock speculative acceptance</span></div></div>
<table><thead><tr><th>Metric</th><th>Value</th><th>Boundary</th></tr></thead><tbody>
<tr><td>Index build</td><td>1.76 s</td><td>100k synthetic chunks</td></tr>
<tr><td>Coarse scan</td><td>p50 25.08 ms / p95 59.41 ms</td><td>INT8 d=64 + FP32 top-50 re-rank</td></tr>
<tr><td>Speculative decoding</td><td>0.45 target calls/token; modeled 1.64×</td><td>Mock latencies; no WebGPU run</td></tr>
<tr><td>ONNX input casting</td><td>BigInt64Array when metadata says int64</td><td>Covered by tests</td></tr>
</tbody></table>""",
     "Synthetic and mock benchmarks only. Not MTEB, not WebGPU tokens/sec.", "edgeinfer")
readme("edgeinfer-v2", "edgeinfer v2", ["webgpu", "onnx", "matryoshka", "retrieval"], "Browser-local ONNX inference, INT8 Matryoshka retrieval, and speculative decoding. Static evidence page; see GitHub for the library and tests.")

# peervault
page("peervault-pqc", "peervault", "peervault · post-quantum WebRTC",
     "FIPS 203 ML-KEM-768 + P-256 hybrid handshake, 21-byte AES-GCM AAD, and an encrypted vector/memory data mesh.",
     """<div class="grid"><div class="stat"><b>100/100</b><span>NIST ML-KEM KAT vectors</span></div><div class="stat"><b>75/75</b><span>SDK tests</span></div><div class="stat"><b>0.836 ms</b><span>hybrid handshake p50</span></div><div class="stat"><b>1395 / 1043</b><span>MB/s encrypt / decrypt (local)</span></div></div>
<table><thead><tr><th>Layer</th><th>Evidence</th></tr></thead><tbody>
<tr><td>ML-KEM-768 core</td><td>Rust/wasm NTT, CBD, implicit rejection; Node/OpenSSL interop</td></tr>
<tr><td>Handshake</td><td>ML-KEM + ECDH + HKDF; PSK-authenticated HMAC; key confirmation</td></tr>
<tr><td>Frame header</td><td>All 21 bytes, including IV, bound as AES-GCM AAD; 200-mutation fuzz</td></tr>
<tr><td>Data mesh</td><td>LWW vector/memory sync; encrypted control messages</td></tr>
</tbody></table>""",
     "KAT and local crypto benchmarks. No live WebRTC network throughput claim.", "peervault")
readme("peervault-pqc", "peervault PQC", ["post-quantum", "ml-kem", "webrtc", "cryptography"], "Post-quantum WebRTC transport with FIPS 203 ML-KEM-768, hybrid handshake, AAD-bound frames, and encrypted data mesh. Static evidence page.")

# firewall
page("heros-firewall", "HEROS-Firewall", "HEROS · agentic security proxy",
     "Deterministic OWASP ASI01–ASI10 policy engine, HMAC human approvals, and Merkle audit receipts for MCP tool calls.",
     """<div class="grid"><div class="stat"><b>0.0000</b><span>FNR · 1000 adversarial</span></div><div class="stat"><b>0.0000</b><span>FPR · 200 benign</span></div><div class="stat"><b>0.103 ms</b><span>p99 policy latency</span></div><div class="stat"><b>16/16</b><span>tests</span></div></div>
<table><thead><tr><th>Layer</th><th>Behavior</th></tr></thead><tbody>
<tr><td>ASI01 goal hijack</td><td>Deny prompt-injection patterns in untrusted text</td></tr>
<tr><td>ASI02 tool misuse</td><td>Deny dangerous shell/SQL/path patterns</td></tr>
<tr><td>ASI03 privilege</td><td>Deny missing scopes</td></tr>
<tr><td>ASI09 human trust</td><td>Challenge destructive tools; HMAC token, 5-min TTL, single use</td></tr>
<tr><td>ASI10 rogue chain</td><td>Deny <code>read_secret → http_post</code></td></tr>
</tbody></table>
<pre>policy: deny/challenge/allow
receipt: input_hash + output_hash + principal + approval + merkle_root</pre>""",
     "Policy-layer p99 only; downstream MCP/network time not measured. Dashboard and OCI deployment not built.", "HEROS-Firewall")
readme("heros-firewall", "HEROS Firewall", ["mcp", "security", "agents", "owasp"], "Inline MCP security proxy with OWASP ASI policies, approvals, and Merkle receipts. Static evidence page.")

# perfbench
shutil.copy(ROOT.parent.parent / "repos" / "Anthropic-PerfBench" / "results" / "roofline.svg", ROOT / "spaces" / "anthropic-perfbench" / "roofline.svg")
page("anthropic-perfbench", "Anthropic-PerfBench", "PerfBench · ARM64 NEON + WGSL",
     "Fused RMSNorm+residual, in-place RoPE, and group-wise INT4 GEMV across three optimization iterations.",
     """<div class="grid"><div class="stat"><b>3.09×</b><span>RMSNorm NEON vs scalar</span></div><div class="stat"><b>2.35×</b><span>RoPE NEON vs scalar</span></div><div class="stat"><b>11.83×</b><span>INT4 GEMV NEON vs scalar</span></div><div class="stat"><b>66.31 GB/s</b><span>measured copy bandwidth</span></div></div>
<img src="roofline.svg" alt="Memory roofline for the three NEON kernels">
<table><thead><tr><th>Kernel</th><th>Scalar</th><th>NEON</th><th>Speedup</th></tr></thead><tbody>
<tr><td>RMSNorm+residual</td><td>6.454 ms</td><td>2.087 ms</td><td>3.09×</td></tr>
<tr><td>RoPE</td><td>1.733 ms</td><td>0.738 ms</td><td>2.35×</td></tr>
<tr><td>INT4 GEMV</td><td>20.686 ms</td><td>1.748 ms</td><td>11.83×</td></tr>
</tbody></table>""",
     "Apple Silicon NEON results. OCI Ampere perf counters and WebGPU timings not run; roofline caveats are documented in RESULTS.md.", "Anthropic-PerfBench")
readme("anthropic-perfbench", "Anthropic PerfBench", ["neon", "arm64", "wgsl", "roofline"], "Three-iteration transformer kernel optimization suite. Static evidence page with the measured NEON roofline; WGSL sources are in the repo.")

# routellm
shutil.copy(ROOT.parent.parent / "repos" / "RouteLLM-Gateway" / "results" / "pareto.svg", ROOT / "spaces" / "routellm-gateway" / "pareto.svg")
page("routellm-gateway", "RouteLLM-Gateway", "RouteLLM · calibrated routing",
     "Bradley–Terry cost-quality routing with a semantic cache, schema fallback, and OpenAI/Anthropic-compatible streaming.",
     """<div class="grid"><div class="stat"><b>98.38%</b><span>accuracy retention vs always-frontier</span></div><div class="stat"><b>69.40%</b><span>cost reduction</span></div><div class="stat"><b>0.74</b><span>calibrated threshold</span></div><div class="stat"><b>13.6%</b><span>cache hit rate</span></div></div>
<img src="pareto.svg" alt="Synthetic cost-accuracy Pareto">
<table><thead><tr><th>System</th><th>Accuracy</th><th>Cost / 250</th><th>p50</th></tr></thead><tbody>
<tr><td>Always frontier</td><td>98.80%</td><td>$0.5000</td><td>650 ms</td></tr>
<tr><td>Router</td><td>97.20%</td><td>$0.1868</td><td>120 ms</td></tr>
<tr><td>Router + cache</td><td>97.20%</td><td>$0.1530</td><td>120 ms</td></tr>
</tbody></table>""",
     "Synthetic mock-provider benchmark. Not MMLU-Pro or GSM8K; real provider keys were unavailable.", "RouteLLM-Gateway")
readme("routellm-gateway", "RouteLLM Gateway", ["routing", "semantic-cache", "llm", "pareto"], "Calibrated multi-model router with semantic cache and streaming APIs. Static evidence page with the synthetic Pareto curve.")

# mobbin ui
boards = ROOT.parent.parent / "repos" / "Mobbin-UI-Compiler" / "generated" / ".mobbin"
(ROOT / "spaces" / "mobbin-ui-compiler" / "boards").mkdir(exist_ok=True)
for board in boards.glob("*.html"):
    shutil.copy(board, ROOT / "spaces" / "mobbin-ui-compiler" / "boards" / board.name)
links = "".join(f'<li><a href="boards/{board.name}">{board.stem}</a></li>' for board in sorted(boards.glob("*.html")))
page("mobbin-ui-compiler", "Mobbin-UI-Compiler", "UI compiler · reference-driven",
     "Five SaaS surfaces compiled from a Mobbin search_screens-style adapter contract. Fixture metadata stands in for the unavailable live MCP.",
     f"""<div class="grid"><div class="stat"><b>5</b><span>surfaces</span></div><div class="stat"><b>10/10</b><span>tests</span></div><div class="stat"><b>0</b><span>live Mobbin calls</span></div><div class="stat"><b>44 px</b><span>minimum target</span></div></div>
<div class="card"><h2>Reference boards</h2><ul>{links}</ul><p class="note">Each board is explicitly labelled as fixture metadata, not copied screenshots. Components include focus-visible, ARIA labels, and reduced-motion rules.</p></div>""",
     "No live Mobbin MCP, no Playwright/axe/Lighthouse, no React build. Source-level invariants only.", "Mobbin-UI-Compiler")
readme("mobbin-ui-compiler", "Mobbin UI Compiler", ["ui", "design-system", "mobbin", "accessibility"], "Reference-driven compiler for five SaaS surfaces. Static evidence page with fixture reference boards; live Mobbin and browser audits are pending.")

# cloud saas
page("heros-cloud-saas", "HEROS Cloud", "HEROS Cloud · PLLB governance",
     "Human-readable policy learning with a language bottleneck: execute workflows, synthesise risk rules, approve them, and rerun under governance.",
     """<div class="grid"><div class="stat"><b>70% → 100%</b><span>held-out completion</span></div><div class="stat"><b>+30 pp</b><span>completion delta</span></div><div class="stat"><b>4</b><span>approved PLLB rules</span></div><div class="stat"><b>100%</b><span>receipt coverage</span></div></div>
<table><thead><tr><th>Metric</th><th>Baseline</th><th>PLLB-governed</th></tr></thead><tbody>
<tr><td>Completion rate</td><td>70.0%</td><td>100.0%</td></tr>
<tr><td>Receipt coverage</td><td>100%</td><td>100%</td></tr>
<tr><td>Policy applications</td><td>0</td><td>20</td></tr>
</tbody></table>
<pre>When a migration workflow includes drop_column,
require a human-approved rollback plan and verified backup.</pre>""",
     "Deterministic 50-workflow simulation. No voice/audio, hosted UI, OCI/Oracle, billing, customers, or ARR claim.", "HEROS-Cloud-SaaS")
readme("heros-cloud-saas", "HEROS Cloud PLLB", ["pllb", "governance", "agents", "workflows"], "PLLB-governed workflow studio composition layer. Static evidence page with the measured baseline-to-governed completion improvement.")

print("built evidence spaces")
