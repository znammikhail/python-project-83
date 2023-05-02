from flask import Flask, render_template, request, flash, get_flashed_messages, redirect, url_for
# import psycopg2
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import validators
from page_analyzer.db import get_urls, add_url_db, get_url_id, get_url_name, add_check_db, get_check_db


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


def validate_url(url):
    """Функция для валидации введенного URL адреса."""
    mistake = None

    if len(url) == 0:
        mistake = 'empty'
    elif len(url) > 255:
        mistake = 'long length'
    elif not validators.url(url):
        mistake = 'invalid'
    else:
        url = urlparse(url)
        url = f'{url.scheme}://{url.netloc}'
        found = get_url_name(url)
        if found:
            mistake = 'exists'
    answer = {'url': url, 'error': mistake}
    return answer


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/urls/<int:id>')
def url_detail(id):
    try:
        url = get_url_id(id)
        url_id = id
        messages = get_flashed_messages(with_categories=True)
        checks = get_check_db(url_id)
        return render_template('url_detail.html', url=url, checks=checks, messages=messages)
    except IndexError:
        return render_template('404.html'), 404


@app.post('/urls/<id>/checks')
def add_check(id):
    url = get_url_id(id)
    url_id = url[0]
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    add_check_db(url_id, created_at)
    flash('Страница успешно проверена', 'alert-success')
    return redirect(url_for('url_detail', id=url_id))


@app.get('/urls')
def url_list():
    urls = get_urls()
    messages = get_flashed_messages(with_categories=True)
    return render_template('url_list.html', urls=urls, messages=messages)


@app.post('/urls')
def add_url():
    url = request.form.get('url')
    answer_valid = validate_url(url)
    url, error = answer_valid['url'], answer_valid['error']

    if error:
        if error == 'exists':
            id = get_url_name(url)[0]
            flash('Страница уже существует', 'alert-info')
            return redirect(url_for('url_detail', id=id))
        else:
            flash('Некорректный URL', 'alert-danger')
            if error == 'empty':
                flash('URL обязателен', 'alert-danger')
            elif error == 'long length':
                flash('URL превышает 255 символов', 'alert-danger')
            messages = get_flashed_messages(with_categories=True)
            return render_template('index.html', url=url, messages=messages), 422

    else:
        data = {
            'url': url,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        add_url_db(data['url'], data['created_at'])
        id = get_url_name(url)[0]
        flash('Страница успешно добавлена', 'alert-success')
        return redirect(url_for('url_detail', id=id))


if __name__ == '__main__':
    app.run()
