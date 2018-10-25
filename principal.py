# -*- coding: utf-8 -*-
"""
BarberShop - Principal
Autor: Matheus Aryell Cavalcante Xavier

"""

from datetime import date
import dbconnect as db
import datetime
import calendar
import time
import bsdate as bs
import os

######################## FUNCÕES ########################

 
#Converte string p/ datetime object
convertdata = lambda s: datetime.datetime.strptime(s, '%d/%m/%Y') 
converthora = lambda s: datetime.datetime.strptime(s, '%H:%M')                           
    
def menu_inicial(perfil):
    if perfil == ('',''):
        print '\x1b[2J\x1b[1;1H' #Código de escape
        data = date.today()
        data = data.strftime('%d/%m/%Y')
        print("*"*40)
        print("BarberShop                    {}".format(data))
        print("*"*40)
    else:
        print '\x1b[2J\x1b[1;1H' #Código de escape
        data = date.today()
        data = data.strftime('%d/%m/%Y')
        print("*"*40)
        print("BarberShop                    {}".format(data))
        print("{}: {}".format(perfil[0],perfil[1]))
        print("*"*40)

def menu():
    perfil = ('','')
    menu_inicial(perfil)
    print('1 - Login')
    print('2 - Realizar Cadastro')
    print('3 - Sair') 


def esperaenter():
    try:
        raw_input("Pressione enter para continuar")
    except SyntaxError:
        pass
        
def opt(lista):  
    for i in range(1, len(lista)+ 1):
        print("{} - {}".format(i,lista[i-1]))
    
  
    print('{} - Voltar'.format(len(lista) + 1))
    #print('{} - Sair'.format(len(lista) + 1))
    
    while True:
        try:
            opcao = int(raw_input())
        except ValueError:
            print('Digite um número no intervalo mostrado.')
            continue
        else:
            break
            
    
    while opcao not in range(1, len(lista)+2): # +1 do voltar
        print 'Selecione uma opção válida.'
        opcao = int(raw_input())
    else:
        return opcao

def cad_servico():
    """
    Funcao que realiza o cadastro de um novo
    servico
    """
    n_servico = raw_input("Digite o nome do servico: ")
    
    while True:
        try:
            duracao = int(raw_input("Digite o tempo medio de duracao do servico (em minutos): "))
        except ValueError:
            print('Digite um número.')
            continue
        else:
            break
    while True:
        try:
            preco = float(raw_input("Digite o preco do servico: "))
        except ValueError:
            print('Digite um número acrescido de sua casa decimal.')
            continue
        else:
            break
        
    newservice = [n_servico,duracao,preco]
    
    return newservice

def cad_user():    
    """
    Função que solicita ao usuário seus dados
    e os armazena em uma lista.
    
    """
    while True:
        login = raw_input("Login: ")
        boolean = db.validatelogin(login)
        
        if boolean == False:
            print('Login em uso. Tente novamente.')
            continue
        else:
            break
    
    while True:
        senha = raw_input("Senha: ")
        r_senha = raw_input("Confirmar senha: ")
        
        if senha == r_senha:
            break
        else:
            print('Senhas diferentes. Por favor, digite novamente.')
            continue
            
    nome = raw_input("Nome: ")
    idade = int(raw_input("Idade: "))
    cpf = raw_input("Cpf: ")
    
    d_nasc = raw_input("Data de Nascimento (dia/mes/ano): ")
    dia,mes,ano = map(int,d_nasc.split('/'))
    date_nasc = datetime.date(ano,mes,dia)   
    
    perfil = 'Perfil Pendente'
    pessoa = [login, senha, nome, idade, cpf, date_nasc, perfil]
    
    return pessoa

def calendario():

    print ('\n' + '-----Calendário-----' + '\n')

    date = datetime.date.today()

    print (calendar.month(date.year, date.month))
              
         
