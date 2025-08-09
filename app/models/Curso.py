from orator import Model


class Curso(Model):
    __table__ = 'curso'
    __timestamps__ = False
    __fillable__ = ['nome']
