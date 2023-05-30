### Hexlet tests and linter status:
[![Actions Status](https://github.com/znammikhail/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/znammikhail/python-project-83/actions)


[![Maintainability](https://api.codeclimate.com/v1/badges/ecc28a08c8e26b4ab278/maintainability)](https://codeclimate.com/github/znammikhail/python-project-83/maintainability)

<a href="https://python-project-83-production-8ea0.up.railway.app/">Посмотреть сайт</a>

<p>
<a href="#about">О проекте</a> •
<a href="#installation">Установка</a> •
<a href="#usage">Использование</a> •
</p>


<h2 id="about">О проекте</h2>

<p>Page Analyzer - это приложение, основанное на фреймворке Flask, которое анализирует указанные страницы на пригодность для SEO. В проекте используются основные принципы построения современных веб-сайтов на архитектуре MVC. Для построения фронтенда используется фреймворк Bootstrap 5 и шаблонизатор Jinja2. В качестве базы данных используется PostgreSQL.</p>

<h2 id="installation">Установка</h2>

<ol>
  <li>Убедитесь, что у вас установлена версия Python 3.8 или выше.</li>
  <li>Установите менеджер зависимостей Poetry, следуя официальной инструкции.</li>
  <li>Установите PostgreSQL, выбрав подходящую версию с официального веб-сайта.</li>
  <li>Склонируйте репозиторий приложения на ваш компьютер с помощью команды <code>git clone</code>.</li>
  <li>В командной строке перейдите в папку с проектом (<code>python-project-83</code>).</li>
  <li>Установите все необходимые зависимости, выполнив команду <code>make install</code>.</li>
  <li>Создайте файл <code>.env</code> в корневой папке проекта и добавьте в него следующие переменные:<br>
  ```bash
    DATABASE_URL = postgresql://{provider}://{user}:{password}@{host}:{port}/{db}
    SECRET_KEY = '{your secret key}
  ```
  </li>
  <li>Запустите команды из файла <code>database.sql</code>, чтобы создать необходимые таблицы.</li>
</ol>

<h2 id="usage">Использование</h2>

<ol>
  <li>Запустите сервер Flask с помощью команды <code>make start</code>.</li>
  <li>По умолчанию сервер будет доступен по адресу <a href="http://0.0.0.0:8000">http://0.0.0.0:8000</a>.</li>
  <li>Чтобы добавить новый сайт для анализа, введите его адрес в форму на главной странице. Введенный адрес будет проверен и добавлен в базу данных.</li>
  <li>После добавления сайта вы можете проверить его. На странице конкретного сайта появится кнопка, и при нажатии на нее будет создана запись в таблице проверок.</li>
  <li>Все добавленные URL-адреса можно просмотреть на странице <a href="/urls">/urls</a>.</li>
</ol>