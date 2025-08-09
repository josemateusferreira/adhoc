import os
from controllers.Controller import Controller
from models.Edicao import Edicao, EdicaoCurso
from models.Curso import Curso
from jinja2 import Environment, FileSystemLoader
import cgi
import sys
sys.path.append('./app')


class EdicaoController(Controller):
    def delete(self, id=None):
        edicao = Edicao.where('id', id).first()
        if edicao:
            edicao.delete()
        self.redirectPage('index')
    def index(self):
        template = self.env.get_template("index.html")
        edicoes = Edicao.all()
        self.data = template.render(edicoes=edicoes)
    def view(self, id=None):
        template = self.env.get_template("view.html")
        edicao = Edicao.find(id)
        import sys
        sys.stderr.write(f"[DEBUG] Dados da edição: {edicao}\n")
        edicao_cursos = EdicaoCurso.where('edicao_id', id).get()
        self.data = template.render(edicao=edicao, edicao_cursos=edicao_cursos)

    def create(self, id=None):
        method = self.environ["REQUEST_METHOD"]
        template = self.env.get_template("create.html")
        edicao = Edicao.where('id', id).first() if id else Edicao()
        error_msg = ""
        cursos = Curso.all()  # Busca todos os cursos do banco
        edicao_cursos = []
        if id:
            edicao_cursos = EdicaoCurso.where('edicao_id', id).get()
        if method == "POST":
            form = cgi.FieldStorage(
                fp=self.environ["wsgi.input"], environ=self.environ)
            form_data = self.form2dict(form)
            edicao.fill_from_form(form_data)
            edicao.save()
            self.redirectPage('view', {'id': edicao.id})

        self.data = template.render(
            edicao=edicao, error=error_msg, cursos=cursos, edicao_cursos=edicao_cursos)
