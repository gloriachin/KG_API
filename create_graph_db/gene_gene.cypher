// This file is in the Google server graph database!

CREATE INDEX ON :Gene(NCBI_ID);
CREATE INDEX ON :Gene(Symbol);

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/14clean_gene_gene.csv' AS row
MERGE (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes), Predicate: toUpper(row.predicate)})
MERGE (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes), Predicate: toUpper(row.predicate)})
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/14clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = 'PHYSICALLY INTERACTS WITH' AND object.Predicate = 'PHYSICALLY INTERACTS WITH'
MERGE (subject)-[p:PHYSICALLY_INTERACTS_WITH {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/14clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = 'INCREASES ACTIVITY OF' AND object.Predicate = 'INCREASES ACTIVITY OF'
MERGE (subject)-[p:INCREASES_ACTIVITY_OF {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/14clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = 'AFFECTS EXPRESSION OF' AND object.Predicate = 'AFFECTS EXPRESSION OF'
MERGE (subject)-[p:AFFECTS_EXPRESSION_OF {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;