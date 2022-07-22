// July 22, 2022
// Creating a graph database from the csv file provided by Emily Zhang.
// Drug and Gene nodes and Targets relationship between them. 

CREATE CONSTRAINT FOR (g:Gene) REQUIRE g.Name IS UNIQUE;
CREATE CONSTRAINT FOR (d:Drug) REQUIRE d.Name IS UNIQUE;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS 
FROM 'file:///no_nulls_final_screened_compounds' AS line

MERGE (drug:Drug {Name: line.DRUG_NAME})
SET drug.Synonyms = line.Synonyms

MERGE (gene:Gene {Name: line.Target})

CREATE (drug)-[t:TARGETS]->(gene)
SET t.Disease = line.Disease,
    t.Reference = line.Reference,
    t.Date = line.Date,
    t.Cumulator = line.Cumulator,
    t.Stage = line.Stage,
    t.Action = line.Action,
    t. pubchem_id = line.pubchem_id,
    t.chembl_id = line.chembl_id
;