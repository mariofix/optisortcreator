# SVS Agro
SVS Ops Management


## Babel Extract
```bash
poetry run pybabel extract -F babel/babel.cfg -o babel/messages.pot .
poetry run pybabel update -N -i babel/messages.pot -d svsagro/translations
``` 

## Babel Compile
```bash
poetry run pybabel compile -f -d svsagro/translations
``` 