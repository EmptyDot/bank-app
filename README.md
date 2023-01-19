# bank-app
[![Code Coverage](https://img.shields.io/json?url=https://gist.github.com/EmptyDot/01ba42d0d77ac026245790b4fef064c2)](https://github.com/EmptyDot/bank-app/actions/workflows/test.yml)

Hej Niklas! Välkommen till min bank app!

## Körning
Programmet är designat att köras från [main.ipynb](main.ipynb). Där kan du se en demonstration hur programmet fungerar.

## Spara / ladda
För att ladda och spara kunder till samma fil (så det är menat att det ska fungera), använd `bank.load_customers()` utan några argument.  
Om du låter argumentet vara namnet på nån annan fil kommer programmet ladda från den och spara till [saved_customers.json](bank_app/data/saved_customers.json)

Jag använder json format för att spara/ladda kunder. För att se hur det funkar kolla [parser_json.py](bank_app/parser_json.py)

## Logs
Om något går fel under körningen finns en log fil att kolla på som heter [bankapp.log](bank_app/logs/bankapp.log)  
Om du är intresserad av hur loggern funkar kolla [logger.py](bank_app/logger.py)

## Test
Jag har även skrivit unit-tests som går att hitta i [tests](tests)

För att köra testen  
Installera pytest:
```
pip install pytest
```
Kör testen:
```
pytest
```

## Issues
Om du vill veta varför jag gjorde på ett visst sätt har jag dokumenterat hela processen i github issues.

## raw
Vissa saker i det här programmet är utanför specifikationerna som angavs i dokumentet vi fick.  
För en mer avskalad version så finns en branch [raw](https://github.com/EmptyDot/bank-app/tree/raw) som endast innehåller det viktigaste.

