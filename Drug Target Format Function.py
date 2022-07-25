#Import libraries
import pandas as pd
import math

class KGI_Formatting:
    #Import data
    gene_list = pd.read_csv('C:/Users/emily/OneDrive/Documents/Drug ID/gene_data.tsv', sep = '\t') #this file contains NCBI gene names, ids, and more
    final_csv = pd.DataFrame()

    #Create lists (each of these will be a column of the dataframe)
    subject_ids = []
    subject_name = []
    subject_synonym = []
    subject_categories = []
    subject_id_prefixes = []

    object_ids = []
    object_categories = []
    object_symbol = []
    object_names = []

    predicates = []

    association_subject = []
    association_object = []
    association_predicate = []
    association_knowledge = []
    association_provider = []

    #Constructor
    def __init__(self, list):
        self.drug_list = list

    #Subject columns method
    def subject(self, prefix):
        #Fill nulls with N/A
        self.drug_list.fillna('N/A', inplace = True)

        #Assign either pubchem or chembl ids/prefix to subject_ids and subject_id_prefixes
        if prefix == 'Pubchem':
            self.subject_ids = self.drug_list['pubchem_id'].values.tolist()
            self.subject_id_prefixes = ['Pubchem.compound'] * len(self.drug_list)

        if prefix == 'Chembl':
            self.subject_ids = self.drug_list['chembl_id'].values.tolist()
            self.subject_id_prefixes = ['Chembl.compound'] * len(self.drug_list)

        #Fill subject lists with ready data from input dataframe
        self.subject_name = self.drug_list['DRUG_NAME'].values.tolist()
        self.subject_synonym = self.drug_list['synonyms'].values.tolist()
        subject_approved = self.drug_list['Stage'].values.tolist()

        #Assign categories based on stage
        for i in range(len(subject_approved)):
            if subject_approved[i] == 'Approved':
                self.subject_categories.append('Drug')
            else:
                self.subject_categories.append('Small molecule')

    #object columns method
    def object(self):
        def binary_search(list, gene_name):
            left_index = 0
            right_index = len(list) - 1
            mid = 0
            while (left_index <= right_index):
                mid = (right_index + left_index) // 2
                if str(list[mid]) < str(gene_name):
                    left_index = mid + 1
                elif str(list[mid]) > gene_name:
                    right_index = mid - 1
                else:
                    return mid
            return -1

        #Fill object lists with ready data from input dataframe
        self.object_symbols = self.drug_list['Target'].values.tolist()
        self.object_categories = ['Gene'] * len(self.drug_list)
        self.object_id_prefixes = ['NCBI.gene'] * len(self.drug_list)
        self.association_knowledge = self.drug_list['Reference'].values.tolist()

        #Sort dataframes alphabetically by name column
        self.drug_list = self.drug_list.sort_values('Target')
        self.gene_list = self.gene_list.sort_values('Approved_symbol')
        target_list = self.drug_list['Target'].values.tolist()

        #Make gene list
        gene_symbols = self.gene_list['Approved_symbol'].values.tolist()

        #Match gene symbol from gene and input dataframes and find gene name and NCBI ID
        for i in range(len(self.object_symbols)):
            name_index = binary_search(gene_symbols, target_list[i])
            if (name_index >= 0):
                object_id = self.gene_list.iloc[name_index, 10]
            else:
                object_id = 'N/A'
            self.object_ids.append(object_id)

        for i in range(len(self.drug_list)):
            name_index = binary_search(gene_symbols, target_list[i])
            if (name_index >= 0):
                object_name = self.gene_list.iloc[name_index, 2]
            else:
                object_name = 'N/A'
            self.object_names.append(object_name)
    
        #Add sorted object lists to drug_list
        self.drug_list = self.drug_list.assign(object_id = self.object_ids)
        self.drug_list = self.drug_list.assign(object_names = self.object_names)
        
        #Sort dataframe back to original format (matching how object_ids and object_names are sorted with other columns)
        self.drug_list = self.drug_list.sort_values('id')
        
        #Assign correctly sorted values to lists
        self.object_ids = self.drug_list['object_id']
        self.object_names = self.drug_list['object_names']

    #Predicate and association columns method
    def association(self):
        self.predicates = ['Targets'] * len(self.drug_list)

        self.association_subject = self.subject_name
        self.association_object = self.object_names
        self.association_predicate = self.predicates
        
        self.association_provider = ['multiomics-BigGIM'] * len(self.drug_list)

    #creating the final csv
    def add_columns(self):

        #assign columns to dataframe
        self.final_csv = self.final_csv.assign(Subject_id = self.subject_ids)
        self.final_csv = self.final_csv.assign(Subject_name = self.subject_name)
        self.final_csv = self.final_csv.assign(Subject_synonym = self.subject_synonym)
        self.final_csv = self.final_csv.assign(Subject_category = self.subject_categories)
        self.final_csv = self.final_csv.assign(Subject_id_prefixes = self.subject_id_prefixes)

        self.final_csv = self.final_csv.assign(Object_id = self.object_ids)
        self.final_csv = self.final_csv.assign(Object_category = self.object_categories)
        self.final_csv = self.final_csv.assign(Object_id_prefixes = self.object_id_prefixes)
        self.final_csv = self.final_csv.assign(Object_symbol = self.object_symbols)
        self.final_csv = self.final_csv.assign(Object_name = self.object_names)

        self.final_csv = self.final_csv.assign(Predicates = self.predicates)

        self.final_csv = self.final_csv.assign(ASSOCIATION_Subject = self.association_subject)
        self.final_csv = self.final_csv.assign(ASSOCIATION_Object = self.association_object)
        self.final_csv = self.final_csv.assign(ASSOCIATION_Predicate = self.association_predicate)
        self.final_csv = self.final_csv.assign(ASSOCIATION_Knowledge20source = self.association_knowledge)
        self.final_csv = self.final_csv.assign(ASSOCIATION_Provided20by = self.association_provider)

        #Correct column names
        self.final_csv.columns = self.final_csv.columns.str.replace('_', '.', regex = False)
        self.final_csv.columns = self.final_csv.columns.str.replace('20', ' ', regex = False)

        #Create output file
        self.final_csv.to_csv('chembl_screened_compounds.csv', index = False)


