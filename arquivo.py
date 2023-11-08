"""
Pedro Henrique Crispim RM:99005
Caique Chagas RM:551943
Rodrigo Resende RM:551057
"""

import json
import requests

""" Função para carregar os dados de clientes do arquivo JSON """
def carregar_clientes():
    try:
        with open('clientes.json', 'r') as file:
            clientes = json.load(file)
            for cliente in clientes:
                cliente['id'] = int(cliente['id'])
    except FileNotFoundError:
            clientes = []
    return clientes

""" Função para salvar os dados dos clientes no arquivo JSON """
def salvar_clientes(clientes):
    for cliente in clientes:
        cliente['id'] = str(cliente['id'])
    with open('clientes.json', 'w', encoding='utf-8') as file:
        json.dump(clientes, file, indent=4)

""" Função para buscar o CEP na API ViaCEP """
def buscar_cep(cep):
    while True:
        try:
            url = f'https://opencep.com/v1/{cep}'
            resposta = requests.get(url)
            if resposta.status_code == 200:
                dicionario = resposta.json()
                if 'erro' in dicionario:
                    print("Erro: CEP não existe. ")
                    novo_cep = input("Digite o CEP novamente: ")
                    if novo_cep.isdigit() and len(novo_cep) == 8: #verifica se tem 8 digitos no CEP
                        cep = novo_cep
                    else:
                        print("CEP invalido. Tente novamente. ")
                else:
                    return dicionario
            else:
                print(f"Erro: Status code {resposta.status_code}")
                novo_cep = input("Digite o CEP novamente: ")
                if novo_cep.isdigit() and len(novo_cep) == 8:  #verifica se tem 8 dígitos no CEP
                    cep = novo_cep
                else:
                    print("CEP inválido. Tente novamente. ")
        except requests.exceptions.ConnectTimeout:
            print('Erro ao carregar API, aguarde..')
            continue


""" Função para validar se uma string pode ser convertida para um número inteiro positivo """
def validar_id(id_str):
    try:
        id_cliente = int(id_str)
        if id_cliente > 0:
            return id_cliente
        else:
            print('ID deve ser um número inteiro positivo.')
    except ValueError:
        print('ID deve ser um número inteiro positivo.')


""" Função para adicionar um novo cliente """
def inserir_cliente(clientes):
    email = input('Digite o email do cliente: ')
    nome = input('Digite o nome do cliente: ')

    while True:
        id_cliente = input('Digite o ID do cliente: ')
        if any(cliente['id'] == id_cliente for cliente in clientes):
            print(f'Já existe um cliente com o ID {id_cliente}. Escolha outro ID.')
        elif not id_cliente.isdigit() or int(id_cliente) <= 0:
            print('O ID deve ser um número inteiro positivo. Tente novamente.')
        else:
            break

    senha = input('Digite a senha do cliente (mínimo 8 caracteres): ')
    while len(senha) < 8:
        senha = input('A senha deve ter no mínimo 8 caracteres. Digite a senha novamente: ')

    cep = input('Digite o CEP do cliente: ')
    endereco = buscar_cep(cep)

    if not endereco:
        print('CEP não encontrado. Verifique o CEP e tente novamente.')
        return

    rua = endereco.get('logradouro', '')
    bairro = endereco.get('bairro', '')
    municipio = endereco.get('localidade', '')
    uf = endereco.get('uf', '')

    numero = input('Digite o número: ')
    complemento = input('Digite o complemento: ')

    cliente = {
        'id': id_cliente,
        'email': email,
        'nome': nome,
        'senha': senha,
        'endereco': {
            'rua': rua,
            'numero': numero,
            'complemento': complemento,
            'bairro': bairro,
            'municipio': municipio,
            'uf': uf,
            'cep': cep
        }
    }

    clientes.append(cliente)
    salvar_clientes(clientes)
    print('Cliente cadastrado com sucesso.')



""" Função para excluir um cliente """
def excluir_cliente(clientes, id_cliente):
    id_cliente = int(id_cliente)
    for cliente in clientes:
        if cliente['id'] == id_cliente:
            clientes.remove(cliente)
            salvar_clientes(clientes)
            print(f'Cliente com ID {id_cliente} excluído com sucesso.')
            return
    print(f'Cliente com ID {id_cliente} não encontrado.')

