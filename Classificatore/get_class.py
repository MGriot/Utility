def get_class(database, input, save_dropped_compounds):
    """
    # This function will eliminate compounds that do not meet the area and match factor or elemental composition criteria and classify the remaining compounds based on the database provided.
    # This feature was written by M.Griot and you can find the original version at https://github.com/MGriot/Utility
    #
    # database: database su cui si basa la classificazione
    # input: dati di input
    # output: dati classificati in output
    """
    #importin the libraries
    import pandas as pd
    import numpy as np
    from tqdm import tqdm
    import os.path
    import re

    #message when you start the function
    print("Starting the classification process...")
    #liste vuote usate nella classificazione
    compounds = []  # lista di tutti i composti
    class_compounds = []  # lista di tutte le classi dei composti

    a = 0
    no_match_value = []
    errate_formulae = []

    #parte per eliminare le righe
    print("I start removing compounds in the input that don't suit the parameters.")
    for i in tqdm(input["compound name"]):
        #removing compound with errate number for area and match factor
        if input["area"][a] < 1e5 or input["Match factor"][a] < 70:
            no_match_value.append(a)

        #removing all numbers from the string
        s = input["formula"][a]
        try:
            result = re.sub(r'[0-9]+', '', s)
            #split the string into a list of elements
            result = re.findall('[A-Z][^A-Z]*', result)
        except:
            result = ""
        for i in result:
            if "F" in i:
                errate_formulae.append(a)
            elif "Cl" in i:
                errate_formulae.append(a)
            elif "S" in i:
                errate_formulae.append(a)
            elif "P" in i:
                errate_formulae.append(a)
            elif "Si" in i:
                errate_formulae.append(a)
        a += 1
    #elimino tutte le righe che non passano i test per i valori e la formula
    dropped_rows = np.unique(no_match_value + errate_formulae)

    if save_dropped_compounds == True:  # creo un file dei composti cancellati se metti True, se metti False ti mostro solo l'id dei composti cancellati
        #creo un nuovo database con i composti eliminati
        dropped_database = input.loc(0)[dropped_rows]
        dropped_names = dropped_database["compound name"]
        dropped_rt = dropped_database["RT"]
        dropped_area = dropped_database["area"]
        dropped_area_ = dropped_database["% area"]
        dropped_Match_factor = dropped_database["Match factor"]
        dropped_formula = dropped_database["formula"]
        dropped_area_area = dropped_database["area/area"]

        dropped_compounds = pd.DataFrame(list(zip(dropped_rt, dropped_names, dropped_area, dropped_area_, dropped_Match_factor, dropped_formula, dropped_area_area)),
                                         columns=["RT", "compound name", "area", "% area", "Match factor", "formula", "area/area"])
    else:
        print(f"Eliminated rows in input: {dropped_rows}")
        print("Remember, to find the compounds in the input file you need to add +1 to the previous numbers.\n")

    # controllo se esiste già un file di Dropped_compounds
    if os.path.isfile('Dropped_compounds.xlsx'):
        print("File \"Dropped_compounds.xlsx\" alredy exists in this directory.\nIf you want to obtain a new one, delete it.")
    else:
        print("File \"Dropped_compounds.xlsx\" will be saved in this directory.")
        # converto il dataframe in un file excel
        dropped_compounds.to_excel("Dropped_compounds.xlsx")

    #creo il nuovo database con le righe ridotte
    new = input.drop(dropped_rows)

    #creo una lista di tutti i composti con la classe di appartenenza
    print("\nI begin to classify the input compounds based on the database.")
    for i in tqdm(new["compound name"]):  # leggo i composti dall'input
        # aggiungo il nome del i composto nella lista dei composti
        compounds.append(i)
        # controllo se il composto i è presente nel database, se si aggiungo la classe conosciuta
        if i in database["Compound"].to_numpy():
            class_compounds.append(
                database["Class"][database[database["Compound"] == i].index[0]])
        else:  # se no, classifica il composto come sconosciuto
            class_compounds.append("Unknown")

    rt = new["RT"]
    area = new["area"]
    area_ = new["% area"]
    Match_factor = new["Match factor"]
    formula = new["formula"]
    area_area = new["area/area"]

    classified_compound = pd.DataFrame(list(zip(rt, compounds, class_compounds, area, area_, Match_factor, formula, area_area)),
                          columns=["RT", "compound name", "Class", "area", "% area", "Match factor", "formula", "area/area"])  # creo il dataframe con i dati classificati

    print("Report of your input after the classification:")
    # print della descrizione dei composti classificati
    print(classified_compound["Class"].value_counts())

    if os.path.isfile('Classified_compounds.xlsx'):  # controllo se esiste già un file di classified_compound
        print("\nFile \"Classified_compounds.xlsx\" alredy exists in this directory.\nIf you want to obtain a new one, delete it.")
    else:
        print("\nFile \"Classified_compounds.xlsx\" will be saved in this directory.")
        # converto il dataframe in un file excel
        classified_compound.to_excel("Classified_compounds.xlsx")


    print("\nSee you next time ;)")
