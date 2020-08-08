virtualenv -p /usr/bin/python3 virtualenvironment/project_1

source virtualenvironment/project_1/bin/activate

cd virtualenvironment/project_1/

pip3 install scikit-build
pip3 install pipenv

git clone https://github.com/ShenWang9202/epanet-python.git


cd epanet-python/
git submodule update --init
cd owa-epanet

./scripts/clean.sh

python3 setup.py sdist bdist_wheel

cd test && pipenv install ../dist/*.whl && pipenv install pytest && pipenv run pytest
