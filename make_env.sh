deactivate
python3 -m pip install virtualenv
python3 -m virtualenv venv
./venv/bin/activate

# nutne je jen tohle
pip install -r dev-requirements.txt
docker-compose build
