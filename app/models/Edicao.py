from orator import Model


class Edicao(Model):
    __table__ = 'edicoes'
    # Desativar timestamps para evitar erro de campos inexistentes no banco
    __timestamps__ = False
    __fillable__ = ['nome', 'ano', 'semestre', 'data_inicio',
                    'data_fim']  # Campos que podem ser preenchidos em massa

    def fill_from_form(self, data):
        self.nome = data.get('nome')
        self.ano = data.get('ano')
        self.semestre = data.get('semestre')
        self.data_inicio = data.get('data_inicio')
        self.data_fim = data.get('data_fim')
        # Não preenche cursos aqui, pois são dados aninhados


class EdicaoCurso(Model):
    __table__ = 'edicao_curso'
    # Campos gerenciados pelo Orator

    def fill_from_form(self, data):
        self.edicao_id = data.get('edicao_id')
        self.curso_id = data.get('curso_id')
        self.vagas_ac = data.get('vagas_ac', 0)
        self.vagas_ppi_br = data.get('vagas_ppi_br', 0)
        self.vagas_publica_br = data.get('vagas_publica_br', 0)
        self.vagas_ppi_publica = data.get('vagas_ppi_publica', 0)
        self.vagas_publica = data.get('vagas_publica', 0)
        self.vagas_deficientes = data.get('vagas_deficientes', 0)
