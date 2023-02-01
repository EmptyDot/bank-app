# bank-app

[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EmptyDot/651703a1c1bca09b4e9b8f3e8a4d60e1/raw/coverage_endpoint.json)](https://github.com/EmptyDot/bank-app/actions/workflows/coverage.yml)

[GitHub repo](https://github.com/EmptyDot/bank-app)
## Running
The program is designed to run from [main.ipynb](main.ipynb). 
There you will see a demonstration of the program.
Requires python 3.9+

## Bank
The bank class is the primary object that you will interact with.

```python
bank = Bank()
```

## Save
If you don't want the bank to save customers when exiting the program set `save_on_exit=False`
```python
bank = Bank(save_on_exit=False)
```

Bank also takes a `save_file_path` argument if you want to define a custom path to save customers to.
```python
bank = Bank(save_file_path="my_file.json")
```

To load customers from a file, call `bank.load_customers()`. This method takes an optional `file_path` argument.

If you don't specify save and load file path arguments, the program will load from and save to the same file at [saved_customers.json](bank_app/data/saved_customers.json).

I'm using json format to save/load customers. To see how it works see [parser_json.py](bank_app/parser_json.py)

## Logs
I've created a logger that logs if anything goes wrong during runtime. 
The log file can be found at [bankapp.log](bank_app/logs/bankapp.log) and the logger at [logger.py](bank_app/logger.py).

## Test
I've written test that can be found in [tests](tests) 

To run the tests:

Install pytest:
```
pip install pytest
```
Navigate  to the root of the repo
You should be in the same directory as [main.ipynb](main.ipynb)  

Run the tests:
```
pytest
```
