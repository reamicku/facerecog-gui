# System rozpoznawania twarzy

## Opis

Prosty interfejs do rozpoznawania twarzy 

  - Zbieranie zdjęć twarzy
  - Tworzenie klasyfikatora 
  - Wykrywanie twarzy

## Korzystanie z aplikacji

Zainstaluj Python 3.10:

https://www.python.org/downloads/release/python-31011

Przygotuj i wepnij kamerkę internetową do komputera. Możesz używać [telefonu jako kamerkę internetową.](#używanie-telefonu-jako-kamerki)

Uruchom aplikację poprzez jeden z plików w zależności od twojego systemu operacyjnego. Program pobierze wszystkie zależności.

System | Plik
-|-
Windows | `start.bat`
Linux   | `start.sh`

### Tworzenie użytkownika

1. Przejdź do `Utwórz użytkownika`.
2. Wprowadź imię dla użytkownika i przejdź dalej.
3. Kliknij w `Utwórz zbiór danych`. Program rozpocznie zbieranie zdjęć twarzy potrzebnych do utworzenia modelu klasyfikującego.
4. Po zebraniu zdjęć kliknij w `Trenuj Model`. Czas trewnowania modelu jest zależny od wydajności twojego komputera.

## Rozpoznawanie użytkowników

1. Przejdź do `Rozpoznaj użytkownika`.
2. Wybierz użytkownika z listy, którego program będzie próbował rozpoznać.
3. Kliknij `Rozpocznij`. Program będzie pobierał obraz z kamerki i oznaczał rozpoznaną osobę w zielonym prostokącie.

## Używanie telefonu jako kamerki

### Linux

Można użyć telefonu jako kamerki na Linuxie za pomocą `scrcpy`.

Wymagany moduł `v4l2`.

https://github.com/Genymobile/scrcpy

https://github.com/Genymobile/scrcpy/blob/master/doc/camera.md

Po uruchomieniu polecenia będzie udostępniona przednia kamerka:

```bash
scrcpy --camera-id=1 --video-source=camera --no-audio --camera-size=1296x970 --v4l2-sink=/dev/video0
```

### Windows

DroidCam

Klient Windows - https://www.dev47apps.com/droidcam/windows

Aplikacja mobilna - https://play.google.com/store/apps/details?id=com.dev47apps.droidcam

## Usuwanie danych

Usuń cały katalog `data`.


## Licencja

Licencja [WTFPL](./LICENSE)
