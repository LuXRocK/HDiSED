#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Poprawiony skrypt do czyszczenia dokumentów technicznych z zbędnych fragmentów
Usuwa spisy treści, nagłówki, stopki, numery stron i inne elementy administracyjne
"""

import re
import os

def clean_document(input_file, output_file):
    """
    Czyści dokument z zbędnych fragmentów
    """
    print(f"Przetwarzam plik: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_size = len(content)
    
    # Usuwanie spisów treści (tylko te z numerami stron)
    content = re.sub(r'SPIS TREŚCI\s*\n(?:.*?\n)*?(?=\d+\.\s*WSTĘP|\d+\.\s*MATERIAŁY|\d+\.\s*SPRZĘT)', '', content, flags=re.MULTILINE | re.DOTALL)
    content = re.sub(r'Spis treści\s*\n(?:.*?\n)*?(?=\d+\.\s*WSTĘP|\d+\.\s*MATERIAŁY|\d+\.\s*SPRZĘT)', '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Usuwanie nagłówków dokumentów na początku
    content = re.sub(r'^.*?SPECYFIKACJE TECHNICZNE\s*WYKONANIA I ODBIORU ROBÓT\s*ST-00\.03\s*Sieć wodociągowa\s*', '', content, flags=re.MULTILINE | re.DOTALL)
    content = re.sub(r'^.*?ROZBUDOWA PODKARPACKIEGO PARKU\s*NAUKOWO-TECHNOLOGICZNEGO\s*', '', content, flags=re.MULTILINE | re.DOTALL)
    content = re.sub(r'^.*?Miejskie Przedsiębiorstwo Wodociągów i Kanalizacji\s*', '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Usuwanie informacji o autorze
    content = re.sub(r'Opracował:\s*inŜ\.\s*Maria Kluzek\s*luty 2010 r\s*', '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Usuwanie kodów CPV
    content = re.sub(r'Kod CPV:\s*45111200-0.*?\n', '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Usuwanie numerów stron (tylko samotne numery)
    content = re.sub(r'^\s*\d+\s*$', '', content, flags=re.MULTILINE)
    
    # Usuwanie informacji o stronie
    content = re.sub(r'str\.\s*\d+.*?\n', '', content, flags=re.MULTILINE)
    
    # Usuwanie powtarzających się nagłówków
    content = re.sub(r'Specyfikacje techniczne wykonania i odbioru robót - ST-00\.03 – Sieć wodociągowa\s*', '', content, flags=re.MULTILINE)
    content = re.sub(r'SZCZEGÓŁOWA SPECYFIKACJA TECHNICZNA\s*SIEĆ WODOCIĄGOWA\s*SST – S\.1\s*', '', content, flags=re.MULTILINE)
    content = re.sub(r'Wytyczne do projektowania sieci wodociągowej i kanalizacyjnej, przyłączy\s*oraz urządzeń technicznych\.\s*', '', content, flags=re.MULTILINE)
    
    # Usuwanie informacji o przedsiębiorstwie
    content = re.sub(r'Włocławek grudzień 2009 r\.\s*', '', content, flags=re.MULTILINE)
    
    # Usuwanie pustych linii na początku
    content = re.sub(r'^\s*\n+', '', content, flags=re.MULTILINE)
    
    # Usuwanie linii z samymi kropkami (separatory)
    content = re.sub(r'^\s*\.+\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*-+\s*$', '', content, flags=re.MULTILINE)
    
    # Usuwanie przepisów prawnych na końcu (tylko jeśli to cała sekcja)
    content = re.sub(r'\n\d+\.\s*PRZEPISY ZWIĄZANE\s*\n(?:.*?\n)*$', '', content, flags=re.MULTILINE | re.DOTALL)
    content = re.sub(r'\n\d+\.\s*PODSTAWA PŁATNOŚCI\s*\n(?:.*?\n)*$', '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Usuwanie nadmiarowych pustych linii
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Usuwanie spacji na początku i końcu
    content = content.strip()
    
    # Zapisywanie wyczyszczonego dokumentu
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Zapisano wyczyszczony dokument: {output_file}")
    print(f"Rozmiar przed: {original_size} znaków")
    print(f"Rozmiar po: {len(content)} znaków")
    print(f"Usunięto: {original_size - len(content)} znaków")
    print("-" * 50)

def main():
    """
    Główna funkcja przetwarzająca wszystkie pliki
    """
    files_to_process = [
        ('projekt.txt', 'projektextracted.txt'),
        ('specyfikacja.txt', 'specyfikacjaextracted.txt'),
        ('wytyczne.txt', 'wytyczneextracted.txt')
    ]
    
    for input_file, output_file in files_to_process:
        if os.path.exists(input_file):
            clean_document(input_file, output_file)
        else:
            print(f"Plik {input_file} nie istnieje!")

if __name__ == "__main__":
    main()
