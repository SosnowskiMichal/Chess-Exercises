#!/bin/bash

if [ ! -f "requirements.txt" ]; then
    echo "File requirements.txt not found"
    exit 1
fi

echo "Installing depedencies..."
pip install -r requirements.txt

FILE_PATH="./data/users_db.db"

if [ ! -f "$FILE_PATH" ]; then
    echo "File $FILE_PATH not found"
    echo "Creating database..."
    python -c "from data_managers import UserDataManager; udm = UserDataManager(); udm.create_database(); udm.add_user('default')"
    if [ $? -ne 0 ]; then
        echo "An error occured while creating database."
        exit 1
    fi
fi

echo "Running the application..."
python main.py