// This file is in the Google server graph database!

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/clean_pubchem_drug_to_disease.csv' AS row

MERGE (subject:Drug {Pubchem_ID: toInteger(row.Subject_id), Category: toUpper(row.Subject_category), Prefixes: toUpper(row.Subject_id_prefixes)})

MERGE (object:Disease {Pubchem_ID: row.Object_id, Category: toUpper(row.Object_category), Prefixes: toUpper(row.Object_id_prefixes)})

CREATE (subject)-[r:APPROVED_TO_TREAT]->(object)
SET r.Knowledge_Source = toUpper(row.ASSOCIATION_Knowledge_source),
    r.Provided_by = toUpper(row.ASSOCIATION_Provided_by),
    r.FDA_approval_status = toUpper(row.ASSOCIATION_FDA_approval_status)

;