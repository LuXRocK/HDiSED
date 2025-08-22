# Proces czyszczenia dokumentów technicznych

## Opis zadania
Zadanie polegało na usunięciu zbędnych fragmentów z trzech dokumentów technicznych dotyczących infrastruktury wodociągowej:
- `projekt.txt` - Specyfikacje techniczne wykonania i odbioru robót - ST-00.03 – Sieć wodociągowa
- `specyfikacja.txt` - Szczegółowa specyfikacja techniczna sieci wodociągowej
- `wytyczne.txt` - Wytyczne do projektowania sieci wodociągowej i kanalizacyjnej

## Co zostało usunięte

### 1. Elementy administracyjne i formalne:
- **Spisy treści** z numerami stron
- **Nagłówki dokumentów** na początku plików
- **Informacje o autorze** (Opracował: inż. Maria Kluzek, luty 2010 r.)
- **Kody CPV** (45111200-0, 45231300-8, 45232150-8)
- **Informacje o przedsiębiorstwie** (Miejskie Przedsiębiorstwo Wodociągów i Kanalizacji we Włocławku)
- **Daty i miejsca** (Włocławek grudzień 2009 r.)

### 2. Elementy formatowania:
- **Numery stron** (samotne numery)
- **Informacje o stronie** (str. 2-17)
- **Powtarzające się nagłówki**
- **Puste linie** na początku dokumentów
- **Separatory** (linie z kropkami i myślnikami)

### 3. Sekcje prawne i administracyjne:
- **Przepisy prawne** na końcu dokumentów
- **Podstawy płatności**
- **Informacje o dokumentacji**

## Wyniki

### Statystyki plików:

| Plik | Przed czyszczeniem | Po czyszczeniu | Usunięto |
|------|-------------------|----------------|----------|
| projekt.txt | 48,479 znaków | 42,561 znaków | 5,918 znaków (12.2%) |
| specyfikacja.txt | 44,399 znaków | 44,118 znaków | 281 znaków (0.6%) |
| wytyczne.txt | 55,078 znaków | 21,203 znaków | 33,875 znaków (61.5%) |

### Liczba linii:

| Plik | Przed czyszczeniem | Po czyszczeniu | Usunięto |
|------|-------------------|----------------|----------|
| projekt.txt | 689 linii | 578 linii | 111 linii |
| specyfikacja.txt | 785 linii | 759 linii | 26 linii |
| wytyczne.txt | 893 linii | 346 linii | 547 linii |

## Co zostało zachowane

### 1. Treść techniczna:
- **Opisy materiałów** (rury, kształtki, armatura)
- **Specyfikacje techniczne** (parametry, wymagania)
- **Procedury montażowe** i wykonawcze
- **Wymagania jakościowe** i kontrolne
- **Określenia podstawowe** i definicje

### 2. Informacje infrastrukturalne:
- **Rodzaje przewodów** (magistralne, rozdzielcze, przyłącza)
- **Lokalizacja** i trasy sieci
- **Materiały** i sposoby łączenia
- **Armatura** (zasuwy, hydranty, zawory)
- **Skrzyżowania** z innymi instalacjami

### 3. Wymagania projektowe:
- **Zagłębienie** przewodów
- **Spadki** i prędkości przepływu
- **Napełnienie** kanałów
- **Odległości** minimalne
- **Rozwiązania** techniczne

## Pliki wynikowe

Utworzono trzy wyczyszczone pliki:
- `projektextracted.txt` - Specyfikacje techniczne (bez elementów administracyjnych)
- `specyfikacjaextracted.txt` - Szczegółowa specyfikacja (zachowana większość treści)
- `wytyczneextracted.txt` - Wytyczne projektowe (znacznie skrócone, ale zachowana treść techniczna)

## Uwagi

1. **Plik wytyczne.txt** został znacznie skrócony, ponieważ zawierał dużo elementów administracyjnych i powtarzających się nagłówków.

2. **Plik specyfikacja.txt** został najmniej zmieniony, ponieważ już na początku zawierał głównie treść techniczną.

3. **Plik projekt.txt** został umiarkowanie skrócony, usunięto głównie spisy treści i elementy formalne.

## Następne kroki

Wyczyszczone pliki są gotowe do:
- Analizy przez LLM w celu ekstrakcji informacji o infrastrukturze
- Przekształcenia na reprezentacje grafowe
- Integracji z bazą grafową (Neo4j)
- Automatycznego generowania grafów infrastruktury liniowej
