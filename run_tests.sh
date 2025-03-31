#!/bin/bash

echo "Running Django tets with MongoDB....."

python manage.py test

python -m unittest discover -s inventory -p "integration_test_with_local_mongo_db.py"

if [ $? -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Tests failed"
    exit 1

fi
