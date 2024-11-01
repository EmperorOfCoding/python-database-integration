import os
import oracledb
import pandas as pd

try:
    conn = oracledb.connect(user="######", password="#####", dsn="####") #Digite o seu usuário, senha, url da conexao do banco

    inst_cadastro = conn.cursor()
    inst_consulta = conn.cursor()
    inst_alteracao = conn.cursor()
    inst_exclusao = conn.cursor()


except Exception as e:

    print("Erro: ", e )
    conexao = False

else:
    conexao = True

margem = ' ' * 4

while conexao:
        os.system('cls')

        print("---- CRUD - PETSHOP ----")
        print("""
              1 - CADASTRAR PET
              2 - LISTAR PETS
              3 - MODIFICAR PET
              4 - EXCLUIR PET
              5 - EXCLUIR TODOS OS PETS
              6 - SAIR)
              """)
        
        escolha = (input(margem + "Escolha -> "))

        if escolha.isdigit():
             escolha = int(escolha)

        else:
             escolha = 6
             print("Digite um número. \nReinicie a Aplicacao!")
             break

        os.system('cls')

        match escolha:
             
               case 1:
                  try:
                       print("----- CADASTRAR PET -----\n")

                       tipo = input(margem + "Digite o tipo...: ")
                       nome = input(margem + "Digite o nome...: ")
                       idade = int(input(margem + "Digite a idade...: "))

                       cadastro = (f"""INSERT INTO petshop (tipo_pet, nome_pet, idade) VALUES ('{tipo}', '{nome}', '{idade}')""")

                       inst_cadastro.execute(cadastro)
                       conn.commit()

                  except ValueError: #Erro de Valor
                       print("Digite um número na idade!")

                  except: #Caso de qualquer tipo de erro
                       print("Erro na transacao do BD")

                  else: #Caso haja sucesso no try
                       print("##### DADOS GRAVADOS COM SUCESSO #####")
   

               case 2:
                  
                  try:
                  
                     print("----- LISTAR PETS -----\n")
                     lista_dados = [] #Criando lista para armazenar dados

                     inst_consulta.execute('SELECT * FROM petshop') #Selecionando todos os elementos da tabela

                     data = inst_consulta.fetchall() #Armazenando os elementos em 'data'

                     for dt in data:
                         lista_dados.append(dt) #Percorrendo os elementos de data e adicionando dentro de 'lista_dados' 
                    
                     lista_dados = sorted(lista_dados) #Ordenando os dados (deixando em ordem)

                     dados_df = pd.DataFrame.from_records(lista_dados, columns=['ID', 'TIPO_PET', 'NOME_PET', 'IDADE'], index='ID') #Cria um DataFrame com os dados da lista utilizando Pandas

                     if dados_df.empty:
                         print("Nao há Pets cadastrados!")

                     else:
                         print(dados_df)  # Exibindo os dados

                         print("LISTADOS!")
                         input("Pressione ENTER")


                  except Exception as e:
                        print("Erro ao listar pets: ", e)

               
               case 3:

                    try:
                         print("----- ALTERAR DADOS DO PET -----\n")

                         lista_dados = []

                         pet_id = int(input(margem + "Escolha um Id: "))

                         consulta = (f"""SELECT * FROM petshop WHERE id = {pet_id}""")

                         inst_consulta.execute(consulta)
                         data = inst_consulta.fetchone()

                         for dt in data:
                              lista_dados.append(dt)

                         if len(lista_dados) == 0: #Verifica se a lista nao possui ID
                              print(f"Nao há um pet cadastrado com o ID = {pet_id}")
                              input("\nPressione ENTER")

                         else:
                              novo_tipo = input(margem + "Digite um novo tipo: ")
                              novo_nome = input(margem + "Digite um novo nome: ")
                              nova_idade= input(margem + "Digite uma nova idade: ")

                              alteracao = (f"""UPDATE petshop SET tipo_pet='{novo_tipo}', nome_pet='{novo_nome}', idade='{nova_idade}' WHERE id={pet_id}""")

                              inst_alteracao.execute(alteracao)
                              conn.commit()

                    except ValueError:
                         print("Digite um Número na idade!")
                         input("\nPressione ENTER")

                    except:
                         print("Erro na transacao BD")
                         input("\nPressione ENTER")

                    else:
                         print("Dados Atualizados")
                         input("Pressione ENTER")


               case 4:

                    try:
                         print("----- EXCLUIR O PET -----\n")
                         
                         lista_dados = []

                         pet_id = input(margem + "Escolha um Id: ")

                         if pet_id.isdigit():
                              
                              pet_id = int(pet_id)

                              consulta = f"""SELECT * FROM petshop WHERE id = {pet_id}"""
                              inst_consulta.execute(consulta)
                              data = inst_consulta.fetchall()

                              for dt in data:
                                   lista_dados.append(dt)

                              if len(lista_dados) == 0:
                                   print(f"Nao há um pet cadastrado com o ID = {pet_id}")
                                   input("Pressione ENTER")

                              else:
                                   exclusao = f"DELETE FROM petshop WHERE id={pet_id}"
                                   inst_exclusao.execute(exclusao)
                                   conn.commit()
                                   print("\n##### PET APAGADO! #####")

                         else:
                              print("O Id nao é numérico!")
                              input("Pressione ENTER")

                         
                    except Exception as e:
                         print("Erro = ", e)


               case 5:

                    try:
                         print("----- EXCLUIR TODOS OS PETS -----\n")

                         confirma = input(margem + "CONFIRMA A EXCLUSAO DE TODOS OS PETS? [S]im ou [N]ao?")

                         if confirma.upper() == "S":

                              exclusao = "DELETE FROM petshop"
                              inst_exclusao.execute(exclusao)
                              conn.commit()

                              #Depois de excluir, é necessário resetar os IDS para comecar a partir do 0.

                              data_reset_ids = """ALTER TABLE petshop MODIFY(ID GENERATED AS IDENTITY (START WITH 1))"""
                              inst_exclusao.execute(data_reset_ids)
                              conn.commit()

                              print("##### REGISTROS EXCLUIDOS COM SUCESSO! #####")
                              input("Pressione ENTER")

                         else:
                              print("Operacao cancelada pelo usuário!")
                              input("Pressione ENTER")

                         input("Pressione ENTER")


                    except Exception as e:
                         print("Erro = ", e)



          









                                   











                    







                         

              

                

                       

            






                     
                       
                       

        
        
        
