# zbx_rac
Проект направлен на создание простого инструмента, для мониторинга состояния и производительности серверов **1С:Предприятие**. 

### Основные идеи:
- Время выполнения любого запроса меньше 4 секунд, стандартного timeout в zabbix.
- Выполнение и обработка запросов на стороне Zabbix сервера или Zabbix proxy.
- Полнота собираемых метрик.

### Основные возможности:
- Автоматическое обнаружение процессов, LLD Zabbix
- Автоматическое обнаружение информационных баз 1С, LLD Zabbix
- Синхронные данные по сессиям и процессам
- Учет блокировок и лицензий
- Инвентарные данные по каждой информационной базе.*

### Состав:
- zbx_rac.py - исполняемый скрипт
- lib_rac.py - библиотека с реализацией оберток для утелиты rac.exe
- rac_templates.xml - шаблон для zabbix
- add_service.bat - рагистрация службы 1С:RAS
- doc - описание возвращаемых данных rac.exe 

### Требования и зависимости:
- Zabbix Server(Proxy) 4.0 и выше
- Python v3.6 и выше
- Утилита RAC (идет в составе сервера 1С:Предприятие)

### Установка и настройка:

1. Установка службы 1С RAS Windows.
>Для установки ras.exe как службы, воспользуйтесь консольной утилитой sc или add_service.bat<br>
>При использовании bat указажите свой путь к ras.exe.<br>
>ras.exe входит в стандартый набор утилит поставляемых с сервером 1С:Предприятие.

2. Подготовка zabbix servera(proxy)
> - Установите технологическую платформу 1C; на сайте <https://releases.1c.ru> доступны 2 варианта deb  и rpm.
> - Скопируйте zbx_rac.py и lib_rac.py в externalscript, добавьте разрешение  на исполнение для файла zbx_rac.py.
```
	Путь до externalscripts определяется в zabbix_*.conf
	grep "externalscripts" /etc/zabbix/zabbix_*.conf
	ExternalScripts=${datadir}/externalscripts
	ExternalScripts=/var/lib/zabbix/externalscripts
```

3. Импорт шаблона Zabbix </summary>
> <https://www.zabbix.com/documentation/4.0/ru/manual/xml_export_import/templates>


### Список источников и литературы:
- <https://its.1c.ru/db/bsp23doc#content:883:hdoc)>
- <https://www.zabbix.com/documentation/current/>
- <https://infostart.ru/1c/articles/1285308/>
- `«Настольная книга 1С:Эксперта по технологическим вопросам»`