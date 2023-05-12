from flask import (
    Flask,
    render_template,
    request,
    flash,
    get_flashed_messages,
    redirect,
    url_for)
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import validators
from page_analyzer.db import (
    get_urls,
    add_url_db,
    get_url_id,
    get_url_name,
    add_check_db,
    get_check_db
)
import requests
from bs4 import BeautifulSoup

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors.

    Return the 404.html template with a status code of 404.
    """
    return render_template('404.html'), 404


def validate_url(url) -> dict:
    """Validate the entered URL address.

    Args:
        url (str): The URL address to validate.

    Returns:
        dict: A dictionary containing the validated URL and any errors found.

    """
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
    """Render the index.html template."""
    return render_template('index.html')


@app.route('/urls/<int:id>')
def url_detail(id):
    """
    Render URL detail page by ID.

    Retrieve URL and check data by ID from the database.
    If the ID is not found, return a 404 error page.

    Args:
        id (int): ID of the URL.

    Returns:
        rendered template with URL, check data, and messages.

    Raises:
        IndexError: if the ID is not found.
    """
    try:
        url = get_url_id(id)
        url_id = id
        messages = get_flashed_messages(with_categories=True)
        checks = get_check_db(url_id)
        return render_template('url_detail.html',
                               url=url, checks=checks,
                               messages=messages)
    except IndexError:
        return render_template('404.html'), 404


@app.post('/urls/<int:id>/checks')
def add_check(id):
    """
    Check the given URL and add the result to the database.

    Args:
        id (int): The ID of the URL to check.

    Returns:
        Response: A redirect to the URL detail page.

    Raises:
        Exception: If an error occurs during the check.

    """
    url = get_url_id(id)[1]
    url_id = id
    try:
        response = requests.get(url)
        status_code = response.status_code

        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        h1_tag = soup.find('h1')
        if h1_tag:
            h1 = h1_tag.text.strip()
        else:
            h1 = None

        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.text.strip()
        else:
            title = None

        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag and 'content' in meta_tag.attrs:
            description = meta_tag['content'].strip()
        else:
            description = None

    except Exception:
        flash('Произошла ошибка при проверке', 'alert-danger')
        return redirect(url_for('url_detail', id=id))

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    add_check_db(url_id=url_id,
                 status_code=status_code,
                 h1=h1, title=title,
                 description=description,
                 created_at=created_at)
    flash('Страница успешно проверена', 'alert-success')
    return redirect(url_for('url_detail', id=url_id))


@app.get('/urls')
def url_list():
    """
    Render the URL list page with a list of URLs retrieved from the database.

    Returns:
        A rendered template with the 'url_list.html' template.
    """
    urls = get_urls()
    messages = get_flashed_messages(with_categories=True)
    return render_template('url_list.html', urls=urls, messages=messages)


@app.post('/urls')
def add_url():
    """
    Add a new URL to the database.

    Returns:
        A redirect to the page for the new or existing URL, or the index page
        with an error message flashed.
    """
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
            return render_template('index.html', url=url, messages=messages)

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
