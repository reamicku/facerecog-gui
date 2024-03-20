set "PACKAGELOCK_FILE=package.lock"

if not exist "%PACKAGELOCK_FILE%" (
    echo Dependencies not installed. Installing...
    python3.10 -m pip install -r requirements.txt
    echo.>"PACKAGELOCK_FILE"
)

echo Starting face recognition application.
python3.10 app-gui.py
