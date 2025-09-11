# Raport z analizy ekstrakcji grafu infrastruktury

## 1. Wstęp

Celem projektu było zbadanie możliwości wykorzystania dużych modeli językowych (LLM) do automatycznej ekstrakcji grafu infrastruktury z opisu tekstowego. W ramach projektu przetestowano cztery modele: `mistral`, `llama3`, `phi3` i `gemma`.

## 2. Przebieg prac

Początkowe próby ekstrakcji grafu przy użyciu modelu `mistral` zakończyły się niepowodzeniem. Wystąpił błąd "Server disconnected without sending a response", który uniemożliwiał uzyskanie odpowiedzi od modelu. Problem ten został rozwiązany poprzez dodanie parametru `timeout` w skrypcie `src/extract_graph.py`, co zapewniło stabilne połączenie z serwerem Ollama.

Po rozwiązaniu problemu z połączeniem, pojawił się kolejny błąd, tym razem związany z walidacją danych. Model `mistral` generował graf w poprawnym formacie JSON, jednak wartości w polu `type` nie były zgodne z predefiniowanym schematem. Przykładowo, model generował typy takie jak `Stacja Pomp Główna` zamiast oczekiwanego `Pompownia`.

Problem ten został rozwiązany poprzez iteracyjne poprawianie promptu. Do promptu dodano bardziej szczegółowe instrukcje oraz przykłady mapowania, które jednoznacznie wskazywały, jak model ma klasyfikować poszczególne elementy infrastruktury. Po tych zmianach, wszystkie testowane modele (`mistral`, `llama3`, `phi3`, `gemma`) były w stanie poprawnie wyekstrahować graf z opisu tekstowego.

## 3. Analiza wyników

### Dlaczego wyniki z różnych modeli mogą być tak różne?

Różnice w wynikach generowanych przez poszczególne modele wynikają z kilku czynników:

*   **Architektura i dane treningowe:** Każdy model ma inną architekturę i był trenowany na innym zbiorze danych. To sprawia, że modele mają różną "wiedzę" i "rozumienie" świata, co wpływa na to, jak interpretują tekst i wykonują zadania.
*   **Zdolność do podążania za instrukcjami:** Niektóre modele są lepsze w precyzyjnym podążaniu za instrukcjami zawartymi w prompcie. Inne mogą mieć tendencję do "halucynacji" lub generowania odpowiedzi, które są tylko częściowo zgodne z oczekiwaniami.
*   **Interpretacja promptu:** Nawet przy tym samym prompcie, różne modele mogą go inaczej interpretować. To, co dla jednego modelu jest jasne i jednoznaczne, dla innego może być nieprecyzyjne.

### Dlaczego żaden z modeli nie odniósł sukcesu na początku?

Początkowe niepowodzenie wszystkich modeli wynikało z dwóch głównych przyczyn:

1.  **Niewystarczająco precyzyjny prompt:** Pierwsza wersja promptu była zbyt ogólna. Modele nie miały wystarczająco dużo informacji, aby zrozumieć, jak dokładnie mają mapować znalezione w tekście elementy na predefiniowane typy w schemacie grafu. Brakowało konkretnych przykładów, które pokazałyby oczekiwany sposób działania.
2.  **Problem techniczny:** Błąd "Server disconnected" był problemem technicznym, a nie błędem modeli. Uniemożliwiał on jakąkolwiek komunikację z modelami, co sprawiało wrażenie, że żaden z nich nie jest w stanie wykonać zadania.

## 4. Wnioski

Projekt pokazał, że duże modele językowe mogą być potężnym narzędziem do automatycznej ekstrakcji informacji z tekstu. Kluczem do sukcesu jest jednak precyzyjne formułowanie poleceń (prompt engineering) oraz zapewnienie stabilnego środowiska technicznego.

Najważniejsze wnioski z projektu:

*   **Prompt engineering jest kluczowy:** Jakość wyników generowanych przez modele LLM jest w dużej mierze zależna od jakości promptu. Im bardziej precyzyjne i jednoznaczne są instrukcje, tym lepsze wyniki można uzyskać.
*   **Iteracyjne podejście:** W przypadku problemów z modelami, najlepsze rezultaty przynosi iteracyjne podejście, polegające na stopniowym poprawianiu promptu i analizowaniu wyników.
*   **Obsługa błędów:** Należy zadbać o odpowiednią obsługę błędów i zarządzanie połączeniem z modelami, aby uniknąć problemów technicznych, które mogą zakłócić proces ekstrakcji.

Ostatecznie, po wprowadzeniu odpowiednich poprawek, wszystkie testowane modele okazały się zdolne do poprawnego wykonania zadania, co potwierdza ich potencjał w tego typu zastosowaniach.
