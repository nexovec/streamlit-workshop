ECHO "THIS SCRIPT SETS YOU UP FOR THE FIRST RUN ONLY. AFTERWARDS YOU CAN JUST DO docker-compose up INSTEAD OF THIS SCRIPT"
pushd $(dirname "${0}") > /dev/null
python3 -m pip install virtualenv --user
python3 -m virtualenv venv
source venv/bin/activate
pip install -r webui/requirements.txt
sudo mkdir secrets
sudo docker-compose up
popd > /dev/null