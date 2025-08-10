from categorias import CATEGORIAS
import os
from controllers.Controller import Controller
from models.Edicao import Edicao, EdicaoCurso
from models.Curso import Curso
from jinja2 import Environment, FileSystemLoader
import cgi
import sys
from urllib.parse import parse_qs
sys.path.append('./app')


class EdicaoController(Controller):
    def delete(self, id=None):
        edicao = Edicao.where('id', id).first()
        if edicao:
            edicao.delete()
        self.redirectPage('index')

    def index(self, origem=None):
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
        self.data = template.render(
            edicoes_detalhe=edicoes_detalhe, origem=origem)

    def view(self, id=None, origem=None):
        template = self.env.get_template("view.html")
        edicao = Edicao.find(id)
        if not edicao:
            self.data = template.render(error="Edição não encontrada.", edicao=None, edicao_cursos=[
            ], origem=origem, candidatos=[])
            return
        edicao_cursos = EdicaoCurso.where('edicao_id', id).get()
        from models.Candidato import Candidato
        from models.Curso import Curso
        # Captura origem da query string se não vier por parâmetro
        from urllib.parse import parse_qs
        qs = parse_qs(self.environ.get('QUERY_STRING', ''))
        origem_qs = qs.get('origem', [None])[0]
        if origem_qs:
            origem = origem_qs
        if origem not in ('edicao', 'candidato'):
            origem = 'edicao'
        # Busca candidatos inscritos apenas nesta edição
        candidatos = []
        for edicao_curso in edicao_cursos:
            for candidato in Candidato.where('edicao_curso_id', edicao_curso.id).get():
                curso = edicao_curso.curso
                candidatos.append({
                    'nome': candidato.nome,
                    'categoria': candidato.categoria,
                    'curso_nome': curso.nome if curso else 'N/A'
                })
        self.data = template.render(
            edicao=edicao, edicao_cursos=edicao_cursos, origem=origem, candidatos=candidatos)

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
                        if str(curso.get('ativo', '0')) == '1':
                            edicao_curso = EdicaoCurso()
                            edicao_curso.fill_from_form({
                                'edicao_id': edicao.id,
                                'curso_id': curso.get('curso_id'),
                                CATEGORIAS[0]: int(curso.get('vagas_ac') or 0),
                                CATEGORIAS[1]: int(curso.get('vagas_ppi_br') or 0),
                                CATEGORIAS[2]: int(curso.get('vagas_publica_br') or 0),
                                CATEGORIAS[3]: int(curso.get('vagas_ppi_publica') or 0),
                                CATEGORIAS[4]: int(curso.get('vagas_publica') or 0),
                                CATEGORIAS[5]: int(
                                    curso.get('vagas_deficientes') or 0)
                            })
                            edicao_curso.save()
                    self.redirectPage(
                        'view', {'id': edicao.id, 'origem': 'edicao'})

        self.data = template.render(
            edicao=edicao, error=error_msg, cursos=cursos, edicao_cursos=edicao_cursos)
