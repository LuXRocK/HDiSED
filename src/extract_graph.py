import ollama
import json
import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schemas import InfrastructureGraph, NodeType

def extract_graph_from_text(model_name: str, input_path: str, output_dir: str):
    """
    Extracts an infrastructure graph from a text file using a specified Ollama model.

    Args:
        model_name: The name of the Ollama model to use (e.g., 'mistral').
        input_path: The path to the input text file.
        output_dir: The directory to save the output JSON file.
    """
    print(f"--- Starting extraction with model: {model_name} ---")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
        print(f"Successfully read input file: {input_path}")
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    model_output_dir = os.path.join(output_dir, model_name)
    os.makedirs(model_output_dir, exist_ok=True)
    output_path = os.path.join(model_output_dir, 'extracted_graph.json')

    allowed_types = ", ".join(f'"{t}"' for t in NodeType.__args__)

    prompt = f'''
Twoim zadaniem jest działać jako analityk danych. Przeanalizuj poniższy tekst i wyekstrahuj z niego graf infrastruktury.
Zwróć odpowiedź jako pojedynczy, poprawny składniowo obiekt JSON i nic więcej.

Obiekt JSON musi zawierać dwa klucze: "elements" i "relationships".

1.  **elements**: To jest lista obiektów. Każdy obiekt w liście reprezentuje jeden element infrastruktury i musi mieć DOKŁADNIE trzy klucze: "id", "type", "description".
    *   `id`: Krótki, unikalny identyfikator (np. "Z1", "P1").
    *   `type`: Kategoria elementu. Musi to być JEDNA z następujących wartości: {allowed_types}.
    *   `description`: Krótki opis elementu wyciągnięty z tekstu (np. "Główny Zbiornik Wody").

2.  **relationships**: To jest lista obiektów. Każdy obiekt reprezentuje relację i musi mieć DOKŁADNIE cztery klucze: "source", "target", "label", "context".

BARDZO WAŻNE ZASADY:
*   Używaj DOKŁADNIE tych nazw kluczy: "id", "type", "description", "source", "target", "label", "context". Nie dodawaj spacji ani innych znaków.
*   Wartość pola `type` MUSI być jedną z dozwolonych wartości. Na przykład, jeśli w tekście jest "Osiedla A", `type` powinien być "Osiedle". Jeśli jest "Mniejsza pompownia P2", `type` powinien być "Pompownia".
*   "Stacja Pomp" i "Pompownia" to ten sam typ: "Pompownia".
*   Cała odpowiedź musi być jednym obiektem JSON. Nie dodawaj żadnych dodatkowych znaków, słów ani wartości (takich jak `false`) poza obiektem JSON.

Przykłady mapowania:
*   "Stacja Pomp Główna" -> "Pompownia"
*   "Pompownia Główna" -> "Pompownia"
*   "Przewód Północny" -> "Rurociąg"
*   "Zbiornik Retencyjny" -> "Zbiornik Wody"
*   "Sieć Dystrybucyjna Północna" -> "Rurociąg"
*   "Osiedle Mieszkaniowe" -> "Osiedle"
*   "Hydrant Północny" -> "Zawór"
*   "Przewód Południowy" -> "Rurociąg"
*   "Sieć Dystrybucyjna Południowa" -> "Rurociąg"
*   "Strefa Przemysłowa" -> "Strefa Przemysłowa"
*   "Zawór Południowy" -> "Zawór"
*   "Punkt Pomiarowy Przepływu" -> "Inne"

Przykład:
{{
  "elements": [
    {{ "id": "Z1", "type": "Zbiornik Wody", "description": "Główny Zbiornik Wody" }},
    {{ "id": "P2", "type": "Pompownia", "description": "Mniejsza pompownia P2" }},
    {{ "id": "A", "type": "Osiedle", "description": "Osiedla A" }}
  ],
  "relationships": [
    {{ "source": "Z1", "target": "P1", "label": "POŁĄCZONY_Z", "context": "Główny Zbiornik Wody (Z1), który jest połączony z Pompownią Główną (P1)." }}
  ]
}}

Tekst do analizy:
---
{text_content}
---

Wygeneruj pełny obiekt JSON na podstawie powyższego tekstu. Upewnij się, że odpowiedź jest poprawna składniowo i zgodna ze schematem.
'''

    try:
        print("Sending request to Ollama model... (to może potrwać)")
        response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}],
            format='json',
            options={'temperature': 0, 'timeout': 300},
        )

        response_content = response['message']['content']
        print("Received response from Ollama.")

        graph_data = InfrastructureGraph.model_validate_json(response_content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            graph_dict = graph_data.model_dump()
            json.dump(graph_dict, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully validated and saved the extracted graph to: {output_path}")

    except Exception as e:
        print(f"An error occurred during the extraction process: {e}")
        if 'response_content' in locals():
            error_path = os.path.join(model_output_dir, 'error_response.json')
            with open(error_path, 'w', encoding='utf-8') as f:
                f.write(response_content)
            print(f"Raw model response saved to {error_path} for debugging.")

    print(f"--- Finished extraction with model: {model_name} ---\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract infrastructure graph from text using Ollama.")
    parser.add_argument("model", type=str, help="The name of the Ollama model to use (e.g., 'mistral', 'llama3').")
    parser.add_argument("--input_file", type=str, default="data/input/opis_infrastruktury.txt", help="The path to the input text file.")
    parser.add_argument("--output_dir", type=str, default="data/output", help="The directory to save the output files.")
    
    args = parser.parse_args()

    abs_input_file = os.path.abspath(args.input_file)
    abs_output_dir = os.path.abspath(args.output_dir)

    extract_graph_from_text(args.model, abs_input_file, abs_output_dir)