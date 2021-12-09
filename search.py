from util import spearman, kendal_tau


def main():
    run = True
    while(run):
        on_query = True
        word_query = []
        while(on_query):
            print("Campos: [geral, memoria, tela, ram, preço, marca]")
            camp = input("Campo que deseja consultar: ")
            value = input("Valor que deseja neste campo: ")
            words = value.split()
            if(camp != "geral"):
                words = [(word + '.' + camp).lower() for word in words]
            
            word_query.extend(words)
            end_query = input("Deseja adicionar mais algo a esta consulta? [Y/n]")
            if(end_query == "n"):
                on_query = False
        
        print("Realizando consulta.....")
        rank = query(word_query)
        print("Resultado encontrado: ", rank)
        end_run = input("Deseja fazer mais uma consulta? [Y/n]")
        if(end_run == "n"):
            run = False

    return ("Processo Finalizado")

def query(words):
    return words


if __name__ == "__main__":
    print(main())