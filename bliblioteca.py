# === Base de dados inicial ===
usuarios = {
    "admin@gmail.com": {
        "senha": "admin",
        "nome": "Administrador",
        "nivel": "Administrador"
    }
}

livros = {
    "9780132350884": {
        "titulo": "Clean Code",
        "autor": "Robert C. Martin",
        "ano": "2008",
        "quantidade": 2
    },
    "9780201616224": {
        "titulo": "The Pragmatic Programmer",
        "autor": "Andrew Hunt",
        "ano": "1999",
        "quantidade": 1
    },
    "9780131103627": {
        "titulo": "The C Programming Language",
        "autor": "Brian W. Kernighan",
        "ano": "1988",
        "quantidade": 0  # Sem exemplares
    }
}

emprestimos = {
    "admin@gmail.com": ["9780132350884", "9780201616224"]
}
# Atualiza estoque baseado em empréstimos
for email in emprestimos:
    for isbn in emprestimos[email]:
        if isbn in livros:
            livros[isbn]["quantidade"] -= 1

# === Funções do sistema ===

def login():
    print("===== Login =====")
    email = input("Email: ")
    senha = input("Senha: ")
    if email in usuarios and usuarios[email]["senha"] == senha:
        print(f"Bem-vindo, {usuarios[email]['nome']}! Nível: {usuarios[email]['nivel']}")
        return email
    else:
        print("Email ou senha incorretos.")
        return None

def controle_usuarios():
    print("===== Controle de Usuários =====")
    for email, dados in usuarios.items():
        print(f"{dados['nome']} | Email: {email} | Nível: {dados['nivel']}")

    print("\n1. Cadastrar novo usuário")
    print("2. Voltar")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        email = input("Novo email: ")
        if email in usuarios:
            print("Usuário já existe.")
            return
        nome = input("Nome: ")
        senha = input("Senha: ")
        nivel = input("Nível (Administrador, Bibliotecário, Usuário comum): ")
        if nivel not in ["Administrador", "Bibliotecário", "Usuário comum"]:
            print("Nível inválido.")
            return
        usuarios[email] = {"senha": senha, "nome": nome, "nivel": nivel}
        print("Usuário cadastrado com sucesso!")
    elif opcao == "2":
        return
    else:
        print("Opção inválida.")

def cadastrar_livro():
    print("===== Cadastro de Livro =====")
    isbn = input("ISBN: ")
    if isbn in livros:
        print("Livro já cadastrado.")
        return
    titulo = input("Título: ")
    autor = input("Autor: ")
    ano = input("Ano: ")
    quantidade = int(input("Quantidade: "))
    livros[isbn] = {"titulo": titulo, "autor": autor, "ano": ano, "quantidade": quantidade}
    print("Livro cadastrado com sucesso!")

def pesquisar_livro():
    print("===== Pesquisar Livro =====")
    termo = input("Digite título, autor ou ISBN: ").lower()
    encontrados = False
    for isbn, dados in livros.items():
        if termo in dados["titulo"].lower() or termo in dados["autor"].lower() or termo in isbn:
            print(f"ISBN: {isbn} | {dados['titulo']} - {dados['autor']} ({dados['ano']}) | Quantidade: {dados['quantidade']}")
            encontrados = True
    if not encontrados:
        print("Nenhum livro encontrado.")

def emprestar_livro():
    print("===== Empréstimo de Livro =====")
    email = input("Email do usuário: ")
    if email not in usuarios:
        print("Usuário não cadastrado.")
        return
    isbn = input("ISBN do livro: ")
    if isbn not in livros or livros[isbn]["quantidade"] <= 0:
        print("Livro não disponível.")
        return
    livros[isbn]["quantidade"] -= 1
    emprestimos.setdefault(email, []).append(isbn)
    print("Livro emprestado com sucesso!")

def devolver_livro():
    print("===== Devolução de Livro =====")
    email = input("Email do usuário: ")
    if email not in emprestimos or not emprestimos[email]:
        print("Nenhum empréstimo encontrado para este usuário.")
        return
    print("Livros emprestados:")
    for i, isbn in enumerate(emprestimos[email]):
        print(f"{i + 1}. {livros[isbn]['titulo']} (ISBN: {isbn})")
    escolha = int(input("Digite o número do livro a devolver: ")) - 1
    if 0 <= escolha < len(emprestimos[email]):
        isbn = emprestimos[email].pop(escolha)
        livros[isbn]["quantidade"] += 1
        print("Livro devolvido com sucesso!")
    else:
        print("Escolha inválida.")

