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
                'mensagem':'Pessoa {} não encontrada'.format(nome)
            }

        except Exception:
            response = {
                'status':'erro',
                'mensagem':'Erro desconhecido, procure o administrador da API'
            }

        return response

    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.get_json(self)

        try:
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

        except AttributeError:
            response = {
                'status':'erro',
                'mensagem':'Pessoa {} não encontrada'.format(nome)
            }

        except Exception:
            response = {
                'status':'erro',
                'mensagem':'Erro desconhecido, procure o administrador da API'
            }
        

        return response

    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()

        try:
            pessoa.delete()
            response = {'status':'sucesso', 'mensagem':'Pessoa {} excluido com sucesso!'.format(nome)}
        
        except AttributeError:
            response = {
                'status':'erro',
                'mensagem':'Pessoa {} não encontrada'.format(nome)
            }

        except Exception:
            response = {
                'status':'erro',
                'mensagem':'Erro desconhecido, procure o administrador da API'
            }

        return response


class ListaPessoas(Resource):
    def get(self):
        pessoas = Pessoas.query.all()

        response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in pessoas]

        return response

    def post(self):
        data = request.get_json(self)

        if 'nome' in data and 'idade' in data:
            pessoa = Pessoas(nome=data['nome'], idade=data['idade'])
            pessoa.save()

            response = {
                'id':pessoa.id,
                'nome':pessoa.nome,
                'idade':pessoa.idade
            }
        
        else:
            response = {'status':'erro', 'mensagem':'Não foi possivel inserir está pessoa por falta de dados.'}

        return response



class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        reponse = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome, 'status':i.status} for i in atividades]

        return reponse


    def post(self):
        dados = request.get_json(self)
        if 'pessoa' in dados and 'nome' in dados and 'status' in dados:
            pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()

            atividade = Atividades(nome=dados['nome'], pessoa=pessoa, status=dados['status'])
            atividade.save()

            response = {
                'status':atividade.status,
                'pessoa':atividade.pessoa.nome,
                'nome':atividade.nome,
                'id':atividade.id
            }

        else:
            response = {'status':'erro', 'mensagem':'Não foi possivel inserir está atividade por falta de dados.'}

        return response


class StatusAtividade(Resource):
    def put(self, id):
        dados = request.get_json(self)
        atividade = Atividades.query.filter_by(id=id).first()

        try:
            if 'status' in dados and (dados['status'] == 'pendente' or dados['status'] == 'concluido'):
                atividade.status = dados['status']
        
            atividade.save()

            response = {
                'id':atividade.id,
                'nome':atividade.nome,
                'pessoa':atividade.pessoa.nome,
                'status':atividade.status
            }

        except AttributeError:
            response = {
                'status':'erro',
                'mensagem':'Atividade de id {} não encontrada'.format(id)
            }

        except Exception:
            response = {
                'status':'erro',
                'mensagem':'Erro desconhecido, procure o administrador da API'
            }
        
        
        return response


    def get(self, id):
        atividade = Atividades.query.filter_by(id=id).first()

        try:
            response = {
                'id':atividade.id,
                'nome':atividade.nome,
                'pessoa':atividade.pessoa.nome,
                'status':atividade.status
            }

        except AttributeError:
            response = {
                'status':'erro',
                'mensagem':'Atividade de id {} não encontrada'.format(id)
            }
        
        return response



class AtividadesByName(Resource):
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        atividades = Atividades.query.filter_by(pessoa=pessoa)
        
        response = {}
        a_cont = 0

        for a in atividades:
            a_cont+=1
            response['Atividade '+str(a_cont)] = {
                'id_atividade':a.id,
                'atividade':a.nome,
                'status':a.status
            }
            print(a)

        return response




api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')
api.add_resource(StatusAtividade, '/atividades/<int:id>/')
api.add_resource(AtividadesByName, '/atividades/<string:nome>/')

if __name__ == "__main__":
    app.run(debug=True)