# AquaEmi

**AquaEmi** is a product aim to identify, control and evaluate environmental effects of water pollution.

Uses [Flask](https://flask.palletsprojects.com/en/2.3.x/) for back-end, [MySQL](https://www.mysql.com/) for database.

## Installation & usage

- (Optional) Create a virtual environment

Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```
    
Windows:
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

If there is error with "Execution Policies", run:
```bash
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
```

- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install require packages.
```bash
pip install -r requirements.txt
```

- To run:
```bash
flask run 
```