""" Função para alterar os dados de um cliente """
def alterar_cliente(clientes, id_cliente):
    id_cliente = int(id_cliente)
    for cliente in clientes:
        if cliente['id'] == id_cliente:
            print('O que deseja alterar?')
            print('1 - Email')
            print('2 - Nome')
            print('3 - Senha')
            print('4 - CEP')
            opcao = input('Digite o número da opção: ')
            
            if opcao == '1':
                novo_email = input('Digite o novo email: ')
                cliente['email'] = novo_email
            elif opcao == '2':
                novo_nome = input('Digite o novo nome: ')
                cliente['nome'] = novo_nome
            elif opcao == '3':
                nova_senha = input('Digite a nova senha (mínimo 8 caracteres): ')
                while len(nova_senha) < 8:
                    nova_senha = input('A senha deve ter no mínimo 8 caracteres. Digite a senha novamente: ')
                cliente['senha'] = nova_senha
            elif opcao == '4':
                novo_cep = input('Digite o novo CEP: ')
                endereco = buscar_cep(novo_cep)
                if not endereco:
                    print('CEP não encontrado. Verifique o CEP e tente novamente.')
                    return
                cliente['endereco']['cep'] = novo_cep
                cliente['endereco']['rua'] = endereco.get('logradouro', '')
                cliente['endereco']['bairro'] = endereco.get('bairro', '')
                cliente['endereco']['municipio'] = endereco.get('localidade', '')
                cliente['endereco']['uf'] = endereco.get('uf', '')
                cliente['endereco']['numero'] = input('Digite o novo número: ')
                cliente['endereco']['complemento'] = input('Digite o novo complemento: ')
            else:
                print('Opção inválida.')
                return

            salvar_clientes(clientes)
            print('Dados do cliente alterados com sucesso.')
            return
    print(f'Cliente com ID {id_cliente} não encontrado.')

""" Função para listar todos os clientes """
def listar_clientes(clientes):
    if not clientes:
        print('Nenhum cliente cadastrado.')
    else:
        print('ID - Nome')
        for cliente in clientes:
            print(f'{cliente["id"]} - {cliente["nome"]}')
    print()

""" Função consultar os clientes"""
def consultar_cliente(clientes):
    listar_clientes(clientes)
    id_consultar = input('Digite o ID do cliente que deseja consultar ou pressione Enter para sair: ')

    if id_consultar:
        id_consultar = int(id_consultar)
        for cliente in clientes:
            if cliente['id'] == id_consultar:
                print('\nInformações do cliente:')
                print(f'ID: {cliente["id"]}')
                print(f'Nome: {cliente["nome"]}')
                print(f'Email: {cliente["email"]}')
                print(f'Senha: {cliente["senha"]}')
                print('Endereço:')
                endereco = cliente['endereco']
                print(f'Rua: {endereco["rua"]}')
                print(f'Número: {endereco["numero"]}')
                print(f'Complemento: {endereco["complemento"]}')
                print(f'Bairro: {endereco["bairro"]}')
                print(f'Município: {endereco["municipio"]}')
                print(f'UF: {endereco["uf"]}')
                print(f'CEP: {endereco["cep"]}')
                break
        else:
            print(f'Cliente com ID {id_consultar} não encontrado.')
    print()


""" Função principal do codigo """
def main():
    clientes = carregar_clientes()

    while True:
        print('Sistema de Cadastro de Clientes')
        print('1 - Inserir cliente')
        print('2 - Excluir cliente')
        print('3 - Alterar cliente')
        print('4 - Consultar clientes')
        print('0 - Sair')
        opcao = input('Digite o número da opção: ')

        if opcao == '1':
            inserir_cliente(clientes)
            salvar_clientes(clientes) 
        elif opcao == '2':
            listar_clientes(clientes)
            id_cliente = int(input('Digite o ID do cliente a ser excluído: '))
            excluir_cliente(clientes, id_cliente)
            salvar_clientes(clientes) 
        elif opcao == '3':
            listar_clientes(clientes)
            id_cliente = int(input('Digite o ID do cliente a ser alterado: '))
            alterar_cliente(clientes, id_cliente)
            salvar_clientes(clientes)  
        elif opcao == '4':
            consultar_cliente(clientes)
        elif opcao == '0':
            print('Programa encerrado.')
            salvar_clientes(clientes) 
            break
        else:
            print('Opção inválida. Tente novamente.')

if __name__ == "__main__":
    main()
