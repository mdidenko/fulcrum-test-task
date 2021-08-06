from api.hash import get_short_link_hash
from api.validator import link_validator
from config import app, db, LINK_LIFETIME
from flask import request, render_template, redirect


@app.before_request
def link_checker():
    """Handler to check link lifetime."""
    if not request.path.startswith('/static/'):
        db.delete_outdated_links(LINK_LIFETIME)


@app.route('/', methods=['GET', 'POST'])
def shortener():
    """Handler to short link."""
    if request.method == "GET":
        return render_template('shortener.html')
    else:
        original_link = request.form['link'].strip()
        if not link_validator(original_link):
            return render_template('shortener.html', error="Enter correct URL!")

        short_link = get_short_link_hash(original_link)
        db.add_new_short_link(original_link, short_link)
        return render_template('shortener.html', short_link=short_link)


@app.route('/<string:shorted_link>', methods=['GET'])
def redirector(shorted_link):
    """Handler to find path for redirect."""
    original_link = db.get_original_link(shorted_link)
    if original_link:
        return redirect(original_link)
    else:
        return render_template(
            'error.html',
            error="REDIRECT ERROR",
            description="No such short link exists!"
        )
