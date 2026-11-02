import packaging.version
from pallets_sphinx_themes import get_version
from pallets_sphinx_themes import ProjectLink

# Project --------------------------------------------------------------

project = "Pboot"
copyright = "2010 Pallets, 2026 pboot-org"
author = "pboot-org"
release, version = get_version("pboot")

# General --------------------------------------------------------------

default_role = "code"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.log_cabinet",
    "sphinx_tabs.tabs",
    "pallets_sphinx_themes",
]
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_preserve_defaults = True
extlinks = {
    "issue": ("https://gitee.com/pboot-org/pboot/issues/%s", "#%s"),
    "pr": ("https://gitee.com/pboot-org/pboot/pulls/%s", "#%s"),
    "ghsa": ("https://gitee.com/pboot-org/pboot/security/advisories/GHSA-%s", "GHSA-%s"),
}
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "werkzeug": ("https://werkzeug.palletsprojects.com/", None),
    "click": ("https://click.palletsprojects.com/", None),
    "jinja": ("https://jinja.palletsprojects.com/", None),
    "itsdangerous": ("https://itsdangerous.palletsprojects.com/", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/", None),
    "wtforms": ("https://wtforms.readthedocs.io/", None),
    "blinker": ("https://blinker.readthedocs.io/", None),
}

# HTML -----------------------------------------------------------------

html_theme = "flask"
html_theme_options = {"index_sidebar_logo": False}
html_context = {
    "project_links": [
        ProjectLink("Donate", "https://gitee.com/pboot-org/pboot"),
        ProjectLink("PyPI Releases", "https://pypi.org/project/pboot/"),
        ProjectLink("Source Code", "https://gitee.com/pboot-org/pboot/"),
        ProjectLink("Issue Tracker", "https://gitee.com/pboot-org/pboot/issues/"),
        ProjectLink("Chat", "https://gitee.com/pboot-org/pboot/issues"),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html", "ethicalads.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html", "ethicalads.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html", "ethicalads.html"]}
html_static_path = ["_static"]
html_favicon = "_static/pboot-icon.svg"
html_logo = "_static/pboot-logo.svg"
html_title = f"Pboot Documentation ({version})"
html_show_sourcelink = False

gettext_uuid = True
gettext_compact = False

# Local Extensions -----------------------------------------------------


def github_link(name, rawtext, text, lineno, inliner, options=None, content=None):
    app = inliner.document.settings.env.app
    release = app.config.release
    base_url = "https://gitee.com/pboot-org/pboot/tree/"

    if text.endswith(">"):
        words, text = text[:-1].rsplit("<", 1)
        words = words.strip()
    else:
        words = None

    if packaging.version.parse(release).is_devrelease:
        url = f"{base_url}main/{text}"
    else:
        url = f"{base_url}{release}/{text}"

    if words is None:
        words = url

    from docutils.nodes import reference
    from docutils.parsers.rst.roles import set_classes

    options = options or {}
    set_classes(options)
    node = reference(rawtext, words, refuri=url, **options)
    return [node], []


def setup(app):
    app.add_role("gh", github_link)
