LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/cleaned_edges_test.csv' AS row

MERGE (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes), Category: toUpper(row.subject_category)})

MERGE (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes), Category: toUpper(row.object_category)})

CREATE (subject)-[p:PHYSICALLY_INTERACTS_WITH]->(object)
SET p.Publications = toUpper(row.ASSOCIATION_Publications)

;