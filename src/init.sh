#!/bin/bash
echo "Initialize the Database"
export FLASK_APP=app.py
flask db init
flask db migrate -m "Create articles table"
flask db upgrade

echo "Run the backend server"
python app.py