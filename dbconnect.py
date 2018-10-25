# -*- coding: utf-8 -*-
"""
BarberShop - Conexão com o Banco de dados
Autor: Matheus Aryell Cavalcante Xavier

"""

import sqlite3
from prettytable import PrettyTable

"""
Pacote adicional:
    
conda install -c conda-forge prettytable 

"""


######################## DATABASE - USUÁRIOS ########################

titles_dados = ['id','login','senha','nome','idade','cpf','data de nascimento','perfil']
titles_servicos = ['id','serviço','preço','duração']
titles_agend = ['id','id cliente','id funcionário','id serviço','hora marcada','hora término','estado']
#conectando ao banco de dados
userdb = sqlite3.connect('dados.db')

#Definindo um cursor para o database
cursor = userdb.cursor()


def printartabela(result, titulos):
     table = PrettyTable()
     table.field_names = titulos
     for linha in result:
          table.add_row(linha)
     print(table)


def user_db():
    """
    Função que cria o banco de dados caso esse
    ainda não exista.  
    
    """
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS 
            dados(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL,
            senha TEXT NOT NULL,
            nome TEXT NOT NULL,
            idade INTEGER,
            cpf VARCHAR(11) NOT NULL,
            d_nascimento DATE NOT NULL,
            perfil TEXT NOT NULL
            ); """ )
    except:
        print('Nao foi possivel criar o banco de dados')
    else:
        print("Banco de dados criado com sucesso.")
        
def inserir_db(pessoa):
    
    try:    
        cursor.executemany("INSERT INTO dados (login,senha,nome,idade,cpf,d_nascimento,perfil) VALUES(?,?,?,?,?,?,?)", [pessoa])
        userdb.commit() #Realiza a inserção
        print("Dados inseridos com sucesso.")
    
    except:
        print("Não foi possível inserir os dados.")
    else:
        print("Inserção realizada com sucesso.")


def login():

    while True:
        usuario = raw_input("Login:")
        senha = raw_input("Senha:")
        cursor.execute("SELECT * FROM dados WHERE login = ? AND senha = ?", (usuario,senha)) 
        
        result = cursor.fetchall()
      
        if len(result) is not 0: #Encontrou o usuario
                print '\n' + "Seja bem vindo {}.".format(result[0][3])
                print("Seu perfil está em análise.")
                return (result[0][7],result[0][1]) #Retorna o perfil   
        else:
            print("Login ou Senha incorreto.")
            opcao = raw_input("Deseja tentar novamente ? (s/n) ")
            if opcao.lower() == 'n':
                return ('','')
            elif opcao.lower() == 's':
                continue
            else:
                print('Digite uma opcao válida.')
                continue

def personread_dados(filtro, info):
    cursor.execute("SELECT * FROM dados WHERE {} = ?".format(filtro), (info,))
    result = cursor.fetchall()
    
    printartabela(result, titles_dados)
    
def filtro(categoria):
    
    filtro = "SELECT * FROM dados ORDER BY " + categoria
    cursor.execute(filtro)
    
    print('\n')
    result = cursor.fetchall()
    
    printartabela(result,titles_dados)
    
        

def mudar_perfil(novo_perfil,id_number):
    cursor.execute("UPDATE dados SET perfil = ? WHERE id = ?", (novo_perfil, id_number))
    userdb.commit()

def id_user(perfil):
    #Qual o id do usuário ?
    
    cursor.execute("SELECT * FROM dados WHERE perfil = ? AND login = ?", (perfil[0],perfil[1]))
    result = cursor.fetchall()
    
    return result[0][0]

def validatelogin(login):
    cursor.execute("SELECT * FROM dados WHERE login = ?", (login,))
    result = cursor.fetchall()
    
    if len(result) is not 0:
        return False
    else:
        return True
          

    
######################## DATABASE - SERVIÇOS ########################

"""
Tarefas a fazer:
    - Mudar esse nome de cursor
    -
    -
"""

#conectando ao banco de dados
servicedb = sqlite3.connect('barber_servicos.db')

#Definindo um cursor para o database
cursor2 = servicedb.cursor()

def service_db():
    """
    Funcao que cria o banco de dados responsável
    por armazenar os serviços da barbearia e suas
    respectivas características
    """
    
    cursor2.execute("""CREATE TABLE IF NOT EXISTS barber_servicos(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            servico TEXT NOT NULL,
            preco DECIMAL(5,2),
            duracao INTEGER NOT NULL
            );""")
    
    print('Tabela de servicos criada com sucesso.')



def add_servico(newservice):    
    """
    Função que adiciona um novo
    serviço a barbearia
    
    """   
    cursor2.executemany("INSERT INTO barber_servicos (servico,duracao,preco) VALUES(?,?,?)", [newservice])
    servicedb.commit() #Realiza a inserção

def up_servico(alterar,campos,info,id_servico): #Alterar servico
    """
    Funcao que altera um servico
    -Altera por campo
    -Altera todos os campos
    
    """
    
    if alterar == 'campo':
        modify = "UPDATE barber_servicos SET " + campos + " = ? WHERE id = ?"
        cursor2.execute(modify,(info,id_servico))
        servicedb.commit()
    elif alterar == 'todos':
        cursor2.execute("UPDATE barber_servicos SET servico = ? WHERE id = ?", (info[0],id_servico))
        cursor2.execute("UPDATE barber_servicos SET duracao = ? WHERE id = ?", (info[1],id_servico))
        cursor2.execute("UPDATE barber_servicos SET preco = ? WHERE id = ?", (info[2],id_servico))
        servicedb.commit()
  
def nservico(id_number):
    """
    Funcao que retorna o nome do servico
    """
    cursor2.execute("SELECT * FROM barber_servicos WHERE id = ?", (id_number,))
    result = cursor2.fetchall()
    
    return str(result[0][1]) #para confirmar

def tservico(id_number):
    cursor2.execute("SELECT * FROM barber_servicos WHERE id = ?", (id_number,))
    result = cursor2.fetchall()
    
    return int(result[0][3])
    
    
def todos_servicos():
    """
    Funcao que retorna todos os servicos
    cadastrados no banco de dados e seu tamanho (uma tupla).
    """
    
    cursor2.execute("SELECT * FROM barber_servicos")
    result = cursor2.fetchall()

    return (result,len(result))
    
######################## DATABASE - AGENDAMENTO ########################            

"""
Tarefas a fazer:
    - Mudar esse nome de cursor
    - Mudar o datatype do hora_marcada
    - Definir como deve ser feita a inserção de dados no banco
