set "PACKAGELOCK_FILE=package.lock"

if not exist "%PACKAGELOCK_FILE%" (
    echo Dependencies not installed. Installing...
    pip install -r requirements.txt
    echo.>"PACKAGELOCK_FILE"
)

echo Starting face recognition application.
python app-gui.py
