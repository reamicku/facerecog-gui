# System rozpoznawania twarzy

## Opis

Prosty interfejs do rozpoznawania twarzy 

  - Zbieranie zdjęć twarzy
  - Tworzenie klasyfikatora 
  - Wykrywanie twarzy

## Instalacja

Zainstaluj Python 3.10

https://www.python.org/downloads/release/python-31011

Uruchom aplikację:

System | Plik
-|-
Windows | `start.bat`
Linux   | `start.sh`

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
