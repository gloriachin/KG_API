// This file is in the Google server graph database!

LOAD CSV WITH HEADERS 
FROM 'https://storage.googleapis.com/testgqin/clean_chembl_drug_to_disease.csv' AS row

MERGE (subject:Drug {Chembl_ID: toInteger(row.Subject_id), Category: toUpper(row.Subject_category), Prefixes: toUpper(row.Subject_id_prefixes)})

MERGE (object:Disease {Chembl_ID: row.Object_id, Category: toUpper(row.Object_category), Prefixes: toUpper(row.Object_id_prefixes)})

CREATE (subject)-[r:APPROVED_TO_TREAT]->(object)
SET r.Knowledge_Source = row.ASSOCIATION_Knowledge_Source,
    r.Provided_by = row.ASSOCIATION_Provided_by,
    r.FDA_approval_status = row.ASSOCIATION_FDA_approval_status

;


// adding Name property to these Drug and Disease nodes
LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/with_names_chembl_drug_to_disease.csv' AS row

WITH row

MATCH (subject: Drug {Chembl_ID: toInteger(row.Subject_id)})
SET subject.Name = toUpper(row.Subject_name)

WITH row

MATCH (object: Disease {Chembl_ID: row.Object_id})
SET object.Name = toUpper(row.Object_name)

;