# bank-app

[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/EmptyDot/651703a1c1bca09b4e9b8f3e8a4d60e1/raw/coverage_endpoint.json)](https://github.com/EmptyDot/bank-app/actions/workflows/coverage.yml)

Hej Niklas! Välkommen till min bank app!

## Körning
Programmet är designat att köras från [main.ipynb](main.ipynb). Där kan du se en demonstration hur programmet fungerar.

Kräver python 3.9+

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
Navigera till roten av repon  
Du bör vara i samma directory som [main.ipynb](main.ipynb)  

Kör testen:
```
pytest
```

----------------
Tack för att du tar dig tiden att kolla :)  
Snälla säg till mig om det är något jag kan förbättra!
