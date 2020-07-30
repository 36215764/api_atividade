from models import Pessoas

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





if __name__ == "__main__":
    #insere_pessoas()
    #altera_pessoa()
    exclui_pessoa()
    consulta_pessoas()