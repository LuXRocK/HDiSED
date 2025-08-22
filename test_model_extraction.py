#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrypt do testowania modelu LLM na ekstrakcji elementów i relacji infrastruktury
Porównuje wyniki z anotacjami referencyjnymi
"""

import json
import re
from typing import Dict, List, Tuple
from difflib import SequenceMatcher

class ModelTester:
    def __init__(self):
        self.test_cases = [
            {
                "id": "test1",
                "text": "Zestaw hydrantowy (komplet): żeliwny hydrant nadziemny HN 100, sztywny; łuk kołnierzowy 90º ze stopką DN 100 z żeliwa sferoidalnego; zasuwa kołnierzowa typu E DN 100 miękkouszczelniająca zasuwa klinowa; króciec dwukołnierzowy kształtka FF 100 z żeliwa sferoidalnego",
                "expected": {
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
            },
            {
                "id": "test2", 
                "text": "Dla średnic kolektorów DN 150 na odcinkach prostych studnie rozmieszczać co 35 m",
                "expected": {
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
            },
            {
                "id": "test3",
                "text": "Minimalny spadek na przyłączu sanitarnym należy przyjmować: dla DN 150 – 1,5%, DN 200 – 1%",
                "expected": {
                    "elements": [
                        {"id": "n1", "type": "przyłącz", "name": "Przyłącz sanitarny DN 150", "params": {"średnica_mm": 150}},
                        {"id": "n2", "type": "przyłącz", "name": "Przyłącz sanitarny DN 200", "params": {"średnica_mm": 200}}
                    ],
                    "relations": [
                        {"type": "has_requirement", "from": "n1", "to": "req1"},
                        {"type": "has_requirement", "from": "n2", "to": "req2"}
                    ],
                    "requirements": [
                        {"id": "req1", "type": "slope_min", "value": 1.5, "unit": "%"},
                        {"id": "req2", "type": "slope_min", "value": 1.0, "unit": "%"}
                    ]
                }
            },
            {
                "id": "test4",
                "text": "Projektować pokrywy komór z włazów żeliwnych o średnicy DN 800 z zamknięciem antywłamaniowym",
                "expected": {
                    "elements": [
                        {"id": "n1", "type": "komora", "name": "Komora kanalizacyjna"},
                        {"id": "n2", "type": "właz", "name": "Właz żeliwny", "params": {"średnica_mm": 800}}
                    ],
                    "relations": [
                        {"type": "covers", "from": "n2", "to": "n1"}
                    ]
                }
            },
            {
                "id": "test5",
                "text": "Zaleca się zastosowanie rur polietylenowych, ciśnieniowych PE100 SDR17 PN10 o wymiarach rury 160x9,5mm (DN150), 110x6,6mm (DN100)",
                "expected": {
                    "elements": [
                        {"id": "n1", "type": "rura", "name": "Rura PE100 SDR17 PN10", "params": {"średnica_mm": 160, "grubość_ścianki_mm": 9.5, "DN": 150}},
                        {"id": "n2", "type": "rura", "name": "Rura PE100 SDR17 PN10", "params": {"średnica_mm": 110, "grubość_ścianki_mm": 6.6, "DN": 100}}
                    ],
                    "relations": []
                }
            }
        ]

    def load_annotations(self, file_path: str) -> List[Dict]:
        """Ładowanie anotacji referencyjnych z pliku JSONL"""
        annotations = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    annotations.append(json.loads(line))
        return annotations

    def simulate_model_response(self, text: str) -> Dict:
        """
        Symulacja odpowiedzi modelu LLM
        W rzeczywistości tutaj byłby wywołanie API modelu
        """
        # To jest uproszczona symulacja - w rzeczywistości byłby tu prompt do LLM
        result = {
            "elements": [],
            "relations": [],
            "requirements": []
        }
        
        # Prosta ekstrakcja elementów na podstawie wzorców
        element_patterns = [
            (r'hydrant.*?HN\s*(\d+)', 'hydrant', 'Hydrant nadziemny HN {}'),
            (r'zasuwa.*?DN\s*(\d+)', 'zasuwa', 'Zasuwa kołnierzowa DN {}'),
            (r'kolektor.*?DN\s*(\d+)', 'kolektor', 'Kolektor DN {}'),
            (r'przyłącz.*?DN\s*(\d+)', 'przyłącz', 'Przyłącz DN {}'),
            (r'właz.*?DN\s*(\d+)', 'właz', 'Właz DN {}'),
            (r'rura.*?(\d+)x(\d+)mm.*?DN(\d+)', 'rura', 'Rura {}x{}mm DN{}')
        ]
        
        element_id = 1
        for pattern, element_type, name_template in element_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if element_type == 'rura':
                    diameter, thickness, dn = match.groups()
                    result["elements"].append({
                        "id": f"n{element_id}",
                        "type": element_type,
                        "name": name_template.format(diameter, thickness, dn),
                        "params": {
                            "średnica_mm": int(diameter),
                            "grubość_ścianki_mm": float(thickness),
                            "DN": int(dn)
                        }
                    })
                else:
                    diameter = match.group(1)
                    result["elements"].append({
                        "id": f"n{element_id}",
                        "type": element_type,
                        "name": name_template.format(diameter),
                        "params": {"średnica_mm": int(diameter)}
                    })
                element_id += 1
        
        # Prosta ekstrakcja relacji
        if len(result["elements"]) > 1:
            for i in range(len(result["elements"]) - 1):
                result["relations"].append({
                    "type": "connected_to",
                    "from": result["elements"][i]["id"],
                    "to": result["elements"][i + 1]["id"]
                })
        
        return result

    def compare_results(self, expected: Dict, actual: Dict) -> Dict:
        """Porównanie wyników z oczekiwanymi"""
        comparison = {
            "elements_accuracy": 0.0,
            "relations_accuracy": 0.0,
            "requirements_accuracy": 0.0,
            "overall_accuracy": 0.0,
            "details": {
                "elements_matched": 0,
                "elements_total": len(expected.get("elements", [])),
                "relations_matched": 0,
                "relations_total": len(expected.get("relations", [])),
                "requirements_matched": 0,
                "requirements_total": len(expected.get("requirements", []))
            }
        }
        
        # Porównanie elementów
        expected_elements = expected.get("elements", [])
        actual_elements = actual.get("elements", [])
        
        for exp_elem in expected_elements:
            for act_elem in actual_elements:
                if (exp_elem["type"] == act_elem["type"] and 
                    exp_elem["name"] == act_elem["name"]):
                    comparison["details"]["elements_matched"] += 1
                    break
        
        # Porównanie relacji
        expected_relations = expected.get("relations", [])
        actual_relations = actual.get("relations", [])
        
        for exp_rel in expected_relations:
            for act_rel in actual_relations:
                if (exp_rel["type"] == act_rel["type"] and
                    exp_rel["from"] == act_rel["from"] and
                    exp_rel["to"] == act_rel["to"]):
                    comparison["details"]["relations_matched"] += 1
                    break
        
        # Porównanie wymagań
        expected_reqs = expected.get("requirements", [])
        actual_reqs = actual.get("requirements", [])
        
        for exp_req in expected_reqs:
            for act_req in actual_reqs:
                if (exp_req["type"] == act_req["type"] and
                    exp_req.get("value") == act_req.get("value")):
                    comparison["details"]["requirements_matched"] += 1
                    break
        
        # Obliczenie dokładności
        if comparison["details"]["elements_total"] > 0:
            comparison["elements_accuracy"] = comparison["details"]["elements_matched"] / comparison["details"]["elements_total"]
        
        if comparison["details"]["relations_total"] > 0:
            comparison["relations_accuracy"] = comparison["details"]["relations_matched"] / comparison["details"]["relations_total"]
        
        if comparison["details"]["requirements_total"] > 0:
            comparison["requirements_accuracy"] = comparison["details"]["requirements_matched"] / comparison["details"]["requirements_total"]
        
        # Dokładność ogólna
        total_expected = (comparison["details"]["elements_total"] + 
                         comparison["details"]["relations_total"] + 
                         comparison["details"]["requirements_total"])
        
        total_matched = (comparison["details"]["elements_matched"] + 
                        comparison["details"]["relations_matched"] + 
                        comparison["details"]["requirements_matched"])
        
        if total_expected > 0:
            comparison["overall_accuracy"] = total_matched / total_expected
        
        return comparison

    def run_tests(self) -> Dict:
        """Uruchomienie wszystkich testów"""
        results = {
            "test_cases": [],
            "summary": {
                "total_tests": len(self.test_cases),
                "average_accuracy": 0.0,
                "elements_accuracy": 0.0,
                "relations_accuracy": 0.0,
                "requirements_accuracy": 0.0
            }
        }
        
        total_accuracy = 0.0
        total_elements_acc = 0.0
        total_relations_acc = 0.0
        total_requirements_acc = 0.0
        
        for test_case in self.test_cases:
            print(f"Testowanie: {test_case['id']}")
            print(f"Tekst: {test_case['text'][:100]}...")
            
            # Symulacja odpowiedzi modelu
            model_response = self.simulate_model_response(test_case["text"])
            
            # Porównanie z oczekiwanymi wynikami
            comparison = self.compare_results(test_case["expected"], model_response)
            
            test_result = {
                "id": test_case["id"],
                "text": test_case["text"],
                "expected": test_case["expected"],
                "actual": model_response,
                "comparison": comparison
            }
            
            results["test_cases"].append(test_result)
            
            total_accuracy += comparison["overall_accuracy"]
            total_elements_acc += comparison["elements_accuracy"]
            total_relations_acc += comparison["relations_accuracy"]
            total_requirements_acc += comparison["requirements_accuracy"]
            
            print(f"  Dokładność ogólna: {comparison['overall_accuracy']:.2%}")
            print(f"  Elementy: {comparison['elements_accuracy']:.2%}")
            print(f"  Relacje: {comparison['relations_accuracy']:.2%}")
            print(f"  Wymagania: {comparison['requirements_accuracy']:.2%}")
            print("-" * 50)
        
        # Podsumowanie
        results["summary"]["average_accuracy"] = total_accuracy / len(self.test_cases)
        results["summary"]["elements_accuracy"] = total_elements_acc / len(self.test_cases)
        results["summary"]["relations_accuracy"] = total_relations_acc / len(self.test_cases)
        results["summary"]["requirements_accuracy"] = total_requirements_acc / len(self.test_cases)
        
        return results

    def save_results(self, results: Dict, output_file: str):
        """Zapisanie wyników do pliku JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

def main():
    """Główna funkcja"""
    tester = ModelTester()
    
    print("=== TESTY MODELU LLM - EKSTRAKCJA ELEMENTÓW I RELACJI ===\n")
    
    # Uruchomienie testów
    results = tester.run_tests()
    
    # Wyświetlenie podsumowania
    print("\n=== PODSUMOWANIE ===")
    print(f"Liczba testów: {results['summary']['total_tests']}")
    print(f"Dokładność ogólna: {results['summary']['average_accuracy']:.2%}")
    print(f"Dokładność elementów: {results['summary']['elements_accuracy']:.2%}")
    print(f"Dokładność relacji: {results['summary']['relations_accuracy']:.2%}")
    print(f"Dokładność wymagań: {results['summary']['requirements_accuracy']:.2%}")
    
    # Zapisanie wyników
    tester.save_results(results, "test_results.json")
    print(f"\nWyniki zapisane do: test_results.json")

if __name__ == "__main__":
    main()
