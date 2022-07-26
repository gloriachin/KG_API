// July 13, 2022
// First attempt creating a graph database using the test.csv file provided by Dr. Qin
// Creating 'Subject' and 'Object' nodes, and a 'Predicate' relationship between them


// constraints with 'assert'
//CREATE CONSTRAINT ON (o:Object) ASSERT o.name IS UNIQUE;
//CREATE CONSTRAINT ON (s:Subject) ASSERT s.name IS UNIQUE;

// constraints with 'require'
//CREATE CONSTRAINT o_unique_name FOR (o:Object) REQUIRE o.name IS UNIQUE
//CREATE CONSTRAINT s_unique_name FOR (s:Subject) REQUIRE s.name IS UNIQUE

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 
'file:///test.csv' AS line 
WITH line

MERGE (subject:Subject {name: line.Subject, Ensembl_gene_ID: line.Subject_Ensembl_gene_ID, NCBI_Gene_ID: line.Subject_NCBI_Gene_ID, Approved_symbol: line.Subject_Approved_symbol, Category: line.Subject_Category})

CREATE (object:Object {name: line.Object_name, id: line.Object_id, Category: line.Object_Category})

MERGE (subject)-[p:Predicate]->(object)

SET p.type = line.Predicate,
    p.Subject_Modifier = line.Edge_attribute_Subject_Modifier,
    p.Object_Modifier = line.Edge_attribute_Object_Modifier,
    p.method = line.Edge_attribute_method,
    p.Pvalue = line.Edge_attribute_Pvalue,
    p.evidence_type = line.Edge_attribute_evidence_type,
    p.evidence_value = line.Edge_attribute_evidence_value,
    p.sample_size = line.Edge_attribute_sample_size,
    p.sample_origin = line.Edge_attribute_sample_orign,
    p.MONDO_ID = line.Edge_attribute_MONDO_ID,
    p.DatabResource = line.Edge_attribute_DataResource,
    p.publication = line.Edge_attribute_Publication,
    p.provider = line.Edge_attribute_Provider

;