import psycopg2

# - Inserir ou atualizar cliente:
def upsert_cliente(cursor, cliente_id, cliente_nome, cliente_cep):
    try:
        # Tenta inserir o cliente. Se o ClienteID já existir, atualiza o nome e o CEP.
        sql = """
        INSERT INTO Cliente (ClienteID, ClienteNome, ClienteCEP)
        VALUES (%s, %s, %s)
        ON CONFLICT (ClienteID) DO UPDATE SET
            ClienteNome = EXCLUDED.ClienteNome,
            ClienteCEP = EXCLUDED.ClienteCEP;
        """
        cursor.execute(sql, (cliente_id, cliente_nome, cliente_cep))
        conn.commit() # Garante que a transação seja efetivada
        print(f"Cliente com ID {cliente_id} inserido/atualizado com sucesso.")
    except Exception as e:
        conn.rollback() # Desfaz a transação em caso de erro
        print(f"Erro ao inserir/atualizar cliente com ID {cliente_id}:", e)

# - Listar clientes:
def listar_clientes(cursor):
    try:
        cursor.execute("SELECT ClienteID, ClienteNome, ClienteCEP FROM Cliente ORDER BY ClienteID;")
        rows = cursor.fetchall()
        if rows:
            print("\n==== Lista de Clientes ====")
            for row in rows:
                print(f"ID: {row[0]}, Nome: {row[1]}, CEP: {row[2]}")
        else:
            print("\nNenhum cliente cadastrado.")
    except Exception as e:
        print("Erro ao listar clientes:", e)

# - Excluir cliente:
def excluir_cliente(cursor, cliente_id):
    try:
        # Verifica se o cliente existe antes de tentar excluir
        cursor.execute("SELECT ClienteID FROM Cliente WHERE ClienteID = %s;", (cliente_id,))
        if cursor.fetchone() is None:
            print(f"Cliente com ID {cliente_id} não encontrado.")
            return

        sql = "DELETE FROM Cliente WHERE ClienteID = %s;"
        cursor.execute(sql, (cliente_id,))
        conn.commit() # Garante que a transação seja efetivada
        print(f"Cliente com ID {cliente_id} excluído com sucesso.")
    except psycopg2.Error as e: # Captura erros específicos do psycopg2
        conn.rollback() # Desfaz a transação em caso de erro
        # Verifica se o erro é de violação de chave estrangeira
        if e.pgcode == '23503': # Código de erro para foreign key violation
            print(f"Erro ao excluir cliente com ID {cliente_id}: Este cliente está referenciado em outras tabelas (ex: Trans_de_Venda) e não pode ser excluído.")
        else:
            print(f"Erro ao excluir cliente com ID {cliente_id}:", e)
    except Exception as e:
        conn.rollback() # Desfaz a transação em caso de erro genérico
        print(f"Erro inesperado ao excluir cliente com ID {cliente_id}:", e)


def main():
    global conn # Tornar conn acessível globalmente para rollback e commit
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()

    while True:
        print("\n==== Menu Cliente ====")
        print("1 - Inserir/Atualizar Cliente")
        print("2 - Listar Clientes")
        print("3 - Excluir Cliente")
        print("0 - Sair")

        try:
            option = int(input("Escolha uma opção: "))
            if option == 0:
                print("Encerrando...")
                break
            elif option == 1:
                try:
                    cliente_id = int(input("Digite o ID do Cliente: "))
                    cliente_nome = input("Digite o Nome do Cliente: ")
                    cliente_cep = input("Digite o CEP do Cliente (8 dígitos): ")

                    if not cliente_nome:
                        print("O nome do cliente não pode ser vazio.")
                        continue
                    if not cliente_cep or not cliente_cep.isdigit() or len(cliente_cep) != 8:
                        print("CEP inválido. Deve conter 8 dígitos numéricos.")
                        continue

                    upsert_cliente(cursor, cliente_id, cliente_nome, cliente_cep)
                except ValueError:
                    print("ID do Cliente deve ser um número inteiro.")
                except Exception as e:
                    print(f"Ocorreu um erro: {e}")
            elif option == 2:
                listar_clientes(cursor)
            elif option == 3:
                try:
                    cliente_id_excluir = int(input("Digite o ID do Cliente a ser excluído: "))
                    excluir_cliente(cursor, cliente_id_excluir)
                except ValueError:
                    print("ID do Cliente deve ser um número inteiro.")
                except Exception as e:
                    print(f"Ocorreu um erro ao tentar excluir o cliente: {e}")
            else:
                print("Opção inválida! Tente novamente.")
        except ValueError:
            print("Entrada inválida! Digite um número.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    conn = None # Inicializa conn como None
    main()