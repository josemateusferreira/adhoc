from categorias import CATEGORIAS
import os
from controllers.Controller import Controller
from models.Candidato import Candidato
from models.Edicao import Edicao, EdicaoCurso
from jinja2 import Environment, FileSystemLoader
from urllib.parse import parse_qs
import sys
sys.path.append('./app')


class ConvocacaoController(Controller):
    def lista(self, *args, **kwargs):
        qs = parse_qs(self.environ.get('QUERY_STRING', ''))
        edicao_id = int(qs.get('edicao_id', [0])[
                        0]) if 'edicao_id' in qs else None
        edicoes = Edicao.all()
        edicao_cursos = EdicaoCurso.where(
            'edicao_id', edicao_id).get() if edicao_id else []
        template = self.env.get_template("lista.html")
        self.data = template.render(
            edicoes=edicoes,
            edicao_cursos=edicao_cursos,
            edicao_id=edicao_id)

    def resultado(self, *args, **kwargs):
        qs = parse_qs(self.environ.get('QUERY_STRING', ''))
        edicao_id = int(qs.get('edicao_id', [0])[
                        0]) if 'edicao_id' in qs else None
        edicao_curso_id = int(qs.get('edicao_curso_id', [0])[
                              0]) if 'edicao_curso_id' in qs else None
        multiplicador = int(qs.get('multiplicador', [1])[
                            0]) if 'multiplicador' in qs else 1
        edicoes = Edicao.all()
        edicao_cursos = EdicaoCurso.where(
            'edicao_id', edicao_id).get() if edicao_id else []
        lista_convocacao = {}
        curso_nome = None
        edicao_nome = None
        if edicao_curso_id:
            ec = EdicaoCurso.find(edicao_curso_id)
            if ec:
                curso_nome = ec.curso.nome if ec.curso else None
                edicao = Edicao.find(ec.edicao_id)
                edicao_nome = f"{edicao.nome} ({edicao.ano}.{edicao.semestre})" if edicao else None
                modalidades = {
                    CATEGORIAS[0]: ec.vagas_ac,
                    CATEGORIAS[1]: ec.vagas_ppi_br,
                    CATEGORIAS[2]: ec.vagas_publica_br,
                    CATEGORIAS[3]: ec.vagas_ppi_publica,
                    CATEGORIAS[4]: ec.vagas_publica,
                    CATEGORIAS[5]: ec.vagas_deficientes
                }
                for modalidade, vagas in modalidades.items():
                    n_convocar = vagas * multiplicador
                    candidatos = (Candidato.where('edicao_curso_id', edicao_curso_id)
                                  .where('categoria', modalidade)
                                  .order_by('nota', 'desc')
                                  .limit(n_convocar)
                                  .get())
                    for idx, candidato in enumerate(candidatos, start=1):
                        candidato.posicao_modalidade = idx
                    lista_convocacao[modalidade] = candidatos
        template = self.env.get_template("resultado.html")
        self.data = template.render(
            edicoes=edicoes,
            edicao_cursos=edicao_cursos,
            edicao_id=edicao_id,
            edicao_curso_id=edicao_curso_id,
            lista_convocacao=lista_convocacao,
            curso_nome=curso_nome,
            edicao_nome=edicao_nome)
