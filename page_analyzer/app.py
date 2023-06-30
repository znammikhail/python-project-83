from flask import (
    Flask,
    render_template,
    request,
    flash,
    get_flashed_messages,
    redirect,
    url_for)
from datetime import datetime
from dotenv import load_dotenv
import os
from page_analyzer.db import (
    get_urls,
    add_url_to_db,
    get_url_by_id,
    get_url_by_name,
    add_check_to_db,
    get_check
)
import requests
from page_analyzer.validate import validate_url, standardize_url, is_url_exists
from page_analyzer.pars import parse_html_content

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors.

    Return the 404.html template with a status code of 404.
    """
    return render_template('404.html'), 404


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
        url = get_url_by_id(id)
        messages = get_flashed_messages(with_categories=True)
        checks = get_check(id)
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
    url = get_url_by_id(id)['name']
    url_id = id
    try:
        response = requests.get(url)
        response.raise_for_status()

        html = response.content
        h1, title, description = parse_html_content(html)

    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'alert-danger')
        return redirect(url_for('url_detail', id=id))

    except (ValueError, TypeError):
        flash('Произошла ошибка при проверке', 'alert-danger')
        return redirect(url_for('url_detail', id=id))

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    add_check_to_db(url_id=url_id,
                    status_code=response.status_code,
                    h1=h1,
                    title=title,
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
    validation_result = validate_url(url)
    standardized_url = standardize_url(url)

    if validation_result['error'] is not None \
            and validation_result['error'] == 'URL is invalid':
        flash('Некорректный URL', 'alert-danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', url=url, messages=messages), 422

    elif validation_result['error'] is not None \
            and validation_result['error'] == 'URL is empty':
        flash('Некорректный URL', 'alert-danger')
        flash('URL обязателен', 'alert-danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', url=url, messages=messages), 422

    elif validation_result['error'] is not None \
            and validation_result['error'] == 'URL exceeds maximum length':
        flash('Некорректный URL', 'alert-danger')
        flash('URL превышает 255 символов', 'alert-danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', url=url, messages=messages), 422

    elif validation_result['error'] is None \
            and is_url_exists(standardized_url):
        flash('Страница уже существует', 'alert-info')
        id = get_url_by_name(standardized_url)['id']
        return redirect(url_for('url_detail', id=id))

    elif validation_result['error'] is None \
            and not is_url_exists(standardized_url):
        data = {
            'url': standardized_url,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        add_url_to_db(data['url'], data['created_at'])
        id = get_url_by_name(standardized_url)['id']
        flash('Страница успешно добавлена', 'alert-success')
        return redirect(url_for('url_detail', id=id))

    flash('Некорректный URL', 'alert-danger')
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', url=url, messages=messages), 500


if __name__ == '__main__':
    app.run()
