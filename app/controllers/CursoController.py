from controllers.Controller import Controller
from models.Curso import Curso
from jinja2 import Environment, FileSystemLoader


class CursoController(Controller):
    def delete(self, id=None, *args, **kwargs):
        # Garante que o id seja tratado corretamente
        if isinstance(id, list):
            id = id[0]
        curso = Curso.find(id)
        if curso:
            curso.delete()
        self.redirectPage('index')

    def index(self, *args, **kwargs):
        template = self.env.get_template("index.html")
        cursos = Curso.all()
        self.data = template.render(cursos=cursos)

    def create(self, *args, **kwargs):
        method = self.environ["REQUEST_METHOD"]
        template = self.env.get_template("create.html")
        curso = Curso()
        if method == "POST":
            self.loadForm(curso)
            if curso.save():
                self.redirectPage('index')
                return
        self.data = template.render(curso=curso)

    def edit(self, id=None, *args, **kwargs):
        # Garante que o id seja tratado corretamente
        if isinstance(id, list):
            id = id[0]
        curso = Curso.find(id)
        if not curso:
            self.data = "Curso não encontrado"
            return
        method = self.environ["REQUEST_METHOD"]
        if method == "POST":
            self.loadForm(curso)
            curso.save()
            cursos = Curso.all()
            template = self.env.get_template("index.html")
            self.data = template.render(cursos=cursos)
            return
        template = self.env.get_template("edit.html")
        self.data = template.render(curso=curso)
