import pandas as pd
from tqdm import tqdm
import os.path


def get_class1(database=pd.read_excel("Database1.xlsx"), input=pd.read_excel("Input.xlsx")):
    #
    # Funzione per classificare in automatico i dati in base ai parametri contenuti nel database
    #
    # database: database su cui si basa la classificazione
    # input: dati di output
    # output: dati classificati
    #

    #liste vuote usate nella classificazione
    compounds = [] # lista di tutti i composti
    class_compounds = [] # lista di tutte le classi dei composti

    for i in tqdm(input["Compound"]): #leggo i composti dall'input
        compounds.append(i) #aggiungo il nome del i composto nella lista dei composti
        if i in database["Compound"].to_numpy(): #controllo se il composto i è presente nel database, se si aggiungo la classe conosciuta
            class_compounds.append(
                database["Class"][database[database["Compound"] == i].index[0]])
        else: #se no, classifica il composto come sconosciuto
            class_compounds.append("Unknown")

    output = pd.DataFrame(list(zip(compounds, class_compounds)),
                          columns=["Compound", "Class"]) #creo il dataframe con i dati classificati

    print("Report of your input:")
    print(output["Class"].value_counts()) #print della descrizione dei composti classificati
    print("\n")

    if os.path.isfile('Output.xlsx'): #controllo se esiste già un file di output
        print("File \"Output.xlsx\" alredy exists in this directory.\nIf you want to obtain a new one, delete it.")
    else:
        print("File \"Output.xlsx\" will be saved in this directory.")
        output.to_excel("Output.xlsx") #converto il dataframe in un file excel
    
    print("Alla prossima ;)")
