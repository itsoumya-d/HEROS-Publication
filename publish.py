#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Create and upload the publication-ready Hugging Face repos."""
from __future__ import annotations

import argparse
from pathlib import Path

from huggingface_hub import HfApi


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    api = HfApi()
    assets = [
        ("space", "heros-rl", root / "spaces" / "heros-rl"),
        ("space", "reflexion-swe", root / "spaces" / "reflexion-swe"),
        ("space", "graphrag-codeaudit", root / "spaces" / "graphrag-codeaudit"),
        ("space", "edgeinfer-v2", root / "spaces" / "edgeinfer-v2"),
        ("space", "peervault-pqc", root / "spaces" / "peervault-pqc"),
        ("space", "heros-firewall", root / "spaces" / "heros-firewall"),
        ("space", "anthropic-perfbench", root / "spaces" / "anthropic-perfbench"),
        ("space", "routellm-gateway", root / "spaces" / "routellm-gateway"),
        ("space", "mobbin-ui-compiler", root / "spaces" / "mobbin-ui-compiler"),
        ("space", "heros-cloud-saas", root / "spaces" / "heros-cloud-saas"),
        ("space", "portfolio", root / "spaces" / "portfolio"),
        ("dataset", "heros-migration-500", root / "datasets" / "heros-migration-500"),
        ("dataset", "graphrag-questions-100", root / "datasets" / "graphrag-questions-100"),
    ]
    for repo_type, name, folder in assets:
        repo_id = f"{args.user}/{name}"
        print(f"{repo_type}: {repo_id} <- {folder}")
        if args.dry_run:
            continue
        kwargs = {"repo_id": repo_id, "repo_type": repo_type, "exist_ok": True, "private": False}
        if repo_type == "space":
            kwargs["space_sdk"] = "static"
        api.create_repo(**kwargs)
        api.upload_folder(repo_id=repo_id, repo_type=repo_type, folder_path=str(folder))
        print(f"  https://huggingface.co/{'spaces' if repo_type == 'space' else 'datasets'}/{repo_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
