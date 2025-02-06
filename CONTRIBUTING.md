Fetch the source code:

```bash
git clone https://github.com/tpmccallum/PyVeritas.git
cd PyVeritas
export PYTHONPATH=$(pwd)
```

Set up a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # For Unix
venv\Scripts\activate     # For Windows
```

Install the requirements:

```bash
pip3 install -r dev-requirements.txt
```

Update the documentation:

```bash
sphinx-apidoc -o docs/ pyveritas
make html
```
