CREATE CONSTRAINT FOR (g:Gene) REQUIRE g.Symbol IS UNIQUE;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS
FROM 'https://storage.googleapis.com/multiomics_provider_kp_data/BigGIM/Signaling/gene_gene_nodes.csv' AS row

MERGE (subject:Gene {Symbol: row.subject_symbol})
ON MATCH 
    //add properties to existing ones
ON CREATE
    SET subject.ID = row.subject_id,
        subject.Prefixes = row.subject_id_prefixes

MERGE (object:Gene {Symbol: row.object_symbol})
ON MATCH    
    //add properties to existing ones
ON CREATE
    SET object.ID = row.object_id,
        object.Prefixes = row.object_id_prefixes

CREATE (subject)-[p:ASSOCIATED_WITH]->(object)
SET p.Predicate = row.predicate,
    p.Publications = row.ASSOCIATION_Publications

;

// The goal would be to do something like:
    // CREATE (subject)-[p:PHYSICALLY_INTERACTS_WITH]->(object)
    // WHERE row.predicate = 'physically interacts with'
    // SET p.Publications = row.ASSOCIATION_Publications

    // CREATE (subject)-[p:INCREASES_ACTIVITY_OF]->(object)
    // WHERE row.predicate = 'increases activity of'
    // SET p.Publications = row.ASSOCIATION_Publications

    // CREATE (subject)-[p:AFFECTS_EXPRESSION_OF]->(object)
    // WHERE row.predicate = 'affects expression of'
    // SET p.Publications = row.ASSOCIATION_Publications