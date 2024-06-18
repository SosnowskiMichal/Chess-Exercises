@echo off
if not exist requirements.txt (
    echo File requirements.txt not found
    exit /b 1
)

echo Installing depedencies...
pip install -r requirements.txt

set FILE_PATH=.\data\users_db.db

if not exist "%FILE_PATH%" (
    echo File %FILE_PATH% not found
    echo Creating database...
    python -c "from data_managers import UserDataManager; udm = UserDataManager(); udm.create_database(); udm.add_user('default')"
    if %errorlevel% neq 0 (
        echo An error occured while creating database.
        exit /b 1
    )
)

echo Running the application...
python main.py