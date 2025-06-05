import psycopg2

#- Conexão com o banco: A função connect_db estabelece a conexão com o PostgreSQL.

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="patroklo"
        )
        # Define o schema default
        conn.cursor().execute("SET search_path TO zagi;")
        return conn
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None


#- Listagem de tabelas: A função list_table executa um SELECT * na tabela escolhida e exibe os resultados.

def list_table(cursor, table_name):
    try:
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        if rows:
            print(f"\nConteúdo da tabela {table_name}:")
            for row in rows:
                print(row)
        else:
            print(f"\nA tabela {table_name} está vazia.")
    except Exception as e:
        print(f"Erro ao listar a tabela {table_name}:", e)


def main():
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()
    tables = [
        "Fornecedor", "Cliente", "Regiao", "Categoria",
        "Produto", "Loja", "Trans_de_Venda", "Incluido_em"
    ]


# Menu interativo: O menu permite ao usuário selecionar a tabela que deseja listar ou encerrar o programa.

    while True:
        print("\n==== Menu de Listagem ====")
        for i, table in enumerate(tables, start=1):
            print(f"{i} - {table}")
        print("0 - Sair")
        # - Tratamento de erros: Inclui verificações para conexões e entradas inválidas.
        try:
            option = int(input("Escolha a tabela que deseja listar: "))
            if option == 0:
                print("Encerrando...")
                break
            elif 1 <= option <= len(tables):
                list_table(cursor, tables[option - 1])
            else:
                print("Opção inválida! Tente novamente.")
        except ValueError:
            print("Entrada inválida! Digite um número.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()