# testLinkHelper
Импорт из excel в testlink с помощью API

## Среда разработки
* Python 3.6+
* PyQt5
* testlink1.9.16+

## Зависимости пакетов для запуска программы
* xlrd
* xlwt
* TestLink-API-Python-client
* PyQt5

pip install -r requirements.txt

## Конфигурация подключения к серверу
config.ini можно создать через gui

Или записать в config.ini
```
[server]
server_url = localhost
devkey = apikey
proxy = 
login_name = username
```


## Запуск
python testLinkHelper.py

