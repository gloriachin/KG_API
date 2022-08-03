#import libraries
import math
import pandas as pd
import numpy as np
import requests

class drug_disease_format:
    #Create empty final dataframe
    final_csv = pd.DataFrame()
    
    #Create lists (each of these will be a column of the dataframe)
    subject_ids = []
    subject_category = []
    subject_id_prefixes = []

    object_ids = []
    object_category = []
    object_id_prefixes = []

    predicates = []

    association_subject = []
    association_object = []
    association_predicate = []
    association_knowledge = []
    association_provider = []
    association_approval = []

    #Constructor
    def __init__(self, list):
        self.drug_list = list
    
    #Mondo disease ID API function
    def get_mondo_id(self, disease):
        mondo_url = 'https://ebi.ac.uk/ols/api/search'
            
        query = str(disease)
        parameters = {'q':query,
                    'ontology':'mondo', 
                    'fieldList':'obo_id'}
    
        mondo_data = requests.get(url = mondo_url, params = parameters)
        mondo_data = mondo_data.json()
    
        if mondo_data['response']['docs'] == []:
            mondo_id = math.nan
        else:
            mondo_id = mondo_data['response']['docs'][0]['obo_id']
        
        return mondo_id

    
    #Subject columns method
    def subject_columns(self, prefix):
        if prefix == 'Pubchem':
            self.subject_ids = self.drug_list['pubchem_id'].values.tolist()
            self.subject_id_prefixes = ['Pubchem.compound'] * len(self.drug_list)
        
        if prefix == 'Chembl':
            self.subject_ids = self.drug_list['chembl_id'].values.tolist()
            self.subject_id_prefixes = ['Chembl.compound'] * len(self.drug_list)

        self.subject_category = ['drug'] * len(self.drug_list)

    #Object columns method
    def object_columns(self):
        disease_list = self.drug_list['Disease'].values.tolist()
        unique_diseases = np.unique(disease_list)
        self.object_ids = ['N/A'] * len(self.drug_list)

        for i in range(len(unique_diseases)):
            object_id = self.get_mondo_id(unique_diseases[i])

            for j in range(len(self.drug_list)):
                if unique_diseases[i] == disease_list[j]:
                    self.object_ids[j] = object_id

        self.object_category = ['disease'] * len(self.drug_list)
        self.object_id_prefixes = ['mondo.disease'] * len(self.drug_list)
    
    #Predicate and associations columns method
    def predicate_association_columns(self):
        self.predicates = ['Approved to treat'] * len(self.drug_list)

        self.association_subject = self.subject_ids
        self.association_object = self.object_ids
        self.association_predicate = self.predicates
        self.association_knowledge = self.drug_list['Reference'].values.tolist()
        self.association_provider = ['multiomics-BigGIM'] * len(self.drug_list)
        self.association_approval = self.drug_list['Stage'].values.tolist()

    #Create final csv
    def add_columns(self):
        self.final_csv = self.final_csv.assign(Subject_id = self.subject_ids)
        self.final_csv = self.final_csv.assign(Subject_category = self.subject_category)
        self.final_csv = self.final_csv.assign(Subject_id_prefixes = self.subject_id_prefixes)

        self.final_csv = self.final_csv.assign(Object_id = self.object_ids)
        self.final_csv = self.final_csv.assign(Object_category = self.object_category)
        self.final_csv = self.final_csv.assign(Object_id_prefixes = self.object_id_prefixes) 

        self.final_csv = self.final_csv.assign(predicates = self.predicates)

        self.final_csv = self.final_csv.assign(ASSOCIATION_Subject = self.association_subject)
        self.final_csv = self.final_csv.assign(ASSOCIATION_Object = self.association_object)
        self.final_csv = self.final_csv.assign(ASSOCIATION_Predicate = self.association_predicate)
        self.final_csv = self.final_csv.assign(ASSOCIATION_Knowledge_source = self.association_knowledge)
        self.final_csv = self.final_csv.assign(ASSOCIATION_Provided_by = self.association_provider)
        self.final_csv = self.final_csv.assign(ASSOCIATION_FDA_approval_status = self.association_approval)

        self.final_csv = self.final_csv.fillna('N/A')

        self.final_csv.to_csv('chembl_drug_to_disease_formatted.csv', index = False)
