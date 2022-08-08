// note to self: this file is good to go


CREATE CONSTRAINT drug_constraint FOR (d:Drug) REQUIRE d.Name IS UNIQUE;
CREATE CONSTRAINT gene_constraint FOR (g:Gene) REQUIRE g.Name IS UNIQUE;

LOAD CSV WITH HEADERS 
FROM 'https://storage.googleapis.com/testgqin/clean_chembl_screened_compounds.csv' AS row

MERGE (subject:Drug {Name: toUpper(row.subject_name), Synonym: toUpper(row.subject_synonym), Category: toUpper(row.subject_category), Prefixes: toUpper(row.subject_id_prefixes)})
SET subject.Chembl_ID = toInteger(row.subject_id)

MERGE (object:Gene {Name: toUpper(row.object_name), Category: toUpper(row.object_category), Symbol: toUpper(row.object_symbol), Prefixes: toUpper(row.object_id_prefixes)})
SET object.Chembl_ID = toInteger(row.object_id)

CREATE (subject)-[p:TARGETS]->(object)
SET p.Knowledge_Source = toUpper(row.ASSOCIATION_Knowledge_source),
    p.Provided_By = toUpper(row.ASSOCIATION_Provided_by)

;


LOAD CSV WITH HEADERS 
FROM 'https://storage.googleapis.com/testgqin/clean_pubchem_screened_compounds.csv' AS line

MATCH (subject:Drug {Name: line.subject_name})
SET subject.Pubchem_ID = toInteger(line.subject_id)

MATCH (object:Gene {Name: line.object_name})
SET object.Pubchem_ID = toInteger(line.oject_id)

;



// MERGE (subject:Drug {Name: toUpper(row.subject_name)})
// ON CREATE
//     SET subject.Chembl_ID = toInteger(row.subject_id),
//         subject.Synonym = toUpper(row.subject_synonym),
//         subject.Category = toUpper(row.subject_category),
//         subject.Prefixes = toUpper(row.subject_id_prefixes)
// ON MATCH
//     // add properties to existing ones


// MERGE (object:Gene {Name: toUpper(row.object_name)})
// ON CREATE
    // SET object.Chembl_ID = toInteger(row.object_id),
        // object.Category = toUpper(row.object_category),
        // object.Symbol = toUpper(row.object_symbol),
        // object.Prefixes = toUpper(row.object_id_prefixes)
// ON MATCH 
    // add properties to existing ones