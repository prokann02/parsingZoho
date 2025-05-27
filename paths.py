import pathlib

ROOT_PATH = pathlib.Path(__file__).parent.absolute()

STATIC = ROOT_PATH.joinpath("static")

TEMPLATES = ROOT_PATH.joinpath("templates")
TEMPLATES_FORM_HTML_ABSOLUTE = TEMPLATES.joinpath("form.html")
TEMPLATES_RESULT_HTML_ABSOLUTE = TEMPLATES.joinpath("result.html")
TEMPLATES_SELECT_LINKS_HTML_ABSOLUTE = TEMPLATES.joinpath("select_links.html")

TEMPLATES_FORM_HTML = "form.html"
TEMPLATES_RESULT_HTML = "result.html"
TEMPLATES_SELECT_LINKS_HTML = "select_links.html"
