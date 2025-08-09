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
        # Monta estrutura mestre-detalhe: cada edição com seus cursos/vagas
        edicoes_detalhe = []
        for edicao in edicoes:
            edicao_cursos = EdicaoCurso.where('edicao_id', edicao.id).get()
            edicoes_detalhe.append({
                'edicao': edicao,
                'cursos': edicao_cursos
            })
        self.data = template.render(edicoes_detalhe=edicoes_detalhe)

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
            nome_sisu = form_data.get('nome_edicao')
            ano = form_data.get('ano_edicao')
            semestre = form_data.get('semestre_edicao')
            data_inicio = form_data.get('data_inicio_edicao')
            data_fim = form_data.get('data_fim_edicao')
            cursos_data = form_data.get('cursos', {})
            # Validação obrigatória
            if not nome_sisu or not ano or not semestre or not data_inicio or not data_fim:
                error_msg = 'Preencha todos os campos obrigatórios: nome, ano, semestre, data de início e fim.'
            elif not cursos_data or not all(
                    all(vaga in curso and curso.get(vaga) is not None and curso.get(vaga) != '' for vaga in [
                        'vagas_ac', 'vagas_ppi_br', 'vagas_publica_br', 'vagas_ppi_publica', 'vagas_publica', 'vagas_deficientes'])
                    for curso in cursos_data.values()):
                error_msg = 'Preencha todas as vagas para todos os cursos (coloque 0 se não houver vaga).'
            else:
                # Verifica se já existe edição com esse nome (exceto a edição atual)
                edicao_existente = Edicao.where('nome', nome_sisu)
                if id:
                    edicao_existente = edicao_existente.where('id', '!=', id)
                edicao_existente = edicao_existente.first()
                if edicao_existente:
                    error_msg = 'Já existe uma edição com esse nome (ano.semestre)!'
                else:
                    edicao.fill_from_form(form_data)
                    edicao.save()
                    # Remove vínculos antigos se estiver editando
                    if id:
                        EdicaoCurso.where('edicao_id', edicao.id).delete()
                    for curso in cursos_data.values():
                        edicao_curso = EdicaoCurso()
                        edicao_curso.fill_from_form({
                            'edicao_id': edicao.id,
                            'curso_id': curso.get('curso_id'),
                            'vagas_ac': curso.get('vagas_ac', 0),
                            'vagas_ppi_br': curso.get('vagas_ppi_br', 0),
                            'vagas_publica_br': curso.get('vagas_publica_br', 0),
                            'vagas_ppi_publica': curso.get('vagas_ppi_publica', 0),
                            'vagas_publica': curso.get('vagas_publica', 0),
                            'vagas_deficientes': curso.get('vagas_deficientes', 0)
                        })
                        edicao_curso.save()
                    self.redirectPage('view', {'id': edicao.id})

        self.data = template.render(
            edicao=edicao, error=error_msg, cursos=cursos, edicao_cursos=edicao_cursos)
