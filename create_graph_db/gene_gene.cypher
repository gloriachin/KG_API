// This file is in the Google server graph database!

CREATE INDEX ON :Gene(NCBI_ID);
CREATE INDEX ON :Gene(Symbol);

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MERGE (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes), Predicate: toUpper(row.predicate)})
MERGE (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes), Predicate: toUpper(row.predicate)})
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = 'PHYSICALLY INTERACTS WITH' AND object.Predicate = 'PHYSICALLY INTERACTS WITH'
MERGE (subject)-[p:PHYSICALLY_INTERACTS_WITH {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = 'INCREASES ACTIVITY OF' AND object.Predicate = 'INCREASES ACTIVITY OF'
MERGE (subject)-[p:INCREASES_ACTIVITY_OF {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = 'AFFECTS EXPRESSION OF' AND object.Predicate = 'AFFECTS EXPRESSION OF'
MERGE (subject)-[p:AFFECTS_EXPRESSION_OF {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = "AFFECTS MOLECULAR MODIFICATION OF" AND object.Predicate = "AFFECTS MOLECULAR MODIFICATION OF"
MERGE (subject)-[p:AFFECTS_MOLECULAR_MODIFICATION_OF {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = "DECREASES ABUNDANCE OF" AND object.Predicate = "DECREASES ABUNDANCE OF"
MERGE (subject)-[p:DECREASES_ABUNDANCE_OF {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = "INCREASES ABUNDANCE OF" AND object.Predicate = "INCREASES ABUNDANCE OF"
MERGE (subject)-[p:INCREASES_ABUNDANCE_OF {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = "POSITIVELY REGULATES" AND object.Predicate = "POSITIVELY REGULATES"
MERGE (subject)-[p:POSITIVELY_REGULATES {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = "NEGATIVELY REGULATES" AND object.Predicate = "NEGATIVELY REGULATES"
MERGE (subject)-[p:NEGATIVELY_REGULATES {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol)})
WHERE subject.Predicate = "BINDS" AND object.Predicate = "BINDS"
MERGE (subject)-[p:BINDS {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = "DECREASES AMOUNT OR ACTIVITY OF" AND object.Predicate = "DECREASES AMOUNT OR ACTIVITY OF"
MERGE (subject)-[p:DECREASES_AMOUNT_OR_ACTIVITY_OF {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = "DECREASES EXPRESSION OF" AND object.Predicate = "DECREASES EXPRESSION OF"
MERGE (subject)-[p:DECREASES_EXPRESSION_OF {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = "INCREASES EXPRESSION OF" AND object.Predicate = "INCREASES EXPRESSION OF"
MERGE (subject)-[p:INCREASES_EXPRESSION_OF {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = "DECREASES ACTIVITY OF" AND object.Predicate = "DECREASES ACTIVITY OF"
MERGE (subject)-[p:DECREASES_ACTIVITY_OF {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = "NEGATIVELY CORRELATES WITH" AND object.Predicate = "NEGATIVELY CORRELATES WITH"
MERGE (subject)-[p:NEGATIVELY_CORRELATES_WITH {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = "POSITIVELY CORRELATED WITH" AND object.Predicate = "POSITIVELY CORRELATED WITH"
MERGE (subject)-[p:POSITIVELY_CORRELATED_WITH {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/gene_gene_files/1clean_gene_gene.csv' AS row
MATCH (subject:Gene {Symbol: toUpper(row.subject_symbol), NCBI_ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
MATCH (object:Gene {Symbol: toUpper(row.object_symbol), NCBI_ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = "AFFECTS" AND object.Predicate = "AFFECTS"
MERGE (subject)-[p:AFFECTS {Publications: toUpper(row.ASSOCIATION_Publications)}]->(object)
;