def livros_emprestados():
    print("===== Livros Emprestados =====")
    encontrados = False
    for email, lista in emprestimos.items():
        if lista:
            print(f"\nUsuário: {usuarios[email]['nome']} ({email})")
            for isbn in lista:
                livro = livros.get(isbn, {"titulo": "Desconhecido"})
                print(f" - {livro['titulo']} (ISBN: {isbn})")
                encontrados = True
    if not encontrados:
        print("Nenhum livro emprestado no momento.")

def relatorios():
    print("===== Relatórios =====")
    print("1. Livros cadastrados")
    print("2. Livros emprestados")
    print("3. Usuários")
    opcao = input("Escolha: ")
    if opcao == "1":
        for isbn, dados in livros.items():
            print(f"{isbn}: {dados['titulo']} - {dados['autor']} ({dados['ano']}) | Qtd: {dados['quantidade']}")
    elif opcao == "2":
        livros_emprestados()
    elif opcao == "3":
        controle_usuarios()
    else:
        print("Opção inválida.")

def controle_livros():
    print("===== Controle de Livros =====")

    print("\n📘 Livros Disponíveis:")
    for isbn, dados in livros.items():
        if dados["quantidade"] > 0:
            print(f"{isbn}: {dados['titulo']} - {dados['autor']} ({dados['ano']}) | Qtd: {dados['quantidade']}")

    print("\n📕 Livros PENDENTES (sem exemplares disponíveis):")
    for isbn, dados in livros.items():
        if dados["quantidade"] == 0:
            print(f"{isbn}: {dados['titulo']} - {dados['autor']} ({dados['ano']}) | Qtd: 0")

    print("\n📚 Livros Emprestados:")
    livros_emprestados()

    print("\n1. Editar livro")
    print("2. Remover livro")
    opcao = input("Escolha: ")
    isbn = input("Digite o ISBN: ")
    if isbn not in livros:
        print("Livro não encontrado.")
        return
    if opcao == "1":
        livros[isbn]["titulo"] = input("Novo título: ")
        livros[isbn]["autor"] = input("Novo autor: ")
        livros[isbn]["ano"] = input("Novo ano: ")
        livros[isbn]["quantidade"] = int(input("Nova quantidade: "))
        print("Livro atualizado.")
    elif opcao == "2":
        del livros[isbn]
        print("Livro removido.")
    else:
        print("Opção inválida.")

# === Menu principal ===
def menu_principal(usuario_logado):
    while True:
        nivel = usuarios[usuario_logado]['nivel']
        print("\n===== Menu =====")
        if nivel == "Administrador":
            print("1. Controle de usuários")
        if nivel in ["Administrador", "Bibliotecário"]:
            print("2. Cadastrar livro")
        print("3. Pesquisar livro")
        if nivel in ["Administrador", "Bibliotecário"]:
            print("4. Emprestar livro")
            print("5. Devolver livro")
            print("6. Relatórios")
        if nivel == "Administrador":
            print("7. Controle de livros")
        print("8. Sair")

        opcao = input("Escolha: ")

        if opcao == "1" and nivel == "Administrador":
            controle_usuarios()
        elif opcao == "2" and nivel in ["Administrador", "Bibliotecário"]:
            cadastrar_livro()
        elif opcao == "3":
            pesquisar_livro()
        elif opcao == "4" and nivel in ["Administrador", "Bibliotecário"]:
            emprestar_livro()
        elif opcao == "5" and nivel in ["Administrador", "Bibliotecário"]:
            devolver_livro()
        elif opcao == "6" and nivel in ["Administrador", "Bibliotecário"]:
            relatorios()
        elif opcao == "7" and nivel == "Administrador":
            controle_livros()
        elif opcao == "8":
            print("Saindo...")
            break
        else:
            print("Opção inválida ou acesso negado.")

# === Início do programa ===
usuario = login()
if usuario:
    menu_principal(usuario)
