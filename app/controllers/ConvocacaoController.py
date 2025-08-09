from controllers.Controller import Controller
from models.Candidato import Candidato
from models.Curso import Curso
from jinja2 import Environment, FileSystemLoader
from urllib.parse import parse_qs


class ConvocacaoController(Controller):
    def index(self, edicao_id=None, origem=None):
        template = self.env.get_template("index.html")
        # Captura origem da query string se não vier por parâmetro
        qs = parse_qs(self.environ.get('QUERY_STRING', ''))
        if origem is None:
            origem = qs.get('origem', ['edicao'])[0]
        if origem not in ('edicao', 'candidato'):
            origem = 'edicao'
        # Busca candidatos da edição
        candidatos = []
        if edicao_id:
            # Busca todos os candidatos inscritos na edição
            for candidato in Candidato.where('edicao_id', edicao_id).get():
                curso = Curso.find(candidato.curso_id)
                candidatos.append({
                    'nome': candidato.nome,
                    'categoria': candidato.categoria,
                    'curso_nome': curso.nome if curso else 'N/A'
                })
        self.data = template.render(
            candidatos=candidatos, origem=origem, edicao_id=edicao_id)
