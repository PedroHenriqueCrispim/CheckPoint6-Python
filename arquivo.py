import json
import requests

# Função para carregar os dados de clientes do arquivo JSON
def carregar_clientes():
    try:
        with open('clientes.json', 'r') as file:
            clientes = json.load(file)
    except FileNotFoundError:
        clientes = []
    return clientes

# Função para salvar os dados dos clientes no arquivo JSON
def salvar_clientes(clientes):
    with open('clientes.json', 'w') as file:
        json.dump(clientes, file, indent=2)

# Função para buscar o CEP na API ViaCEP
def buscar_cep(cep):
    try:
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(url)
        data = response.json()
        return data
    except requests.exceptions.ConnectTimeout:
        print('Erro ao carregar API, aguarde..')
        return data

# Função para adicionar um novo cliente
def inserir_cliente(clientes):
    id_cliente = len(clientes) + 1
    email = input('Digite o email do cliente: ')
    nome = input('Digite o nome do cliente: ')
    senha = input('Digite a senha do cliente (mínimo 8 caracteres): ')
    while len(senha) < 8:
        senha = input('A senha deve ter no mínimo 8 caracteres. Digite a senha novamente: ')

    cep = input('Digite o CEP do cliente: ')
    endereco = buscar_cep(cep)
    if 'erro' in endereco:
        print('CEP não encontrado. Verifique o CEP e tente novamente.')
        return

    rua = endereco['logradouro']
    bairro = endereco['bairro']
    municipio = endereco['localidade']
    uf = endereco['uf']

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

# Função para excluir um cliente
def excluir_cliente(clientes, id_cliente):
    for cliente in clientes:
        if cliente['id'] == id_cliente:
            clientes.remove(cliente)
            salvar_clientes(clientes)
            print(f'Cliente com ID {id_cliente} excluído com sucesso.')
            return
    print(f'Cliente com ID {id_cliente} não encontrado.')

# Função para alterar os dados de um cliente
def alterar_cliente(clientes, id_cliente):
    for cliente in clientes:
        if cliente['id'] == id_cliente:
            print('O que deseja alterar?')
            print('1 - Email')
            print('2 - Nome')
            print('3 - Senha')
            opcao = input('Digite o número da opção: ')
            if opcao == '1':
                novo_email = input('Digite o novo email: ')
                cliente['email'] = novo_email
                salvar_clientes(clientes)
                print('Email alterado com sucesso.')
            elif opcao == '2':
                novo_nome = input('Digite o novo nome: ')
                cliente['nome'] = novo_nome
                salvar_clientes(clientes)
                print('Nome alterado com sucesso.')
            elif opcao == '3':
                nova_senha = input('Digite a nova senha (mínimo 8 caracteres): ')
                while len(nova_senha) < 8:
                    nova_senha = input('A senha deve ter no mínimo 8 caracteres. Digite a senha novamente: ')
                cliente['senha'] = nova_senha
                salvar_clientes(clientes)
                print('Senha alterada com sucesso.')
            else:
                print('Opção inválida.')
            return
    print(f'Cliente com ID {id_cliente} não encontrado.')

# Função para listar todos os clientes
def listar_clientes(clientes):
    if not clientes:
        print('Nenhum cliente cadastrado.')
    for cliente in clientes:
        print(f'ID: {cliente["id"]}')
        print(f'Email: {cliente["email"]}')
        print(f'Nome: {cliente["nome"]}')
        print(f'Senha: {cliente["senha"]}')
        print('Endereço:')
        endereco = cliente['endereco']
        print(f'  Rua: {endereco["rua"]}')
        print(f'  Número: {endereco["numero"]}')
        print(f'  Complemento: {endereco["complemento"]}')
        print(f'  Bairro: {endereco["bairro"]}')
        print(f'  Município: {endereco["municipio"]}')
        print(f'  UF: {endereco["uf"]}')
        print(f'  CEP: {endereco["cep"]}')
        print()

def main():
    clientes = carregar_clientes()
    
    while True:
        print('Sistema de Cadastro de Clientes')
        print('1 - Inserir cliente')
        print('2 - Excluir cliente')
        print('3 - Alterar cliente')
        print('4 - Consultar clientes')
        print('5 - Sair')
        opcao = input('Digite o número da opção: ')

        if opcao == '1':
            inserir_cliente(clientes)
        elif opcao == '2':
            id_cliente = int(input('Digite o ID do cliente a ser excluído: '))
            excluir_cliente(clientes, id_cliente)
        elif opcao == '3':
            id_cliente = int(input('Digite o ID do cliente a ser alterado: '))
            alterar_cliente(clientes, id_cliente)
        elif opcao == '4':
            listar_clientes(clientes)
        elif opcao == '5':
            print('Saindo do sistema.')
            break
        else:
            print('Opção inválida. Tente novamente.')

if __name__ == "__main__":
    main()
