# HDISED - Ekstrakcja Grafu Infrastruktury

## O Projekcie

Ten projekt wykorzystuje duże modele językowe (LLM) do automatycznego wyodrębniania informacji o grafie infrastruktury z opisu tekstowego. System przetwarza tekst, aby zidentyfikować elementy (węzły) i relacje (krawędzie), a następnie zapisuje wyniki w formacie JSON.

Celem jest porównanie zdolności różnych modeli LLM (Mistral, Llama3, Gemma, Phi3) do ekstrakcji i strukturyzacji danych.

## Wymagania

Przed uruchomieniem projektu upewnij się, że masz zainstalowane następujące oprogramowanie:

1.  **Python 3.10+**
2.  **Ollama**: [https://ollama.com/](https://ollama.com/)
3.  **Modele Ollama**: Wymagane modele muszą być pobrane i dostępne lokalnie.
    *   `mistral`
    *   `llama3`
    *   `gemma`
    *   `phi3`

## Instalacja

1.  **Sklonuj repozytorium:**
    ```bash
    git clone <URL_REPOZYTORIUM>
    cd HDISED
    ```

2.  **Zainstaluj wymagane biblioteki Python:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Pobierz modele Ollama:**
    Uruchom następujące polecenia w terminalu, aby pobrać wszystkie wymagane modele:
    ```bash
    ollama pull mistral
    ollama pull llama3
    ollama pull gemma
    ollama pull phi3
    ```

## Użycie

Głównym skryptem do ekstrakcji danych jest `src/extract_graph.py`.

Aby uruchomić ekstrakcję dla konkretnego modelu, użyj następującego polecenia, zastępując `<nazwa_modelu>` jedną z wartości: `mistral`, `llama3`, `gemma`, `phi3`.

```bash
python3 src/extract_graph.py <nazwa_modelu>
```

**Przykłady:**

*   **Dla modelu Mistral:**
    ```bash
    python3 src/extract_graph.py mistral
    ```
*   **Dla modelu Llama3:**
    ```bash
    python3 src/extract_graph.py llama3
    ```
*   **Dla modelu Gemma:**
    ```bash
    python3 src/extract_graph.py gemma
    ```
*   **Dla modelu Phi3:**
    ```bash
    python3 src/extract_graph.py phi3
    ```

Wyniki dla każdego modelu zostaną zapisane w odpowiednim podkatalogu w `data/output/`. Na przykład, wynik dla modelu `mistral` znajdzie się w `data/output/mistral/extracted_graph.json`.

Jeśli model napotka błąd podczas walidacji JSON, surowa odpowiedź zostanie zapisana w pliku `error_response.json` w tym samym katalogu, co ułatwi debugowanie.

## Struktura Projektu

```
/
├── data/
│   ├── input/
│   │   └── opis_infrastruktury.txt  # Plik wejściowy z opisem
│   └── output/
│       ├── gemma/
│       ├── llama3/
│       ├── mistral/
│       └── phi3/                   # Katalogi z wynikami dla każdego modelu
├── specs/                          # Dokumenty ze specyfikacją
├── src/
│   ├── extract_graph.py            # Główny skrypt do ekstrakcji
│   └── schemas.py                  # Schematy Pydantic dla danych wyjściowych
└── README.md                       # Ten plik
```
