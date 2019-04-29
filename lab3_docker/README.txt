Tabele:

-LISTENED_SONG
-- jest to tabela faktów w schemacie gwiazdy
-- kluczem głównym jest id utworu
-- zawiera informacje o id użytkownika
-- kluczami obcymi są klucze do pozostałych dwóch tabel 
   opisanych poniżej - id daty i id utworu

-SONG
-- jeden z dwóch wymiarów
-- kluczem głównym jest id utworu
-- pozostałe kolumny to informacje o utworze (tytuł, artysta) pobierane 
   z pliku unique_tracks.txt

-DATE
-- jeden z dwóch wymiarów
-- kluczem głównym jest data w postaci czasu uniksowego,
-- pozostałe kolumny rok, miesiąc, ..., sekunda są odzytywane z klucza głównego
   przy wstawianiu danych do tabeli. Przyspiesza to przetwarzanie przy podpunkcie 4.
