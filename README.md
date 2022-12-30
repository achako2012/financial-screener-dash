## Design
```
stocks
 ┣ package_example
 ┃ ┣ __init__.py
 ┃ ┣ core.py
 ┃ ┗ helpers.py
 ┣ .gitignore
 ┣ LICENSE
 ┣ README.md
 ┣ main.py
 ┣ requirements.txt
 ┗ setup.py
 ```

## Installation
Install all packages from setup.py
```bash
pip3 install -e
```

## Usage:
```python
python3 main.py
```

or

```python
python3
from package_example import is_number
is_number(10)
```