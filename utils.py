from models import Pessoas, Usuarios

#Insere dados na tabela Pessoas
def insere_pessoas():
    pessoa = Pessoas(nome='Richard', idade=25)
    print(pessoa)
    pessoa.save()


#Realiza consulta na Tabela Pessoas
def consulta_pessoas():
    pessoas = Pessoas.query.all()
    pessoa = Pessoas.query.filter_by(nome='Rafael').first()
    print(pessoas)
    print(pessoa.idade)


#Altera dados na Tabela Pessoas
def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Rafael').first()
    pessoa.idade = 18
    pessoa.save()


#Exlui dados da tabela Pessoas
def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Richard').first()
    pessoa.delete()


def insere_usuario(login, senha):
    usuario = Usuarios(login=login, password=senha)
    usuario.save()


def consulta_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)


if __name__ == "__main__":
    #insere_pessoas()
    #altera_pessoa()
    #exclui_pessoa()
    #consulta_pessoas()
    #insere_usuario('richard', '123456')
    #insere_usuario('rafael', '654321')
    consulta_usuarios()