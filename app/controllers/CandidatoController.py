from controllers.Controller import Controller
from models.Candidato import Candidato
from models.Curso import Curso
from models.Edicao import Edicao


class CandidatoController(Controller):
    def create(self, edicao_id=None):
        method = self.environ["REQUEST_METHOD"]
        template = self.env.get_template("create.html")
        candidato = Candidato()
        error_message = None

        if method == "POST":
            self.loadForm(candidato)
            if hasattr(candidato, 'edicao_curso_id') and candidato.edicao_curso_id:
                candidato.edicao_curso_id = candidato.edicao_curso_id
            try:
                if candidato.save():
                    self.redirectPage('view', {'id': candidato.id})
                    return
            except Exception as e:
                if 'unique constraint' in str(e).lower() or 'duplicate key' in str(e).lower():
                    error_message = "Já existe um candidato cadastrado com este CPF."
                else:
                    error_message = "Erro ao salvar candidato: " + str(e)

        edicao_cursos = []
        if edicao_id:
            from models.Edicao import EdicaoCurso
            edicao_cursos = EdicaoCurso.where('edicao_id', edicao_id).get()

        self.data = template.render(
            candidato=candidato, edicao_cursos=edicao_cursos, error_message=error_message
        )

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
        error_message = None

        if not candidato:
            self.notFound()
            return

        if method == "POST":
            # Remove cpf do fillable para impedir alteração
            if 'cpf' in candidato.__fillable__:
                candidato.__fillable__.remove('cpf')
            # Guarda o CPF original antes de carregar o form
            cpf_original = candidato.cpf

            # Carrega dados do formulário
            self.loadForm(candidato)

            # Impede alteração de CPF, mesmo após erro
            candidato.cpf = cpf_original

            try:
                if candidato.save():  # Orator vai fazer UPDATE
                    self.redirectPage('view', {'id': candidato.id})
                    return
            except Exception as e:
                # Garante que o CPF permaneça imutável após erro
                candidato.cpf = cpf_original
                error_message = "Erro ao salvar candidato: " + str(e)

        # Buscar cursos da edição do candidato
        edicao_cursos = []
        if candidato.edicao_curso_id:
            from models.Edicao import EdicaoCurso
            edicao_curso = EdicaoCurso.find(candidato.edicao_curso_id)
            if edicao_curso:
                edicao_cursos = EdicaoCurso.where(
                    'edicao_id', edicao_curso.edicao_id
                ).get()

        self.data = template.render(
            candidato=candidato, edicao_cursos=edicao_cursos, error_message=error_message
        )

    def delete(self, id):
        candidato = Candidato.find(id[0])
        if candidato:
            candidato.delete()
            self.session['flash'] = 'Candidato deletado com sucesso'
            self.redirectPage('index')
        else:
            self.notFound()

    def index(self, *args, **kwargs):
        edicoes = Edicao.all()
        message = ""
        if 'flash' in self.session:
            message = self.session['flash']
            self.session['flash'] = ""
        template = self.env.get_template("index.html")
        self.data = template.render(edicoes=edicoes, message=message)

    def edicao_detalhe(self, edicao_id=None):
        from models.Edicao import Edicao, EdicaoCurso
        from models.Candidato import Candidato
        edicao = Edicao.find(edicao_id)
        edicao_cursos = EdicaoCurso.where('edicao_id', edicao_id).get()
        candidatos = []
        for edicao_curso in edicao_cursos:
            for candidato in Candidato.where('edicao_curso_id', edicao_curso.id).get():
                curso = edicao_curso.curso
                candidatos.append({
                    'id': candidato.id,
                    'nome': candidato.nome,
                    'categoria': candidato.categoria,
                    'curso_nome': curso.nome if curso else 'N/A'
                })
        template = self.env.get_template("edicao_detalhe.html")
        self.data = template.render(edicao=edicao, candidatos=candidatos)
