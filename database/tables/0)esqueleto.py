import psycopg2

""" MODELO DE INTERFACE NO TERMINAL """
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
