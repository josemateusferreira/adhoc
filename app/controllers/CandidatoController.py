
from controllers.Controller import Controller
from models.Candidato import Candidato
from models.Curso import Curso
from models.Edicao import Edicao


class CandidatoController(Controller):
    def create(self, edicao_id=None):
        method = self.environ["REQUEST_METHOD"]
        template = self.env.get_template("create.html")
        candidato = Candidato()
        if method == "POST":
            self.loadForm(candidato)
            if candidato.save():
                self.redirectPage('view', {'id': candidato.id})
        cursos = Curso.all()
        self.data = template.render(candidato=candidato, cursos=cursos)

    def view(self, id):
        candidato = Candidato.find(id[0])
        if candidato:
            template = self.env.get_template("view.html")
            self.data = template.render(candidato=candidato)
        else:
            self.notFound()

    def update(self, id):
        method = self.environ["REQUEST_METHOD"]
        template = self.env.get_template("create.html")
        candidato = Candidato.find(id[0])
        if candidato:
            if method == "POST":
                self.loadForm(candidato)
                if candidato.save():
                    self.redirectPage('view', {'id': candidato.id})
        else:
            self.notFound()
            return
        cursos = Curso.all()
        self.data = template.render(candidato=candidato, cursos=cursos)

    def delete(self, id):
        candidato = Candidato.find(id[0])
        if candidato:
            candidato.delete()
            self.session['flash'] = 'Candidato deletado com sucesso'
            self.redirectPage('index')
        else:
            self.notFound()

    def index(self):
        edicoes = Edicao.all()
        message = ""
        if 'flash' in self.session:
            message = self.session['flash']
            self.session['flash'] = ""
        template = self.env.get_template("index.html")
        self.data = template.render(edicoes=edicoes, message=message)
