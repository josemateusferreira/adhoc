import os
from controllers.Controller import Controller
from models.Edicao import Edicao
from jinja2 import Environment, FileSystemLoader
import cgi
import sys
sys.path.append('./app')


class EdicaoController(Controller):

    def create(self):
        method = self.environ["REQUEST_METHOD"]
        template = self.env.get_template("create.html")
        edicao = Edicao()
        error_msg = ""
        if method == "POST":
            form = cgi.FieldStorage(
                fp=self.environ["wsgi.input"], environ=self.environ)
            edicao.fill_from_form(self.form2dict(form))
            if edicao.save():
                self.redirectPage('view', {'id': edicao.id})

        self.data = template.render(edicao=edicao, error=error_msg)

    def view(self, id):
        edicao = Edicao.find(id[0])
        if edicao:
            template = self.env.get_template("view.html")
            self.data = template.render(edicao=edicao, error="")
        else:
            self.notFound()
