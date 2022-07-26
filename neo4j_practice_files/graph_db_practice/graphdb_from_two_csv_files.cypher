// July 20, 2022
// Creating a graph database from two csv files provided by Dr. Qin
// 'Drug' and 'Gene' nodes, with the relationship 'Targets' 
// Each file contains 'Drugs', 'Genes', and relationship properties.
// The goal is to avoid duplicate nodes from each file and to
// attach the properties from each file to the nodes and relationships. 


CREATE CONSTRAINT FOR (g:Gene) REQUIRE g.Name IS UNIQUE;
CREATE CONSTRAINT FOR (d:Drug) REQUIRE d.Name IS UNIQUE;


USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM  
'file:///Table_DrugResponse_KP_v2021.11.21_rm_redundance_v2022.2.25.csv' AS line

MERGE (drug:Drug {Name: line.Object})
ON CREATE SET
    drug.ID = line.Object_id,
    drug.Category = line.Object_Category

MERGE (gene:Gene {Name: line.Subject})
ON CREATE SET
    gene.Ensembl_gene_ID = line.Subject_Ensembl_gene_ID,
    gene.NCBI_Gene_ID = line.Subject_NCBI_Gene_ID,
    gene.Approved_symbol = line.Subject_Approved_symbol,
    gene.Category = line.Subject_Category

// Problem: all relationships are being created on ONE drug. All the genes
//          are correct, but only the drug on the first row in the csv file
//          is being connected to all the genes. But, the other drugs are 
//          still being created, just not connecting to the relationships... hmmmmm why?
CREATE (drug)-[t:TARGETS]->(gene) 
SET 
    t.Predicate = line.Predicate,
    t.Subject_Modifier = line.Edge_attribute_Subject_Modifier,
    t.Object_Modifier = line.Edge_attribute_Object_Modifier,
    t.Method = line.Edge_attribute_method,
    t.Pvalue = line.Edge_attribute_Pvalue,
    t.Evidence_type = line.Edge_attribute_evidence_type,
    t.Evidence_value = line.Edge_attribute_evidence_value,
    t.Sample_size = line.Edge_attribute_sample_size,
    t.Sample_origin = line.Edge_attribute_sample_orign,
    t.MONDO_ID = line.Edge_attribute_MONDO_ID,
    t.DatabResource = line.Edge_attribute_DataResource,
    t.Publication = line.Edge_attribute_Publication,
    t.Provider = line.Edge_attribute_Provider

;


USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM 
'file:///CTDMB_formated.csv' AS line
WITH line where line.Name is not null

MERGE (gene:Gene {Name: line.Target})

MERGE (drug:Drug {Name: line.Drug})

MERGE (drug)-[t:Targets]->(gene)
SET t.Disease = line.Disease,
    t.Reference = line.Reference,
    t.Cumulator = line.Cumulator,
    t.Stage = line.Stage,
    gene.Date = line.Date

;

    // SPLIT(line.Date, '.') AS date 
    // gene.Year = toInteger(date[0]),
    // gene.Month = toInteger(date[1]),
    // gene.Day = toInteger(date[2])
    