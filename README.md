This project falls under the scope of text classification and aims at both identifying query types (intents) and performing slot filling.

Databases used for this study are stored in the foldr "query_dbs".

Python code can be found in the folder "notebooks":
    - "query_types_classif" notebook contains the LSTM model used to identofy query types; 
    - "random_fields" notebook corresponds to the CRF model used to perform slot filling.
    
Models are saved in the folder "models" and graphs in the folder "graphs". The folder "utils" contains the different functions we created and used. 
