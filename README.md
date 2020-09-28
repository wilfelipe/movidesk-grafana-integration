# Movidesk-Grafana API
APi de integração de tickets do Movidesk para o Grafana via "SimpleJSON".
## Instalação
- Instalação do plugin SimpleJSON no Grafana
```bash
sudo grafana-cli plugins install grafana-simple-json-datasource
sudo service grafana-server restart
```
- Configuração do Linux
```bash
$ sudo apt-get update
$ sudo apt-get install python3.6
$ sudo apt install python-pip
$ sudo pip3 install virtualenv
```
- Download dos repositorios
```bash
$ git clone https://github.com/wilfelipe/movidesk-grafana-integration.git
```
- Configuração do Ambiente Virtual
```bash
$ python3.6 -m venv my_env
$ source my_env/bin/activate
$ pip install -r requirements.txt
```
-Executando o codigo
````bash
$ python movidesk-grafana-integration/server.py
````