def cad_agendamento(id_cliente):
            
    calendario()
    
    #Range de 1 semana
    #Loja funciona das 8:00 às 19:00
    
    while True:
        while True:
            data = raw_input('Data (DD/MM/YYYY): ')
            if len (data) != 10:
                print('Digite uma data no formato informado.')
                continue
            else:
                break
            
        data_marcada = convertdata(data)    
        
        if datetime.datetime(2018,10,23) <= data_marcada <= datetime.datetime(2018,10,30):
            break
        else:
            print('Digite uma data referente a essa semana.')
            time.sleep(1)
            continue        
    
    while True:      
        while True:
            hora = raw_input('Hora (HH:MM): ')
            
            if len(hora) != 5:
                print('Digite um horário no formato informado.')
                continue
            else:
                break
            
        hora_marcada = converthora(hora)
        hora_servico = data_marcada.replace(hour = hora_marcada.hour, minute = hora_marcada.minute)
    
        if data_marcada.replace(hour = 8, minute = 0) <= hora_servico <= data_marcada.replace(hour = 19, minute = 0):
            break
        else:
            print('Barbearia fechada neste horário')
            time.sleep(1)
            continue
      
    servicos = db.todos_servicos()
    userservop = []
    
    for x in servicos[0]:
        userservop.append(x[1:4])
    
    
    serv = list([str(x[0]) for x in userservop])
    precos = list([str(x[1]) for x in userservop])
    duracao = list([str(x[2]) for x in userservop])
    
    
    if len(serv) == 0:
        print('Não há serviços cadastrados no sistema.')
        return
    else:
        while True:
            
            opcao = opt(serv)
            if opcao != len(serv)+1:
                print('Servico possui duracao de {} minutos'.format(duracao[opcao-1]))
                print('E custa R${}'.format(precos[opcao-1]))
                
                op = raw_input('Confirmar agendamento ? (s/n)')
                
                if op.lower() == 's':
                    id_servico = opcao
                    t_servico = db.tservico(id_servico)
                    hora_termino = hora_servico + datetime.timedelta(minutes = t_servico)
                    
                    agendamento = [id_cliente,'',id_servico,hora_servico,hora_termino,'agendamento pendente']
                
                    print('Agendamento realizado com sucesso. Aguarde confirmação.')    
                    
                    return agendamento
                
                elif op.lower() == 'n':
                    break
                else:
                    print('Digite uma opção válida.')
                    continue
            else:
                break
        
        return []
                
    

    