"""
    
#conectando ao banco de dados   
appointdb = sqlite3.connect('agendamentos.db')

#Definindo um cursor para o database
cursor3 = appointdb.cursor()

def agendadb():
    """
    Função que cria o banco de dados
    responsável pelos agendamentos dos
    clientes da barbearia.
    """
    
    cursor3.execute("""CREATE TABLE IF NOT EXISTS agendamentos(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_funcionario INTEGER NOT NULL,
            id_servico INTEGER NOT NULL,
            hora_marcada TEXT NOT NULL,
            hora_termino TEXT NOT NULL,
            estado TEXT NOT NULL
            );""")
    
    
    print('Tabela de agendamentos criada com sucesso.')



def read_agend():
    cursor3.execute("SELECT * FROM agendamentos")
    result = cursor3.fetchall()
    
    printartabela(result,titles_agend)

def personread_agend(filtro, id_number):
    """
    Funcao que permite uma leitura personalizada do database
    agendamentos.
    """
    
    cursor3.execute("SELECT * FROM agendamentos WHERE {} = ?".format(filtro),   (id_number,))
    result = cursor3.fetchall()
    
    printartabela(result,titles_agend)

def add_agendamento(appoint):
    cursor3.executemany("INSERT INTO agendamentos (id_cliente,id_funcionario,id_servico,hora_marcada,hora_termino,estado) VALUES(?,?,?,?,?,?)", [appoint] )
    appointdb.commit()

def confirma_agend(funcid, novo_estado,id_number):
    cursor3.execute("UPDATE agendamentos SET estado = ? WHERE id = ?", (novo_estado, id_number))
    cursor3.execute("UPDATE agendamentos SET id_funcionario = ? WHERE id = ?", (funcid, id_number))
    appointdb.commit()



def printagend(id_user,option):
    cursor3.execute("SELECT * FROM agendamentos WHERE id_cliente = ?", (id_user,))
    result = cursor3.fetchall()    
                 
    if option == 'checar':
        checktitle = ['serviço','hora marcada','hora término','estado']
    
        sliceresult = []
        for i in range(len(result)):    
            servicename = nservico(result[i][3])
            sliceresult.append(tuple([servicename]) + result[i][4:7])

        printartabela(sliceresult,checktitle)
        
    elif option == 'deletar':
        deltitle = ['id','serviço','hora marcada','hora término','estado']
            
        sliceresult = []
        for i in range(len(result)):    
            servicename = nservico(result[i][3])
            sliceresult.append(tuple([str(result[i][0])]) + tuple([servicename]) + result[i][4:7])

        printartabela(sliceresult,deltitle)    
    
 
    
def checaragend(filtro, info):
    """
    funcao que retorna o tamanho de resultados
    com o determinado filtro utilizado.
    """
    
    if filtro == '':
        cursor3.execute("SELECT * FROM agendamentos")
        result = cursor3.fetchall()
        return len(result)
    else:     
        cursor3.execute("SELECT * FROM agendamentos WHERE {} = ?".format(filtro), (info,))
        result = cursor3.fetchall()
        return len(result)
    
def delagend(filtro, info):
    cursor3.execute("DELETE FROM agendamentos WHERE {} = ?".format(filtro), (info,))
    appointdb.commit()

######################## FUNÇÕES GERAIS ########################

def ler_db(flag):
    
    if flag == 'dados':
        cursor.execute("SELECT * FROM dados;")
        result = cursor.fetchall()
        printartabela(result, titles_dados)
    
    elif flag == 'servico':
        cursor2.execute("SELECT * FROM barber_servicos;")
        result = cursor2.fetchall()
        printartabela(result, titles_servicos)
    
    elif flag == 'agendamento':
        cursor3.execute("SELECT * FROM agendamentos;")
        result = cursor3.fetchall()
        printartabela(result, titles_agend)
        
def deletar(id_number, opcao): 
    
    if opcao == 'dados':
        cursor.execute("DELETE FROM dados WHERE id = ?", (id_number,)) # 'id_number, - tupla que contém id_number #VIAGEM
        userdb.commit()
    elif opcao == 'servico':
        cursor.execute("DELETE FROM barber_servicos WHERE id = ?", (id_number,))
        servicedb.commit()

def tamanho_db(flag):
    
    if flag == 'dados':
        cursor.execute("SELECT * FROM dados;")
        result = cursor.fetchall()
        return len(result)
    
    elif flag == 'servico':
        cursor2.execute("SELECT * FROM barber_servicos;")
        result = cursor2.fetchall()
        return len(result)
    
    elif flag == 'agendamento':
        cursor3.execute("SELECT * FROM agendamentos;")
        result = cursor3.fetchall()
        return len(result)
            
def close():
    userdb.close()
    servicedb.close()
    appointdb.close()
       

