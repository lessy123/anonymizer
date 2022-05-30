# anonymizer

Анонимайзер расчитан на русский текст и меняет имена, фамилии, адреса, написанные на русском языке.Помимо этого программа анонимизирует даты, номера телефонов, инн и номера карт. Также программа блюрит изображения.

Программа расчитана для работы Firebird и производной от нее RedDataBase.

Программа написана на языке Python(V:3.8.10). Список необходимых к установке библиотек:
 - natasha==1.4.0
 - fdb==2.0.2
 - random
 - datetime
 - faker==0.7.7
 - re
 - numpy==1.22.3
 - opencv-python==4.5.5.64

Запуск программы производится через файл index.py. 
Запуск программы из командной строки:

  python3 index.py
  
Программа потребует ввести путь до базы данных, которую планируется анонимизировать. Путь должен быть построен к копии данных, иначе рискуете потерять данные. После подключения к базе данных будет предоставлен выбр: анонимизировать всю базу данных или только отдельные таблицы. При выборе анонимизации отдельных таблиц алгоритм потребудет ввести количество таблиц, подлежащих изменению, после чего необходимо будет ввести названия этих таблиц. 

После выбора объекта анонимизации программа анонимизирует все поля таблицы, которые программа посчитает личными данными. 
