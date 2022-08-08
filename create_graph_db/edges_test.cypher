// note to self: this file is good to go


CREATE CONSTRAINT gene_constraint FOR (g:Gene) REQUIRE g.Symbol IS UNIQUE;

LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/testgqin/clean_edges_test.csv' AS row

MERGE (subject:Gene {Symbol: toUpper(row.subject_symbol), ID: toInteger(row.subject_id), Prefixes: toUpper(row.subject_id_prefixes), Category: toUpper(row.subject_category)})

MERGE (object:Gene {Symbol: toUpper(row.object_symbol), ID: toInteger(row.object_id), Prefixes: toUpper(row.object_id_prefixes), Category: toUpper(row.object_category)})

CREATE (subject)-[p:PHYSICALLY_INTERACTS_WITH]->(object)
SET p.Publications = toUpper(row.ASSOCIATION_Publications)

;



// MERGE (subject:Gene {Symbol: toUpper(row.subject_symbol)})
// SET subject.ID = toInteger(row.subject_id),
    // subject.Prefixes = toUpper(row.subject_id_prefixes),
    // subject.Category = toUpper(row.subject_category)

// MERGE (object:Gene {Symbol: toUpper(row.object_symbol)})
// SET object.ID = toInteger(row.object_id),
    // object.Prefixes = toUpper(row.object_id_prefixes),
    // object.Category = toUpper(row.object_category)