CREATE CONSTRAINT FOR (d:Drug) REQUIRE d.Name IS UNIQUE;
CREATE CONSTRAINT FOR (g:Gene) REQUIRE g.Name IS UNIQUE;

//USING PERIODIC COMMIT
LOAD CSV WITH HEADERS 
FROM 'file:///clean_chembl_screened_compounds.csv' AS row

MERGE (subject:Drug {Name: row.subject_name})
SET subject.Chembl_ID = row.subject_id,
    subject.Synonym = row.subject_synonym,
    subject.Category = row.subject_category,
    subject.ID_Prefixes = row.subject_id_prefixes

MERGE (object:Gene {Name: row.object_name})
// SET object.Chembl_ID = row.object_id,
//     object.Category = row.object_category,
//     object.Symbol = row.object_symbol,
//     object.ID_Prefixes = row.object_id_prefixes
// ^ this will erase all of the properties already set for genes and overwrite them
// I need to figure out how to add this property in addition to the already set ones !!

CREATE (subject)-[p:TARGETS]->(object)
SET p.Knowledge_Source = row.ASSOCIATION_Knowledge_source,
    p.Provided_By = row.ASSOCIATION_Provided_by

;

//USING PERIODIC COMMIT 
LOAD CSV WITH HEADERS 
FROM 'file:///clean_pubchem_screened_compounds.csv' AS line

MATCH (subject:Drug {Name: line.subject_name})
// SET subject.Pubchem_ID = line.subject_id
// ^ this will erase all of the properties already set and overwrite them with just this one property.
// I need to figure out how to add this property in addition to the already set ones !!

MATCH (object:Gene {Name: line.object_name})
// SET object.Pubchem_ID = line.oject_id
// ^ this will erase all of the properties already set and overwrite them with just this one property.
// I need to figure out how to add this property in addition to the already set ones !!