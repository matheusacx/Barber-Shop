# -*- coding: utf-8 -*-
"""
BarberShop - Arquivo Log
Autor: Matheus Aryell Cavalcante Xavier

"""

import datetime

        
def logmenu(datafile):
    
    log_file = open(datafile, 'a')
    
    log_file.write("*"*40 + '\n')
    log_file.write("BarberShop - Arquivo de Log" + '\n')
    log_file.write("*"*40 + '\n')
    
def evento_log(datafile, usuario, acao):
    
    log_file = open(datafile, 'a')
    t_acao = datetime.datetime.now()
    
    # [HORA] : USUARIO -> ACAO
    log_file.write("[{}:{}] : {} -> {}".format(t_acao.hour, t_acao.minute, usuario, acao) + '\n')
    log_file.close()
    

