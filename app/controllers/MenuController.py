from controllers.Controller import Controller
from jinja2 import Environment, FileSystemLoader


class MenuController(Controller):
    def index(self):
        template = self.env.get_template("menu.html")
        self.data = template.render()
