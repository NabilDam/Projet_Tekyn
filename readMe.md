# First time :
Do not forget to install packages via pipenv install
```shell script 
$ pipenv install
```
# Args : -v / --verbose
When this argument is used, the program will print information
about the collection and the polygones.
#### Exemple of use :
```shell script 
$ pipenv run python3.8 main.py -v
```
or 
```shell script 
$ pipenv run python3.8 main.py --verbose
```
## Warning !
    1. This arg doesn't work with pytest.
    2. Before using pytest, you have to comment the line using the arg.
    3. This line is in the file Polygones_package/logging_type.py
    4. The line to comment is "logging = create_logging()"

#### Exemple to launch the script without verbose :
```shell script 
$ pipenv run python3.8 main.py
```
or 
```shell script 
$ pipenv shell
$ python main.py
```