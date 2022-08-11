LOAD CSV WITH HEADERS 
FROM 'https://storage.googleapis.com/testgqin/clean_chembl_screened_compounds.csv' AS row

MERGE (subject:Drug {Name: toUpper(row.subject_name), Synonym: toUpper(row.subject_synonym), Category: toUpper(row.subject_category), Prefixes: toUpper(row.subject_id_prefixes)})
SET subject.Chembl_ID = row.subject_id

MERGE (object:Gene {Name: toUpper(row.object_name), Category: toUpper(row.object_category), Symbol: toUpper(row.object_symbol), Prefixes: toUpper(row.object_id_prefixes)})
SET object.Chembl_ID = toInteger(row.object_id)

CREATE (subject)-[p:TARGETS]->(object)
SET p.Knowledge_Source = toUpper(row.ASSOCIATION_Knowledge_source),
    p.Provided_By = toUpper(row.ASSOCIATION_Provided_by)

;