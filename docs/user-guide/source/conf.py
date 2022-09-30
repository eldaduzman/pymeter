import packaging.version
from pallets_sphinx_themes import get_version
from pallets_sphinx_themes import ProjectLink

# Project --------------------------------------------------------------

project = "pymeter"
copyright = "2010 Eldad Uzman"
author = "Eldad Uzman"
release, version = get_version("pymeter")

# General --------------------------------------------------------------

master_doc = "index"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.log_cabinet",
    "pallets_sphinx_themes",
    "sphinx_issues",
    "sphinx_tabs.tabs",
]
autodoc_typehints = "description"
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),

}
issues_github_path = "eldaduzman/pymeter"

# HTML -----------------------------------------------------------------

html_theme = "flask"
html_theme_options = {"index_sidebar_logo": False}
html_context = {
    "project_links": [
        ProjectLink("PyPI Releases", "https://pypi.org/project/pymeter/"),
        ProjectLink("Source Code", "https://github.com/eldaduzman/pymeter"),
        ProjectLink("Issue Tracker", "https://github.com/eldaduzman/pymeter/issues/"),

        # : ("https://abstracta.github.io/jmeter-java-dsl/", None),
        # pyjnius: ("https://github.com/kivy/pyjnius", None),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html", "ethicalads.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html", "ethicalads.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html", "ethicalads.html"]}
html_static_path = ["_static"]

html_favicon = "_static/pymeter-logo.png"
html_logo = "_static/pymeter-logo.png"
html_title = f"pymeter Documentation ({version})"

html_show_sourcelink = False

# LaTeX ----------------------------------------------------------------

latex_documents = [(master_doc, f"pymeter-{version}.tex", html_title, author, "manual")]

# Local Extensions -----------------------------------------------------


def github_link(name, rawtext, text, lineno, inliner, options=None, content=None):
    app = inliner.document.settings.env.app
    release = app.config.release
    base_url = "https://github.com/eldaduzman/pymeter/tree/"

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
