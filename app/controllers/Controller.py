from jinja2 import Environment, FileSystemLoader
import os
import cgi
from html import escape
from urllib.parse import urlencode

class Controller:
    def __init__(self, env):
        self.environ = env
        self.data = ""
        self.status = "200 OK"
        self.redirect_url = ""
        self.session = env['session']
        self.nome = (self.__class__.__name__).lower()[:-len("controller")]
        self.env = Environment(loader=FileSystemLoader(os.getcwd() + f'/views/{self.nome}'))

    def form2dict(self, form):
        """
        Converte campos de formulário (simples e aninhados) em um dicionário estruturado.
        Exemplo:
        - Campos simples: {'nome': 'valor'}
        - Campos aninhados: {'cursos': {0: {'vagas_ac': '10'}, 1: {'vagas_ac': '20'}}}
        """
        data = {}
        for key in form:
            value = escape(form.getvalue(key))
            if '[' in key and ']' in key:  # Campo aninhado (ex: cursos[0][vagas_ac])
                parts = key.replace(']', '').split('[')
                parent = parts[0]  # 'cursos'
                index = int(parts[1])  # 0
                child_key = parts[2]  # 'vagas_ac'
                
                if parent not in data:
                    data[parent] = {}
                if index not in data[parent]:
                    data[parent][index] = {}
                data[parent][index][child_key] = value
            else:
                data[key] = value  # Campo simples
        return data

    def loadForm(self, model):
        """
        Carrega dados de formulário (simples) no modelo.
        """
        form = cgi.FieldStorage(fp=self.environ["wsgi.input"], environ=self.environ)
        model.fill(self.form2dict(form))

    def loadNestedForm(self, model, parent_field):
        """
        Carrega dados de formulário aninhado (mestre-detalhe) e retorna os dados detalhados.
        Exemplo de uso:
        - nested_data = self.loadNestedForm(edicao_model, 'cursos')
        """
        form = cgi.FieldStorage(fp=self.environ["wsgi.input"], environ=self.environ)
        form_data = self.form2dict(form)
        
        # Preenche o modelo mestre com campos simples
        model.fill({k: v for k, v in form_data.items() if '[' not in k})
        
        # Extrai dados aninhados (ex: cursos[0][vagas_ac])
        nested_data = {}
        for key in form_data:
            if '[' in key and key.startswith(parent_field):
                parts = key.replace(']', '').split('[')
                index = int(parts[1])
                child_key = parts[2]
                
                if index not in nested_data:
                    nested_data[index] = {}
                nested_data[index][child_key] = form_data[key]
        
        return nested_data

    def redirectPage(self, path: str, params=None):
        """
        Redireciona para uma URL específica com parâmetros opcionais.
        """
        self.status = "302 OK"
        self.redirect_url = f'/app/{self.nome}/{path}'
        if params:
            self.redirect_url += f'?{urlencode(params)}'

    def notFound(self):
        """
        Retorna uma página 404 personalizada.
        """
        self.status = "404 Not Found"
        template = self.env.get_template("404.html")
        self.data = template.render()