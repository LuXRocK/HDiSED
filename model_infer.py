#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrypt do wywoływania modelu LLM i ekstrakcji elementów/relacji w formacie JSON.
Obsługuje dwa backendy:
- OpenAI-kompatybilny endpoint (HTTP) — wymaga OPENAI_API_KEY (i opcjonalnie OPENAI_BASE_URL, OPENAI_MODEL)
- transformers (lokalny) — jeśli zainstalowane (model wskazany parametrem --model)

Użycie:
python3 model_infer.py --text "..." --backend openai --model gpt-4o-mini --output out.json
python3 model_infer.py --input-file projektextracted.txt --backend openai --output out.jsonl
python3 model_infer.py --text "..." --backend transformers --model mistralai/Mistral-7B-Instruct-v0.2
"""

import os
import sys
import json
import argparse
import time
from typing import Optional, Dict, Any

PROMPT_SYSTEM = (
    "Jesteś ekspertem ds. infrastruktury. Ekstrahuj elementy infrastruktury, relacje i wymagania z podanego tekstu."
    " Zwróć wyłącznie poprawny JSON zgodny ze schematem: {\"elements\":[],\"relations\":[],\"requirements\":[]}"
)

PROMPT_USER_TEMPLATE = (
    "Zadanie: Wyekstrahuj elementy infrastruktury, relacje i wymagania z poniższego tekstu.\n"
    "Wymagania:\n"
    "- Użyj standardowych jednostek (mm, m, %, m³/h).\n"
    "- Jeśli czegoś brak, pomiń pole.\n"
    "- Zwróć wyłącznie czysty JSON bez komentarzy i bez znaczników kodu.\n\n"
    "Tekst:\n{input_text}\n\n"
    "Format wyjściowy (JSON):\n{\"elements\":[{\"id\":\"n1\",\"type\":\"...\",\"name\":\"...\",\"params\":{}}],\"relations\":[],\"requirements\":[]}"
)


def _extract_json(text: str) -> Dict[str, Any]:
    """Próbuje wyodrębnić i sparsować JSON z tekstu odpowiedzi."""
    if not text:
        return {"elements": [], "relations": [], "requirements": []}
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end + 1]
        try:
            data = json.loads(candidate)
            # Normalizacja minimalna
            for key in ("elements", "relations", "requirements"):
                if key not in data or not isinstance(data[key], list):
                    data[key] = []
            return data
        except Exception:
            pass
    # Jeśli nie udało się, zwróć pustą strukturę
    return {"elements": [], "relations": [], "requirements": []}


def call_openai(text: str, model: Optional[str] = None, temperature: float = 0.0, max_tokens: int = 1000) -> Dict[str, Any]:
    import requests

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Brak OPENAI_API_KEY w środowisku.")

    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model_name,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": PROMPT_SYSTEM},
            {"role": "user", "content": PROMPT_USER_TEMPLATE.format(input_text=text)},
        ],
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    if resp.status_code != 200:
        raise RuntimeError(f"Błąd API ({resp.status_code}): {resp.text[:200]}")

    data = resp.json()
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return _extract_json(content)


def call_transformers(text: str, model: str) -> Dict[str, Any]:
    try:
        from transformers import pipeline
    except Exception as exc:
        raise RuntimeError("Brak pakietu transformers. Zainstaluj: pip install transformers accelerate") from exc

    generator = pipeline("text-generation", model=model, device_map="auto")
    prompt = (
        f"System: {PROMPT_SYSTEM}\n\n"
        f"User: {PROMPT_USER_TEMPLATE.format(input_text=text)}\n\n"
        f"Assistant:"
    )
    out = generator(prompt, max_new_tokens=800, temperature=0.1, do_sample=False)
    content = out[0]["generated_text"][len(prompt):]
    return _extract_json(content)


def infer(text: str, backend: str, model: Optional[str]) -> Dict[str, Any]:
    if backend == "openai":
        return call_openai(text=text, model=model)
    elif backend == "transformers":
        if not model:
            raise RuntimeError("Dla backendu 'transformers' wymagany jest parametr --model")
        return call_transformers(text=text, model=model)
    else:
        raise RuntimeError(f"Nieznany backend: {backend}")


def main():
    parser = argparse.ArgumentParser(description="Wywołanie LLM do ekstrakcji elementów/relacji w JSON.")
    parser.add_argument("--text", type=str, help="Tekst wejściowy.")
    parser.add_argument("--input-file", type=str, help="Plik wejściowy z tekstem.")
    parser.add_argument("--output", type=str, help="Plik wyjściowy (JSON/JSONL). Jeśli nie podano, wypisze na stdout.")
    parser.add_argument("--backend", type=str, default="openai", choices=["openai", "transformers"], help="Backend LLM")
    parser.add_argument("--model", type=str, default=None, help="Nazwa modelu (dla openai lub transformers)")
    args = parser.parse_args()

    if not args.text and not args.input_file:
        print("Podaj --text lub --input-file", file=sys.stderr)
        sys.exit(2)

    outputs = []
    if args.text:
        outputs.append(infer(args.text, backend=args.backend, model=args.model))
    else:
        with open(args.input_file, "r", encoding="utf-8") as f:
            content = f.read()
        result = infer(content, backend=args.backend, model=args.model)
        outputs.append(result)

    if args.output:
        # Jeżeli końcówka .jsonl => zapis JSON Lines, w innym razie pojedynczy JSON
        if args.output.lower().endswith(".jsonl"):
            with open(args.output, "w", encoding="utf-8") as f:
                for obj in outputs:
                    f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        else:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(outputs[0] if len(outputs) == 1 else outputs, f, ensure_ascii=False, indent=2)
        print(f"Zapisano wynik do: {args.output}")
    else:
        print(json.dumps(outputs[0] if len(outputs) == 1 else outputs, ensure_ascii=False))


if __name__ == "__main__":
    main()
