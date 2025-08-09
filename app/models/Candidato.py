from orator import Model


class Candidato(Model):
    __table__ = 'candidato'
    __timestamps__ = False
    __fillable__ = ['nome', 'cpf', 'data_nascimento',
                    'categoria', 'edicao_curso_id', 'nota']
