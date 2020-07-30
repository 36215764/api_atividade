from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades


app = Flask(__name__)
api = Api(app)

class Pessoa(Resource):
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()

        try:
            response = {
                'id':pessoa.id,
                'nome':pessoa.nome,
                'idade':pessoa.idade            
            }
        except AttributeError:
            response = {
                'status':'erro',
                'mensagem':'Pessoa "{}" não encontrada'.format(nome)
            }

        return response

    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.get_json(self)

        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        
        pessoa.save()

        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        

        return response

    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        pessoa.delete()
        response = {'status':'sucesso', 'mensagem':'Pessoa {} excluido com sucesso!'.format(nome)}

        return response


class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()

        response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in pessoas]

        return response

    def post(self):
        data = request.get_json(self)
        pessoa = Pessoas(nome=data['nome'], idade=data['idade'])
        pessoa.save()

        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }

        return response



class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        reponse = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome} for i in atividades]

        return reponse


    def post(self):
        dados = request.get_json(self)
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()

        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()

        response = {
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome,
            'id':atividade.id
        }

        return response





api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')

if __name__ == "__main__":
    app.run(debug=True)