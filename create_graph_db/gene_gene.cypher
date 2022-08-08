LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/clean_gene_gene.csv' AS row
MERGE (subject:Gene {Symbol: toUpper(row.subject_symbol), ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)})
SET subject.Predicate = toUpper(row.predicate)
MERGE (object:Gene {Symbol: toUpper(row.object_symbol), ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
SET object.Predicate = toUpper(row.predicate)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/clean_gene_gene.csv' AS row
MATCH 
    (subject:Gene {Symbol: toUpper(row.subject_symbol), ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)}),
    (object:Gene {Symbol: toUpper(row.object_symbol), ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = 'PHYSICALLY INTERACTS WITH' AND object.Predicate = 'PHYSICALLY INTERACTS WITH'
CREATE (subject)-[p:PHYSICALLY_INTERACTS_WITH]->(object)
SET p.Publications = toUpper(row.ASSOCIATION_Publications)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/clean_gene_gene.csv' AS row
MATCH 
    (subject:Gene {Symbol: toUpper(row.subject_symbol), ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)}),
    (object:Gene {Symbol: toUpper(row.object_symbol), ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = 'INCREASES ACTIVITY OF' AND object.Predicate = 'INCREASES ACTIVITY OF'
CREATE (subject)-[p:INCREASES_ACTIVITY_OF]->(object)
SET p.Publications = toUpper(row.ASSOCIATION_Publications)
;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/clean_gene_gene.csv' AS row
MATCH 
    (subject:Gene {Symbol: toUpper(row.subject_symbol), ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes)}),
    (object:Gene {Symbol: toUpper(row.object_symbol), ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes)})
WHERE subject.Predicate = 'AFFECTS EXPRESSION OF' AND object.Predicate = 'AFFECTS EXPRESSION OF'
CREATE (subject)-[p:AFFECTS_EXPRESSION_OF]->(object)
SET p.Publications = toUpper(row.ASSOCIATION_Publications)
;




// MERGE (subject:Gene {Symbol: toUpper(row.subject_symbol)})
// ON CREATE
    // SET subject.ID = toInteger(row.subject_id),
        // subject.Prefixes = toUpper(row.subject_id_prefixes),
        // subject.Predicate = toUpper(row.predicate)
// ON MATCH 
    // add properties to existing ones


// MERGE (object:Gene {Symbol: toUpper(row.object_symbol)})
// ON CREATE
    // SET object.ID = toInteger(row.object_id),
        // object.Prefixes = toUpper(row.object_id_prefixes),
        // object.Predicate = toUpper(row.predicate)
// ON MATCH    
    // add properties to existing ones


// CREATE (subject)-[p:PHYSICALLY_INTERACTS_WITH]->(object)
// WHERE toUpper(subject.Predicate) = 'PHYSICALLY INTERACTS WITH'
// SET p.Publications = toUpper(row.ASSOCIATION_Publications)

// CREATE (subject)-[p:INCREASES_ACTIVITY_OF]->(object)
// WHERE toUpper(subject.Predicate) = 'INCREASES ACTIVITY OF'
// SET p.Publications = toUpper(row.ASSOCIATION_Publications)

// CREATE (subject)-[p:AFFECTS_EXPRESSION_OF]->(object)
// WHERE toUpper(object.Predicate) = 'AFFECTS EXPRESSION OF'
// SET p.Publications = toUpper(row.ASSOCIATION_Publications)