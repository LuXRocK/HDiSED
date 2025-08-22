# Instrukcje dla modelu LLM - Ekstrakcja elementów i relacji infrastruktury

## Zadanie
Przeanalizuj podany tekst techniczny dotyczący infrastruktury wodociągowej/kanalizacyjnej i wyekstrahuj:
1. **Elementy infrastruktury** z ich parametrami technicznymi
2. **Relacje** między elementami
3. **Wymagania techniczne** dla elementów

## Format wyjściowy - JSON
```json
{
  "elements": [
    {
      "id": "n1",
      "type": "typ_elementu",
      "name": "nazwa_elementu",
      "params": {
        "średnica_mm": 150,
        "ciśnienie_PN": 10,
        "długość_m": 50,
        "głębokość_m": 2.5,
        "spadek_percent": 2.0,
        "przepływ_m3h": 20,
        "grubość_ścianki_mm": 9.5
      }
    }
  ],
  "relations": [
    {
      "type": "typ_relacji",
      "from": "id_elementu_źródłowego",
      "to": "id_elementu_docelowego",
      "attributes": {
        "dodatkowe_parametry": "wartość"
      }
    }
  ],
  "requirements": [
    {
      "id": "req1",
      "type": "typ_wymagania",
      "description": "opis_wymagania",
      "value": "wartość_liczbowa",
      "unit": "jednostka"
    }
  ]
}
```

## Typy elementów infrastruktury
- **rury**: rury wodociągowe, kanalizacyjne, tłoczne
- **armatura**: zasuwy, zawory, hydranty, klapy zwrotne
- **kształtki**: trójniki, zwężki, króćce, łuki, opaski
- **studnie**: studnie rewizyjne, komory, przepompownie, syfony
- **przewody**: kolektory, kanały, przyłącza, rurociągi
- **uzbrojenie**: skrzynki, obudowy, wodomierze, bloki oporowe, włazy

## Typy relacji
- **connected_to**: bezpośrednie połączenie
- **connected_via**: połączenie przez element pośredni
- **contains**: zawieranie (np. studnia zawiera kanał)
- **covers**: przykrycie (np. właz przykrywa studnię)
- **supplies**: zasilanie (np. rura zasila hydrant)
- **drains_to**: odprowadzanie do
- **has_requirement**: element ma wymaganie techniczne
- **parallel_to**: równoległość do
- **crosses**: skrzyżowanie z

## Parametry techniczne do ekstrakcji
- **średnica_mm**: średnica nominalna w mm (DN)
- **ciśnienie_PN**: ciśnienie nominalne (PN)
- **długość_m**: długość w metrach
- **głębokość_m**: głębokość posadowienia
- **spadek_percent**: spadek w procentach
- **przepływ_m3h**: przepływ w m³/h
- **grubość_ścianki_mm**: grubość ścianki
- **odległość_m**: odległość między elementami
- **napełnienie_percent**: napełnienie w procentach
- **prędkość_ms**: prędkość przepływu w m/s

## Typy wymagań technicznych
- **spacing**: wymagania dotyczące odstępów
- **slope_min/max**: minimalny/maksymalny spadek
- **depth_min/max**: minimalna/maksymalna głębokość
- **material**: wymagania materiałowe
- **connection**: wymagania połączeniowe
- **testing**: wymagania testowe

## Przykłady anotacji referencyjnych

### Przykład 1: Zestaw hydrantowy
**Tekst**: "Zestaw hydrantowy (komplet): żeliwny hydrant nadziemny HN 100, sztywny; łuk kołnierzowy 90º ze stopką DN 100; zasuwa kołnierzowa typu E DN 100; króciec dwukołnierzowy FF 100"

**JSON**:
```json
{
  "elements": [
    {"id": "n1", "type": "hydrant", "name": "Hydrant nadziemny HN 100", "params": {"średnica_mm": 100}},
    {"id": "n2", "type": "łuk", "name": "Łuk kołnierzowy 90°", "params": {"średnica_mm": 100}},
    {"id": "n3", "type": "zasuwa", "name": "Zasuwa kołnierzowa typu E", "params": {"średnica_mm": 100}},
    {"id": "n4", "type": "króciec", "name": "Króciec dwukołnierzowy FF", "params": {"średnica_mm": 100}}
  ],
  "relations": [
    {"type": "connected_via", "from": "n1", "to": "n2"},
    {"type": "connected_via", "from": "n2", "to": "n3"},
    {"type": "connected_via", "from": "n3", "to": "n4"}
  ]
}
```

### Przykład 2: Wymagania techniczne
**Tekst**: "Dla średnic kolektorów DN 150 na odcinkach prostych studnie rozmieszczać co 35 m"

**JSON**:
```json
{
  "elements": [
    {"id": "n1", "type": "kolektor", "name": "Kolektor DN 150", "params": {"średnica_mm": 150}}
  ],
  "relations": [
    {"type": "has_requirement", "from": "n1", "to": "req1"}
  ],
  "requirements": [
    {"id": "req1", "type": "spacing", "description": "Rozmieszczenie studni co 35 m", "value": 35, "unit": "m"}
  ]
}
```

## Instrukcje szczegółowe

1. **Identyfikuj elementy**: Znajdź wszystkie wzmianki o elementach infrastruktury w tekście
2. **Ekstrahuj parametry**: Wyciągnij wartości liczbowe i jednostki miary
3. **Określ relacje**: Zidentyfikuj jak elementy są ze sobą powiązane
4. **Wymagania**: Znajdź wymagania techniczne i normy
5. **Nadaj ID**: Każdemu elementowi nadaj unikalny identyfikator (n1, n2, n3...)
6. **Użyj precyzyjnych typów**: Wybierz najbardziej odpowiedni typ z listy
7. **Zachowaj kontekst**: Uwzględnij informacje o lokalizacji i warunkach

## Uwagi
- Jeśli parametr nie jest podany, pomiń go w JSON
- Jeśli relacja nie jest jasna, pomiń ją
- Używaj standardowych jednostek (mm, m, %, m³/h)
- Zachowaj oryginalne nazwy elementów w polu "name"
- Grupuj powiązane elementy w jednym zestawie relacji
