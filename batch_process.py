#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wsadowe przetwarzanie wielu plików extracted.txt do JSONL przy użyciu model_infer.py
Użycie:
python3 batch_process.py --backend openai --model gpt-4o-mini --inputs projektextracted.txt specyfikacjaextracted.txt wytyczneextracted.txt --out results.jsonl
python3 batch_process.py --backend ollama --model mistral:instruct --inputs projektextracted.txt specyfikacjaextracted.txt wytyczneextracted.txt --out results.jsonl
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_infer(input_path: Path, backend: str, model: str) -> str:
    cmd = [
        sys.executable, "model_infer.py",
        "--input-file", str(input_path),
        "--backend", backend,
    ]
    if model:
        cmd += ["--model", model]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Błąd inferencji dla {input_path}: {proc.stderr}")
    return proc.stdout.strip()


def main():
    parser = argparse.ArgumentParser(description="Wsadowe przetwarzanie plików extracted.txt")
    parser.add_argument("--backend", required=True, choices=["openai", "transformers", "ollama"], help="Backend LLM")
    parser.add_argument("--model", required=False, default=None, help="Nazwa modelu")
    parser.add_argument("--inputs", nargs="+", required=True, help="Lista plików wejściowych")
    parser.add_argument("--out", required=True, help="Plik wyjściowy JSONL")
    args = parser.parse_args()

    out_path = Path(args.out)
    with out_path.open("w", encoding="utf-8") as out_f:
        for inp in args.inputs:
            input_path = Path(inp)
            print(f"Przetwarzam: {input_path}")
            try:
                result_json = run_infer(input_path, args.backend, args.model)
                out_f.write(result_json + "\n")
            except Exception as e:
                sys.stderr.write(f"[WARN] {input_path}: {e}\n")
                out_f.write("{\"elements\":[],\"relations\":[],\"requirements\":[],\"error\":true}\n")
    print(f"Zapisano wyniki do: {out_path}")


if __name__ == "__main__":
    main()