######################## PESSOAS ########################
def gerente(perfil):    
    
    while True:
        menu_inicial(perfil)
        opcao = opt(menu_gerente)
        
        if opcao != len(menu_gerente)+1:
            bs.evento_log('log_barbershop.txt',perfil[1],menu_gerente[opcao-1])
        
        if opcao == 1:
            
            sizedb = db.tamanho_db('dados')
            
            if sizedb == 0:
                print('Não há usuários a serem listados.')
                esperaenter()
                continue
            else:
                print('Listar usuários por:')
                
                filterop = opt(submenu_gerente[0])
                
                if filterop == 1:
                    db.filtro('login')
                    esperaenter()
                    continue
                elif filterop == 2:
                    db.filtro('nome')
                    esperaenter()
                    continue
                elif filterop == 3:
                    db.filtro('idade')
                    esperaenter()
                    continue
                elif filterop == 4:
                    db.filtro('perfil')
                    esperaenter()
                    continue
        
        elif opcao == 2:
            
            sizedb = db.tamanho_db('dados')
            
            if sizedb == 1:
                print('Não há usuários a serem analisados.')
                esperaenter()
                continue
            
            else:
                print('Análise dos cadastros')
                db.ler_db('dados')
                
                analiseop = opt(submenu_gerente[1])
                
                if analiseop == 1:
                    while True:
                        try:
                            id_usuario = int(raw_input("Digite o id do usuario: "))
                        except ValueError:
                            print('Digite um número no intervalo mostrado.')
                            continue
                        else:
                            break
                                     
                    print('Qual perfil desejado para este usuario ?')
                 
                    perfilop = opt(submenu_gerente[2])
                    
                    if perfilop == 1:
                        db.mudar_perfil('cliente',id_usuario)
                        continue
                    elif perfilop == 2:
                        db.mudar_perfil('funcionario',id_usuario)
                        continue
                    elif perfilop == 3:
                        db.mudar_perfil('gerente',id_usuario)
                        continue
                            
        elif opcao == 3:
            
            sizedb = db.tamanho_db('dados')
            
            if sizedb == 1:
                print('Não há usuários a serem deletados.')
                esperaenter()
                continue
            else:
                print('Deletar usuário')
                
                db.ler_db('dados')
                
                while True:
                    try:
                        id_usuario = int(raw_input("Digite o id do usuario: "))
                    except ValueError:
                        print('Digite um número no intervalo mostrado.')
                        continue
                    else:
                        break
                    
            
                print('Deseja realmente excluir esse usuário ? (s/n)')
                delop = raw_input()
                
                if delop.lower() == 's':
                    db.deletar(id_usuario,'dados')
                    db.delagend('id_cliente',id_usuario) #Deleta todos os dados remanescentes do usuário
                    continue
                elif delop.lower() == 'n':
                    continue
                else:
                    print('Digite uma opção válida.')
                    continue
        
        elif opcao == 4:
            tamanho = db.checaragend('','')
            
            if tamanho == 0:
                print('Não há agendamentos.')
                esperaenter()
                continue
            else:
                print('Checar agendamentos')
                db.read_agend()
                esperaenter()
                continue
        
     
        elif opcao == 5:
            editop = opt(submenu_gerente[4])
            
            if editop == 1:
                tamanho = db.checaragend('estado','agendamento pendente')
        
                if tamanho == 0:
                    print('Não há agendamentos a serem editados.')
                    esperaenter()
                    continue
                else:
                    print('Editar agendamentos')
                    print('\n' + 'Funcionários')
                    db.personread_dados('perfil', 'funcionario')
                    print('\n' + 'Agendamentos')
                    db.personread_agend('estado','agendamento pendente')
                   
                        
                    funcid = raw_input('Digite o id do funcionario: ')
                    agendid = raw_input('Digite o id do agendamento: ')
                    db.confirma_agend(funcid,'confirmado',agendid)
                    continue
      
            elif editop == 2:
                tamanho = db.checaragend('','')
                if tamanho == 0:
                    print('Não há agendamentos.')
                    esperaenter()
                    continue
                else:
                    db.read_agend()
                    deleteid = int(raw_input('Digite o id do agendamento: '))
                    db.delagend('id',deleteid)
                    continue
                
            elif editop == 3:
                continue
                     
        elif opcao == 6:                
            service = cad_servico()
            db.add_servico(service)
            continue
        
        elif opcao == 7:
            
            
            tamanho = db.todos_servicos()
            
            if tamanho[1] == 0:
                print('Não há serviços a serem editados.')
                esperaenter()
                continue
            else:
                print('Editar serviço')
                db.ler_db('servico')
                
                while True:
                    try:
                        serviceid = int(raw_input("Digite o id do servico: "))
                    except ValueError:
                        print('Digite um número no intervalo mostrado.')
                        continue
                    else:
                        break
                        
                serviceop = opt(submenu_gerente[3])
                
                if serviceop == 1:
                    print('1 - Alterar nome do servico')
                    print('2 - Alterar duracao do servico')
                    print('3 - Alterar preco do servico')
                    
                    serviceop = 0
                    serviceop = int(raw_input())
                    
                    if serviceop == 1:
                        servico = raw_input("Digite o nome do servico: ")
                        db.up_servico('campo','servico',servico,serviceid)
                        continue
                    elif serviceop == 2:
                        duracao = raw_input("Digite a duracao do servico: ")
                        db.up_servico('campo','duracao',duracao,serviceid)
                        continue
                    elif serviceop == 3:
                        preco = raw_input("Digite o preco do servico: ")
                        db.up_servico('campo','preco',preco,serviceid)
                        continue
                elif serviceop == 2:
                    newservice = cad_servico()
                    db.up_servico('todos','',newservice,serviceid)
                    continue
                elif serviceop == 3:              
                    delop = ''
                    delop = raw_input('Deseja realmente excluir esse servico ? (s/n)')
                    
                    if delop.lower() == 's':
                        db.deletar(serviceid, 'servico')
                        continue
                    elif delop.lower() == 'n':
                        continue
                    else:
                        print('Digite uma opção válida.')
                        esperaenter()
                        continue
                    
        elif opcao == 8:
            break

def funcionario(perfil):
      
    while True:
        menu_inicial(perfil)
        opcao = opt(menu_funcionario)
        usuarioid = db.id_user(perfil)
        
        if opcao != len(menu_funcionario)+1:
            bs.evento_log('log_barbershop.txt',perfil[1],menu_funcionario[opcao-1])
        
        if opcao == 1:         
            tamanho = db.checaragend('id_funcionario',usuarioid)
            
            if tamanho == 0:
                print('Não há compromissos no momento.')
                esperaenter()
                continue
            else:
                print('Meus compromissos')
                db.personread_agend('id_funcionario',usuarioid)
                esperaenter()
                continue
            
            
        elif opcao == 2:
            
            tamanho = db.checaragend('estado','agendamento pendente')
            
            if tamanho == 0:
                print('Não há agendamentos no momento.')
                esperaenter()
                continue
            else:
                print('Confirmar agendamentos')
                db.personread_agend('estado','agendamento pendente')
                id_number = raw_input('Digite o id: ')
                db.confirma_agend(usuarioid,'confirmado',id_number)
                continue
        
        elif opcao == 3:
            break
        
       
            

