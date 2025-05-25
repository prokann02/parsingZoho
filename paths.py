import pathlib

ROOT_PATH = pathlib.Path(__file__).parent.absolute()

TEMPLATES = ROOT_PATH.joinpath("templates")
TEMPLATES_FORM_HTML = TEMPLATES.joinpath("form.html")
TEMPLATES_RESULT_HTML = TEMPLATES.joinpath("result.html")
TEMPLATES_SELECT_LINKS_HTML = TEMPLATES.joinpath("select_links.html")
