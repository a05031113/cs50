import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    current_app, Markup
)
from markdown import markdown

from werkzeug.exceptions import abort

from miki.auth import login_required
from miki.db import connect


bp = Blueprint('edit', __name__)


@bp.app_template_filter('markdown')
def markdown_filter(content):
    return Markup(markdown(content))


@bp.route('/edit', methods=('GET', 'POST'))
@login_required
def edit():
    if request.method == 'POST':
        source = request.form.get('source', None)
        content = request.form.get('content', None)

        if not source or not content:
            abort(406)

        # Extract filename
        file_name = os.path.splitext(os.path.basename(source))[0]

        # Write content to markdown
        md = open(os.path.join(
            current_app.config.get('SOURCE'),
            file_name + '.md'),
            'w'
        )
        md.write(content)
        md.close()

        # Write content to html
        html = open(os.path.join(
            current_app.config.get('OUTPUT'),
            file_name + '.html'),
            'w'
        )
        html.write(render_template(
            'page.html',
            content=content,
            name=file_name)
        )
        html.close()

        # Redirect to generated html
        return redirect('/' + file_name + '.html')
    else:
        # Check for args in request
        if not request.args.get("file"):
            raise RuntimeError("No file parameter passed!")

        # Markdown file
        md = os.path.join(
            current_app.config.get('SOURCE'),
            request.args.get('file')
        )

        # Try opening markdown
        try:
            # Save contents
            md_file = open(md, 'r')
            content = md_file.read()
            md_file.close()
        # If file do not exist
        except FileNotFoundError:
            content = ''
            flash('Page do not exist yet.')

        return render_template(
            'edit.html',
            content=content,
            source=request.args.get("file")
        )
