# HDISED - Ekstrakcja Grafu Infrastruktury

## O Projekcie

Ten projekt wykorzystuje duże modele językowe (LLM) do automatycznego wyodrębniania informacji o grafie infrastruktury z opisu tekstowego. System przetwarza tekst, aby zidentyfikować elementy (węzły) i relacje (krawędzie), a następnie zapisuje wyniki w formacie JSON.

Celem jest porównanie zdolności różnych modeli LLM (Mistral, Llama3, Gemma, Phi3) do ekstrakcji i strukturyzacji danych.

## Wymagania

Przed uruchomieniem projektu upewnij się, że masz zainstalowane następujące oprogramowanie:

1.  **Python 3.10+**
2.  **Docker**: [https://www.docker.com/](https://www.docker.com/)
3.  **Ollama**: [https://ollama.com/](https://ollama.com/)
4.  **Modele Ollama**: Wymagane modele muszą być pobrane i dostępne lokalnie.
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

### Ekstrakcja grafu z opisu tekstowego

Głównym skryptem do ekstrakcji danych jest `src/extract_graph.py`.

Aby uruchomić ekstrakcję dla konkretnego modelu, użyj następującego polecenia, zastępując `<nazwa_modelu>` jedną z wartości: `mistral`, `llama3`, `gemma`, `phi3`.

```bash
python3 src/extract_graph.py <nazwa_modelu>
```

Wyniki dla każdego modelu zostaną zapisane w odpowiednim podkatalogu w `data/output/`.

### Uruchomienie i import danych do Neo4j

Po wygenerowaniu plików `extracted_graph.json` możesz załadować je do bazy danych Neo4j w celu wizualizacji i analizy.

**Krok 1: Uruchomienie bazy danych Neo4j za pomocą Docker**

Użyj poniższej komendy, aby uruchomić kontener Docker z bazą danych Neo4j. Baza danych będzie dostępna pod adresem `bolt://localhost:7687`, a interfejs webowy pod `http://localhost:7474`.

```bash
sudo docker run --name neo4j-hdi -p 7474:7474 -p 7687:7687 -d -v $PWD/neo4j_data:/data -e NEO4J_AUTH=neo4j/password neo4j:latest
```
*   **Uwaga:** Jeśli nie chcesz używać `sudo`, dodaj swojego użytkownika do grupy `docker`.
*   Dane bazy będą przechowywane w nowo utworzonym katalogu `neo4j_data` w folderze projektu.

**Krok 2: Import danych do Neo4j**

Użyj skryptu `src/load_to_neo4j.py`, aby zaimportować dane wybranego modelu do bazy. Skrypt za każdym razem czyści bazę przed importem.

```bash
python3 src/load_to_neo4j.py <nazwa_modelu>
```

**Przykłady:**
```bash
# Import danych z modelu gemma
python3 src/load_to_neo4j.py gemma

# Import danych z modelu mistral
python3 src/load_to_neo4j.py mistral
```

**Krok 3: Wizualizacja grafu w Neo4j Browser**

1.  Otwórz w przeglądarce interfejs webowy Neo4j: `http://localhost:7474`.
2.  Zaloguj się używając domyślnych danych:
    *   **Użytkownik:** `neo4j`
    *   **Hasło:** `password`
3.  W polu zapytania na górze ekranu (`$`) wklej poniższe zapytanie, aby wyświetlić cały graf (węzły i relacje).

```cypher
MATCH (n)-[r]->(m)
RETURN n, r, m
```
4.  Naciśnij przycisk "play" (trójkąt) lub użyj skrótu `Ctrl+Enter`, aby wykonać zapytanie i zobaczyć wizualizację.

## Struktura Projektu

```
/
├── data/
│   ├── input/
│   │   └── opis_infrastruktury.txt
│   └── output/
│       ├── gemma/
│       ├── llama3/
│       ├── mistral/
│       └── phi3/
├── neo4j_data/
├── specs/
├── src/
│   ├── extract_graph.py
│   ├── load_to_neo4j.py
│   └── schemas.py
└── README.md
```