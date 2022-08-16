// Note: this query was executed after the chembl_screened_compounds.cypher query was executed.

LOAD CSV WITH HEADERS 
FROM 'https://storage.googleapis.com/testgqin/clean_pubchem_screened_compounds.csv' AS line

MATCH 
    (subject:Drug {Name: toUpper(line.subject_name)}),
    (object:Gene {Name: toUpper(line.object_name)})
SET subject.Pubchem_ID = toInteger(line.subject_id),
    object.NCBI_ID = toInteger(line.object_id)

;