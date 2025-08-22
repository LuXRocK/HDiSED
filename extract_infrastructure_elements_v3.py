#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finalna wersja skryptu do ekstrakcji elementów infrastruktury z dokumentów technicznych
i uporządkowania ich w standardowym formacie: [Element] — [Opis] — [Parametry]
"""

import re
import os
from typing import List, Dict, Tuple

class InfrastructureExtractorV3:
    def __init__(self):
        # Bardziej precyzyjne wzorce do identyfikacji elementów z parametrami
        self.element_patterns = [
            # Rury z konkretnymi parametrami
            (r'ru[ry] (?:ciśnieniowe|polietylenowe) (?:z )?PE(?:100|HD)? SDR17 PN10', 'rury'),
            (r'ru[ry] (?:ciśnieniowe|polietylenowe) (?:z )?PE(?:100|HD)?', 'rury'),
            (r'ru[ry] (?:żeliwne|stalowe|kamionkowe)', 'rury'),
            (r'ru[ry] (?:PVC|PVC-U)', 'rury'),
            (r'ru[ry] (?:ochronne|osłonowe)', 'rury'),
            
            # Armatura z konkretnymi typami
            (r'zasuwa(?: kołnierzowa| podziemna| nadziemna)? (?:typu E|z miękkim uszczelnieniem)', 'armatura'),
            (r'hydrant(?: podziemny| nadziemny)? (?:HN \d+|nadziemny)', 'armatura'),
            (r'zawór (?:kulowy|kinetyczny|odpowietrzający|napowietrzający)', 'armatura'),
            (r'zawór (?:zwrotny|odcinający|burzowy)', 'armatura'),
            (r'klapa zwrotna', 'armatura'),
            
            # Kształtki z konkretnymi typami
            (r'trójnik(?: żeliwny| równoprzelotowy| redukcyjny)?', 'kształtki'),
            (r'zwężka(?: dwukołnierzowa)?', 'kształtki'),
            (r'króciec(?: jednokołnierzowy| dwukołnierzowy| kielichowo-kołnierzowy)?', 'kształtki'),
            (r'łuk kołnierzowy', 'kształtki'),
            (r'opaska(?: samonawiercająca)?', 'kształtki'),
            (r'nawiertka(?: samonawiercająca)?', 'kształtki'),
            
            # Studnie i komory
            (r'studnia(?: rewizyjna| kaskadowa)?', 'studnie'),
            (r'komora(?: rozprężna)?', 'studnie'),
            (r'przepompownia(?: ścieków)?', 'studnie'),
            (r'syfon', 'studnie'),
            (r'zamknięcie kanałowe', 'studnie'),
            (r'przewietrznik', 'studnie'),
            
            # Przewody z konkretnymi typami
            (r'przewód (?:magistralny|rozdzielczy|przyłączeniowy)', 'przewody'),
            (r'przewód (?:wodociągowy|kanalizacyjny|tłoczny)', 'przewody'),
            (r'przyłącz(?: wodociągowy| kanalizacyjny)?', 'przewody'),
            (r'kanał(?: sanitarny| deszczowy| ogólnospławny)?', 'przewody'),
            (r'kolektor(?: boczny| zbiorczy)?', 'przewody'),
            (r'rurociąg(?: tłoczny| grawitacyjny)?', 'przewody'),
            
            # Uzbrojenie
            (r'skrzynka(?: uliczna| do zasuw)?', 'uzbrojenie'),
            (r'obudowa(?: teleskopowa)?', 'uzbrojenie'),
            (r'wodomierz(?: główny| domowy)?', 'uzbrojenie'),
            (r'zestaw (?:wodomierzowy| hydrantowy)', 'uzbrojenie'),
            (r'blok oporowy', 'uzbrojenie'),
            (r'przykrycie', 'uzbrojenie'),
            (r'osłona', 'uzbrojenie')
        ]

    def extract_elements(self, content: str) -> List[Dict]:
        """Ekstrakcja elementów infrastruktury z tekstu"""
        elements = []
        
        # Podział na zdania i akapity
        sentences = re.split(r'[.!?]\s+', content)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:  # Pomijamy zbyt krótkie zdania
                continue
                
            # Sprawdzenie każdego wzorca
            for pattern, category in self.element_patterns:
                matches = re.finditer(pattern, sentence, re.IGNORECASE)
                for match in matches:
                    element_text = match.group(0)
                    
                    # Ekstrakcja parametrów z kontekstu
                    params = self.extract_parameters_from_context(sentence, element_text)
                    
                    # Tworzenie opisu
                    description = self.create_description_from_context(sentence, element_text)
                    
                    # Sprawdzenie czy element nie jest duplikatem
                    if not self.is_duplicate(elements, element_text, description):
                        elements.append({
                            'element': element_text,
                            'kategoria': category,
                            'opis': description,
                            'parametry': params,
                            'kontekst': sentence
                        })
        
        return elements

    def extract_parameters_from_context(self, sentence: str, element: str) -> Dict[str, str]:
        """Ekstrakcja parametrów z kontekstu zdania"""
        params = {}
        
        # Bardziej precyzyjne wzorce parametrów
        param_patterns = [
            # Średnica z różnymi formatami - bardziej precyzyjne
            (r'DN\s*(\d+(?:\.\d+)?)', 'średnica'),  # DN 150, DN 200
            (r'(\d+(?:\.\d+)?)\s*mm\s*(?:średnicy|DN|dz|Ø)', 'średnica'),  # 150 mm średnicy
            (r'średnica\s*(\d+(?:\.\d+)?)\s*(?:mm|m)', 'średnica'),  # średnica 150 mm
            (r'(\d+(?:\.\d+)?)\s*(?:mm|m)\s*(?:ru[ry]|przewodu|kanału)', 'średnica'),  # 150 mm rury
            
            # Długość
            (r'długość\s*(\d+(?:\.\d+)?)\s*(?:m|km)', 'długość'),  # długość 50 m
            (r'(\d+(?:\.\d+)?)\s*(?:m|km)\s*długości', 'długość'),  # 50 m długości
            
            # Przepływ
            (r'przepływ\s*(\d+(?:\.\d+)?)\s*(?:m3/h|l/s)', 'przepływ'),  # przepływ 20 m3/h
            (r'(\d+(?:\.\d+)?)\s*(?:m3/h|l/s)\s*przepływu', 'przepływ'),  # 20 m3/h przepływu
            
            # Ciśnienie
            (r'ciśnienie\s*(\d+(?:\.\d+)?)\s*(?:bar|MPa)', 'ciśnienie'),  # ciśnienie 10 bar
            (r'PN\s*(\d+(?:\.\d+)?)', 'ciśnienie'),  # PN 10
            
            # Głębokość
            (r'głębokość\s*(\d+(?:\.\d+)?)\s*(?:m|cm)', 'głębokość'),  # głębokość 2 m
            (r'zagłębienie\s*(\d+(?:\.\d+)?)\s*(?:m|cm)', 'głębokość'),  # zagłębienie 2 m
            
            # Spadek
            (r'spadek\s*(\d+(?:\.\d+)?)\s*(?:%|‰|0/00)', 'spadek'),  # spadek 2%
            (r'(\d+(?:\.\d+)?)\s*(?:%|‰|0/00)\s*spadku', 'spadek'),  # 2% spadku
            
            # Napełnienie
            (r'napełnienie\s*(\d+(?:\.\d+)?)\s*%', 'napełnienie'),  # napełnienie 80%
            (r'(\d+(?:\.\d+)?)\s*%\s*napełnienia', 'napełnienie'),  # 80% napełnienia
            
            # Prędkość
            (r'prędkość\s*(\d+(?:\.\d+)?)\s*(?:m/s|km/h)', 'prędkość'),  # prędkość 2 m/s
            (r'(\d+(?:\.\d+)?)\s*(?:m/s|km/h)\s*prędkości', 'prędkość'),  # 2 m/s prędkości
            
            # Grubość
            (r'grubość\s*(\d+(?:\.\d+)?)\s*(?:mm|cm)', 'grubość'),  # grubość 10 mm
            (r'(\d+(?:\.\d+)?)\s*(?:mm|cm)\s*grubości', 'grubość'),  # 10 mm grubości
            
            # Odległość
            (r'odległość\s*(\d+(?:\.\d+)?)\s*(?:m|km)', 'odległość'),  # odległość 5 m
            (r'(\d+(?:\.\d+)?)\s*(?:m|km)\s*odległości', 'odległość'),  # 5 m odległości
        ]
        
        for pattern, param_type in param_patterns:
            matches = re.finditer(pattern, sentence, re.IGNORECASE)
            for match in matches:
                value = match.group(1)
                unit = self.extract_unit_from_match(match.group(0))
                if param_type not in params:  # Pierwszy znaleziony parametr danego typu
                    params[param_type] = f"{value} {unit}"
        
        return params

    def extract_unit_from_match(self, text: str) -> str:
        """Ekstrakcja jednostki z dopasowanego tekstu"""
        units = {
            'mm': 'mm', 'm': 'm', 'km': 'km',
            'm3/h': 'm³/h', 'l/s': 'l/s',
            'bar': 'bar', 'MPa': 'MPa',
            'cm': 'cm', '%': '%', '‰': '‰', '0/00': '‰',
            'm/s': 'm/s', 'km/h': 'km/h'
        }
        
        for unit in units:
            if unit in text:
                return units[unit]
        return ''

    def create_description_from_context(self, sentence: str, element: str) -> str:
        """Tworzenie opisu z kontekstu zdania"""
        # Usunięcie elementu z opisu
        description = sentence.replace(element, '').strip()
        
        # Usunięcie nadmiarowych spacji i znaków
        description = re.sub(r'\s+', ' ', description)
        description = re.sub(r'^[.,\s]+', '', description)
        description = re.sub(r'[.,\s]+$', '', description)
        
        # Usunięcie numerów sekcji
        description = re.sub(r'^\d+\.\s*', '', description)
        
        # Usunięcie nadmiarowych znaków
        description = re.sub(r'[•\-\*]\s*', '', description)
        
        # Ograniczenie długości
        if len(description) > 120:
            description = description[:120] + '...'
        
        return description if description else 'brak opisu'

    def is_duplicate(self, elements: List[Dict], element_text: str, description: str) -> bool:
        """Sprawdzenie czy element nie jest duplikatem"""
        for existing in elements:
            if (existing['element'].lower() == element_text.lower() and 
                existing['opis'][:50] == description[:50]):
                return True
        return False

    def format_element(self, element: Dict) -> str:
        """Formatowanie elementu w standardowym formacie"""
        element_name = element['element']
        description = element['opis']
        
        # Formatowanie parametrów
        params_list = []
        for param_type, value in element['parametry'].items():
            if param_type == 'średnica':
                params_list.append(f"średnica {value}")
            elif param_type == 'długość':
                params_list.append(f"długość {value}")
            elif param_type == 'przepływ':
                params_list.append(f"przepływ {value}")
            elif param_type == 'ciśnienie':
                params_list.append(f"ciśnienie {value}")
            elif param_type == 'głębokość':
                params_list.append(f"głębokość {value}")
            elif param_type == 'spadek':
                params_list.append(f"spadek {value}")
            elif param_type == 'napełnienie':
                params_list.append(f"napełnienie {value}")
            elif param_type == 'prędkość':
                params_list.append(f"prędkość {value}")
            elif param_type == 'grubość':
                params_list.append(f"grubość {value}")
            elif param_type == 'odległość':
                params_list.append(f"odległość {value}")
        
        params_str = ', '.join(params_list) if params_list else 'brak parametrów'
        
        return f"{element_name} — {description} — {params_str}"

def process_file(input_file: str, output_file: str):
    """Przetwarzanie pojedynczego pliku"""
    print(f"Przetwarzam plik: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    extractor = InfrastructureExtractorV3()
    elements = extractor.extract_elements(content)
    
    # Zapisywanie wyników
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Elementy infrastruktury wyekstrahowane z {input_file}\n\n")
        
        # Grupowanie według kategorii
        categories = {}
        for element in elements:
            cat = element['kategoria']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(element)
        
        # Zapisywanie według kategorii
        for category, cat_elements in categories.items():
            f.write(f"## {category.upper()}\n\n")
            
            for element in cat_elements:
                formatted = extractor.format_element(element)
                f.write(f"{formatted}\n")
            
            f.write("\n")
        
        # Statystyki
        f.write(f"## Statystyki\n\n")
        f.write(f"Łącznie znaleziono: {len(elements)} elementów\n\n")
        for category, cat_elements in categories.items():
            f.write(f"- {category}: {len(cat_elements)} elementów\n")
    
    print(f"Zapisano wyniki do: {output_file}")
    print(f"Znaleziono {len(elements)} elementów infrastruktury")
    print("-" * 50)

def main():
    """Główna funkcja"""
    files_to_process = [
        ('projektextracted.txt', 'projekt_elements_final.txt'),
        ('specyfikacjaextracted.txt', 'specyfikacja_elements_final.txt'),
        ('wytyczneextracted.txt', 'wytyczne_elements_final.txt')
    ]
    
    for input_file, output_file in files_to_process:
        if os.path.exists(input_file):
            process_file(input_file, output_file)
        else:
            print(f"Plik {input_file} nie istnieje!")

if __name__ == "__main__":
    main()
