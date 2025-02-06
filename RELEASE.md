Set up a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # For Unix
venv\Scripts\activate     # For Windows
export PYTHONPATH=$(pwd)
```

Install the requirements:

```bash
pip3 install -r dev-requirements.txt
```

Update the version number in the pyproject.toml file:

```toml
version = "x.x.x"
```

Build the distribution:

```bash
flit build
```

Publish the distribution:

```bash
flit publish
```


