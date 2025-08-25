## Krok 4: Uruchomienie inferencji na darmowym backendzie (Ollama lub Transformers)

### Opcja A: Ollama (zalecane lokalnie)
1. Zainstaluj Ollama: `https://ollama.com`
2. Pobierz model instruktarzowy, np. Mistral:
   - `ollama pull mistral:instruct`
3. Uruchom inferencję na jednym pliku:
   - `python3 model_infer.py --input-file projektextracted.txt --backend ollama --model mistral:instruct --output out_projekt.json`
4. Uruchom wsadowo na wszystkich plikach:
   - `python3 batch_process.py --backend ollama --model mistral:instruct --inputs projektextracted.txt specyfikacjaextracted.txt wytyczneextracted.txt --out results.jsonl`

Zmienne opcjonalne: `OLLAMA_BASE_URL` (domyślnie `http://localhost:11434`).

### Opcja B: Transformers (offline)
1. `pip install -r requirements.txt`
2. Przykład uruchomienia:
   - `python3 model_infer.py --input-file projektextracted.txt --backend transformers --model mistralai/Mistral-7B-Instruct-v0.2 --output out_projekt.json`

Uwagi:
- Backend OpenAI nie jest wymagany. Całość działa lokalnie.
- Wynik to JSON zgodny ze schematem z `prompt_instructions.md`.
# Zadania na następne dni - WYKONANE ✅

## Zadanie 1: Przygotowanie promptu/instrukcji dla modelu

### Utworzone pliki:
- **`prompt_instructions.md`** - szczegółowe instrukcje dla modelu LLM

### Zawartość instrukcji:
1. **Format wyjściowy JSON** z polami:
   - `elements`: lista elementów infrastruktury z parametrami
   - `relations`: lista relacji między elementami  
   - `requirements`: lista wymagań technicznych

2. **Typy elementów** (6 kategorii):
   - rury, armatura, kształtki, studnie, przewody, uzbrojenie

3. **Typy relacji** (9 typów):
   - connected_to, connected_via, contains, covers, supplies, drains_to, has_requirement, parallel_to, crosses

4. **Parametry techniczne** (10 typów):
   - średnica_mm, ciśnienie_PN, długość_m, głębokość_m, spadek_percent, przepływ_m3h, grubość_ścianki_mm, odległość_m, napełnienie_percent, prędkość_ms

5. **Typy wymagań** (6 typów):
   - spacing, slope_min/max, depth_min/max, material, connection, testing

6. **Przykłady anotacji referencyjnych** z JSON

## Zadanie 2: Testowanie na małym zbiorze

### Utworzone pliki:
- **`test_model_extraction.py`** - skrypt testujący model
- **`test_results.json`** - wyniki testów

### Testy przeprowadzone:
**5 przypadków testowych** z różnymi scenariuszami:

1. **Zestaw hydrantowy** - kompleksowy zestaw elementów z relacjami
2. **Wymagania odstępów** - kolektor z wymaganiami technicznymi
3. **Wymagania spadków** - przyłącza z różnymi spadkami
4. **Relacja przykrycia** - właz przykrywający komorę
5. **Rury z parametrami** - rury z wymiarami i DN

### Wyniki testów:

#### Symulacja modelu (uproszczona):
- **Dokładność ogólna**: 9.52%
- **Dokładność elementów**: 25.00%
- **Dokładność relacji**: 0.00%
- **Dokładność wymagań**: 0.00%

#### Analiza wyników:
- **Elementy**: Model poprawnie identyfikuje podstawowe elementy (hydranty, zasuwy, kolektory)
- **Relacje**: Nie rozpoznaje relacji między elementami
- **Wymagania**: Nie ekstrahuje wymagań technicznych
- **Parametry**: Częściowo poprawnie wyciąga średnice

### Problemy zidentyfikowane:
1. **Wzorce regex** są zbyt uproszczone
2. **Brak rozpoznawania kontekstu** - model nie rozumie związków między elementami
3. **Niepełna ekstrakcja parametrów** - brak rozpoznawania jednostek i wartości
4. **Brak analizy semantycznej** - model nie rozumie znaczenia tekstu

## Następne kroki do poprawy:

### 1. Ulepszenie promptu:
- Dodanie więcej przykładów z różnymi scenariuszami
- Precyzyjniejsze instrukcje dotyczące rozpoznawania relacji
- Dodanie instrukcji dotyczących kontekstu i znaczenia

### 2. Integracja z prawdziwym LLM:
- Podłączenie do API GPT-4, Claude lub lokalnego modelu
- Testowanie na rzeczywistym modelu językowym
- Dostrojenie promptu na podstawie wyników

### 3. Rozszerzenie testów:
- Więcej przypadków testowych
- Różnorodne typy tekstów technicznych
- Testy na pełnych dokumentach

### 4. Metryki oceny:
- Precyzja i recall dla elementów
- Dokładność relacji
- Kompletność parametrów
- Jakość JSON output

## Pliki źródłowe:
- `prompt_instructions.md` - instrukcje dla modelu
- `test_model_extraction.py` - skrypt testujący
- `test_results.json` - wyniki testów
- `annotations_examples.jsonl` - anotacje referencyjne

## Status:
✅ **Zadanie 1**: Prompt przygotowany
✅ **Zadanie 2**: Testy przeprowadzone
🔄 **Następny krok**: Integracja z prawdziwym LLM i ulepszenie promptu
