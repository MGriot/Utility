# How to use this script

## Import the necessary libraries

```Python
import pandas as pd
import numpy as np
import os.path
from tqdm import tqdm
```

## Load the `Database.xlsx` file where the compoun and class are stored

```Python
database = pd.read_excel("Database.xlsx")
database #this is necessary if you want to see the database after the import
```

## Load the `Input.xlsx` file where the compounds that are necessary to be classified.

```Python
input = pd.read_excel("Input.xlsx")
input #this is necessary if you want to see the input after the import
```

## The function for classify the input compunds

```Python
def get_class(database, input):
    #
    # Funzione per classificare in automatico i dati in base ai parametri contenuti nel database
    #
    # database: database su cui si basa la classificazione
    # input: dati di output
    # output: dati classificaticompound name
    #

    #liste vuote usate nella classificazione
    compounds = []  # lista di tutti i composti
    class_compounds = []  # lista di tutte le classi dei composti

    
    a=0
    no_match_value=[]
    errate_formulae=[]
    
    #parte per eliminare le righe
    for i in input["compound name"]:
        #removing compound with errate number for area and match factor
        if input["area"][a]<1e5 or input["Match factor"][a]<70:
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
        a+=1     
    #elimino tutte le righe che non passano i test per i valori e la formula
    dropped_rows = np.unique(no_match_value + errate_formulae)
    #creo il nuovo database con le righe ridotte    
    new=input.drop(dropped_rows)
        
    for i in tqdm(new["compound name"]):  # leggo i composti dall'input
        # aggiungo il nome del i composto nella lista dei composti
        compounds.append(i)
        # controllo se il composto i è presente nel database, se si aggiungo la classe conosciuta
        if i in database["Compound"].to_numpy():
            class_compounds.append(
                database["Class"][database[database["Compound"] == i].index[0]])
        else:  # se no, classifica il composto come sconosciuto
            class_compounds.append("Unknown")
    
    RT=new["RT"]
    area=new["area"]
    area_=new["% area"]
    Match_factor=new["Match factor"]
    formula=new["formula"]
    area_area=new["area/area"]
    
    output = pd.DataFrame(list(zip(RT, compounds, class_compounds, area, area_, Match_factor, formula, area_area)),
                          columns=["RT", "compound name", "Class", "area", "% area", "Match factor", "formula", "area/area"])  # creo il dataframe con i dati classificati

    print("Report of your input:")
    # print della descrizione dei composti classificati
    print(output["Class"].value_counts())
    print(f"Eliminated rows in input: {dropped_rows}")
    print("Remember, to find the compounds in the input file you need to add +1 to the previous numbers.\n")

    if os.path.isfile('Output.xlsx'):  # controllo se esiste già un file di output
        print("File \"Output.xlsx\" alredy exists in this directory.\nIf you want to obtain a new one, delete it.")
    else:
        print("File \"Output.xlsx\" will be saved in this directory.")
        # converto il dataframe in un file excel
        output.to_excel("Output.xlsx")

    print("\nSee you next time ;)")

```

### Run the function

```Python
get_class(database=database, input=input)
```