def cliente(perfil):
    usuarioid = db.id_user(perfil)
    
    while True:
        menu_inicial(perfil)
        opcao = opt(menu_cliente)
        
        if opcao != len(menu_cliente)+1:
            bs.evento_log('log_barbershop.txt',perfil[1],menu_cliente[opcao-1])

        if opcao == 1:
            print('Agendar serviço')
            
            agend = cad_agendamento(usuarioid)
            
            if len(agend) == 0:
                continue
            else:
                db.add_agendamento(agend)
                continue
        
        elif opcao == 2:
            tamanho = db.checaragend('id_cliente',usuarioid)
            if tamanho == 0:
                print('Não há agendamentos a serem checados')
                esperaenter()
                continue
            else:
                db.printagend(usuarioid,'checar')
                esperaenter()
                continue
        
        elif opcao == 3:
            tamanho = db.checaragend('id_cliente', usuarioid)
            if tamanho == 0:
                print('Não há agendamentos a serem cancelados')
                esperaenter()
                continue
            else:
                db.printagend(usuarioid,'deletar')
                while True:
                    try:
                        delop = int(raw_input('Digite o id: '))
                    except ValueError:
                        print('Digite um id.')
                        continue
                    else:
                        break          
                db.delagend('id',delop)
                continue
        elif opcao == 4:
            break
     

######################## PROGRAMA ########################


ini_menu = ['Login','Realizar Cadastro','Cancelar servico']

menu_cliente = ['Agendar serviço','Checar meus agendamentos','Cancelar serviço']
menu_funcionario = ['Meus compromissos','Confirmar agendamentos']
menu_gerente = ['Listar usuários por Categoria','Análise dos Cadastros','Deletar usuário','Checar agendamentos','Editar agendamentos','Adicionar serviço','Editar serviço']

submenu_gerente = [['Login','Nome','Idade','Perfil'],['Mudar perfil'],['Cliente','Funcionário','Gerente'],['Alterar por Campo','Alterar os Campos','Excluir serviço'],['Associar funcionario-agendamento','Deletar agendamento']]                    
submenu_funcionario = [['Login','Nome','Idade']]

    
db.user_db()
db.service_db()
db.agendadb()


sizedb = db.tamanho_db('dados')

while sizedb == 0:
    print('Foi adicionado um perfil de gerente para acesso inicial.')
    print('Login: Root')
    print('Senha: 123')
    print('Execute o sistema novamente' + '\n')
    
    default = ['Root','123','default',18,'12345678910','23/05/2000','gerente']
    db.inserir_db(default)
    break
else:

#PERFIL[0] - CARGO
#PERFIL[1] - LOGIN DO USUARIO : UTILIZAR NO ARQUIVO DE LOG
    while True:
        
        if os.path.exists('log_barbershop.txt') == False:
            open('log_barbershop.txt','w+')
            
        if os.stat('log_barbershop.txt').st_size == 0:
            bs.logmenu('log_barbershop.txt')
        
        
            
        perfil = ('','')
        menu()
        
        while True:
            try:
                layerop = int(raw_input())
            except ValueError:
                print('Digite um número no intervalo mostrado.')
                continue
            else:
                break
        
        if layerop == 1:
            menu_inicial(perfil)
            perfil = db.login()
            
            if perfil[0] == 'gerente':
                gerente(perfil)  
            elif perfil[0] == 'funcionario':
                funcionario(perfil)
            elif perfil[0] == 'cliente':
                cliente(perfil)
            else:
                break
                
            continue
        elif layerop == 2:
            menu_inicial(perfil)
            cd_user = cad_user()
            db.inserir_db(cd_user)
            continue
        elif layerop == 3:
            break
    
print('\n' + 'Agradecemos pela preferência.')
print('Tenha um bom dia !')  
db.close()
        



