#Import libraries
import pandas as pd

class gene_gene_format:
    #Import data
    ncbi_list = pd.read_csv('C:/Users/emily/OneDrive/Documents/Drug ID/gene_data.tsv', sep = '\t')
    final_csv = pd.DataFrame()

    #Create lists (each of these will be a column of the dataframe)
    subject_ids = []
    subject_category = []
    subject_id_prefixes = []
    subject_symbol = []

    object_ids = []
    object_category = []
    object_id_prefixes = []
    object_symbol = []

    predicates = []

    association_subject = []
    association_object = []
    association_publications = []

    #Constructor
    def __init__(self, list):
        self.gene_list = list

    #Binary search methods
    def binary_search(self, list, gene_symbol):
        left_index = 0
        right_index = len(list) - 1

        while left_index <= right_index:
            mid = (left_index + right_index) // 2
            if str(list[mid]) < str(gene_symbol):
                left_index = mid + 1
            elif str(list[mid]) > str(gene_symbol):
                right_index = mid - 1
            else:
                return mid
        return -1

    #Subject columns method
    def subject_columns(self):
        #Sort dataframes alphabetically by gene symbol
        self.gene_list = self.gene_list.sort_values('Node1')
        self.ncbi_list = self.ncbi_list.sort_values('Approved_symbol')

        #Make sorted lists of gene symbol
        node1 = self.gene_list['Node1'].values.tolist()
        symbol_list = self.ncbi_list['Approved_symbol'].values.tolist()
        
        #Match gene symbol from NCBI and gene_list and find NCBI ID, fill subject_ids list
        for i in range(len(self.gene_list)):
            name_index = self.binary_search(symbol_list, node1[i])
            if name_index >= 0:
                subject_id = self.ncbi_list.iloc[name_index, 10]
            else:
                subject_id = 'N/A'
            self.subject_ids.append(subject_id)
        
        #Sort dataframe and subject_id list back to original format
        self.gene_list = self.gene_list.assign(subject_id = self.subject_ids)
        self.gene_list = self.gene_list.sort_values('id')
        self.subject_ids = self.gene_list['subject_id']

        #Fill subject lists with constants or input data
        self.subject_category = ['Gene'] * len(self.gene_list)
        self.subject_id_prefixes = ['NCBI.gene'] * len(self.gene_list)
        self.subject_symbol = self.gene_list['Node1'].values.tolist()

    #Object columns method
    def object_columns(self):
        #Sort dataframes alphabetically by gene symbol
        self.gene_list = self.gene_list.sort_values('Node2')
        self.ncbi_list = self.ncbi_list.sort_values('Approved_symbol')

        #Make sorted lists of gene symbol
        node2 = self.gene_list['Node2'].values.tolist()
        symbol_list = self.ncbi_list['Approved_symbol'].values.tolist()

        #Match gene symbol from NCBI and gene_list and find NCBI ID, fill object_ids list
        for i in range(len(self.gene_list)):
            name_index = self.binary_search(symbol_list, node2[i])
            if name_index >= 0:
                object_id = self.ncbi_list.iloc[name_index, 10]
            else:
                object_id = 'N/A'
            self.object_ids.append(object_id)
        
        #Sort dataframe and object_id list back to original format
        self.gene_list = self.gene_list.assign(object_id = self.object_ids)
        self.gene_list = self.gene_list.sort_values('id')
        self.object_ids = self.gene_list['object_id']

        #Fill object lists with constants or input data
        self.object_category = ['Gene'] * len(self.gene_list)
        self.object_id_prefixes = ['NCBI.gene'] * len(self.gene_list)
        self.object_symbol = self.gene_list['Node2'].values.tolist()
    
    #Predicates column method
    def predicate_column(self):
        #Create list containing edges
        edge_list = self.gene_list['edge'].values.tolist()

        #Method that assigns predicate from edge
        def edge_to_predicate(edge):
            predicate = ''
            edge = str(edge).lower()
            processes_list = ['phosphorylation', 'dephosphorylation', 'ubiquitination', 'deubiquitination', 'methylation', 'demethylation','sumoylation', 'guanine nucleotide exchange factor', 'acetylation', 'deacetylation', 'ADP-ribosylation']

            if 'down-regulates' in edge:
                if 'destabilization' in edge:
                    predicate += 'decreases abundance of;'
                elif 'quantity :' in edge:
                    predicate += 'negatively regulates;decreases abundance of;'
                else:
                    predicate += 'negatively regulates;'
                if 'repression' in edge:
                    predicate += 'decreases amount or activity of;'

            elif 'up-regulates' in edge:
                if 'activity' in edge:
                    predicate += 'increases activity of;'
                elif 'quantity' in edge:
                    predicate += 'increases abundance of;'
                else:
                    predicate += 'positively regulates;'

            elif 'compound' in edge:
                if 'activation' in edge:
                    predicate += 'increases activity of;'
                else:
                    predicate += 'positively correlated with;'

            elif 'activation' in edge:
                if 'tf' in edge:
                    predicate += 'increases expression of;'
                else:
                    predicate += 'increases activity of;'

                if any(process in edge for process in processes_list):
                    predicate += 'affects molecular modification of;'

            elif 'inhibition' in edge:
                if 'ubiquitination' in edge:
                    predicate += 'decreases expression of;'
                else:
                    predicate += 'decreases activity of;'
                if any(process in edge for process in processes_list):
                    predicate += 'affects molecular modification of;'
            
            elif 'repression' in edge:
                if 'tf' in edge:
                    predicate += 'decreases expression of;'
                else:
                    predicate += 'decreases activity of;'

            elif 'expression' in edge:
                predicate += 'affects expression of;'

            elif any(relationship in edge for relationship in ['binding/association', 'ppi']):
                predicate += 'physically interacts with;'

            elif 'binding' in edge:
                predicate += 'binds;'

            elif 'dissociation' in edge:
                predicate += 'negatively correlates with;'

            elif 'indirect effect' in edge:
                if 'phosphorylation' in edge:
                    predicate += 'affects molecular modification of;'
                else:
                    predicate += 'affects;'
            
            elif any(process in edge for process in processes_list):
                predicate += 'affects molecular modification of;'

            elif 'tf' in edge:
                predicate += 'affects expression of;'

            else:
                predicate += 'N/A'

            return predicate

        for i in range(len(self.gene_list)):
            predicate = edge_to_predicate(edge_list[i])
            self.predicates.append(predicate)

    #Association columns method
    def association_columns(self):
        self.association_subject = self.subject_symbol
        self.association_object = self.object_symbol
        self.association_predicate = self.predicates
        self.association_publications = self.gene_list['source'].values.tolist()
    
    #Creating the final csv
    def add_columns(self):
        self.final_csv = self.final_csv.assign(Subject_id = self.subject_ids)
        self.final_csv = self.final_csv.assign(Subject_category = self.subject_category)
        self.final_csv = self.final_csv.assign(Subject_id20prefixes = self.subject_id_prefixes)
        self.final_csv = self.final_csv.assign(Subject_symbol = self.subject_symbol)

        self.final_csv = self.final_csv.assign(object_id = self.object_ids)
        self.final_csv = self.final_csv.assign(object_category = self.object_category)
        self.final_csv = self.final_csv.assign(object_id20prefixes = self.object_id_prefixes)
        self.final_csv = self.final_csv.assign(object_symbol = self.object_symbol)

        self.final_csv = self.final_csv.assign(predicate = self.predicates)

        self.final_csv = self.final_csv.assign(ASSOCIATION_Subject = self.association_subject)
        self.final_csv = self.final_csv.assign(ASSOCIATION_Object = self.association_object)
        self.final_csv = self.final_csv.assign(ASSOCIATION_Predicate = self.association_predicate)
        self.final_csv = self.final_csv.assign(ASSOCIATION_Publications = self.association_publications)

        self.final_csv.columns = self.final_csv.columns.str.replace('_', '.', regex = False)
        self.final_csv.columns = self.final_csv.columns.str.replace('20', ' ', regex = False)

        self.final_csv.to_csv('gene_gene_formatted.csv', index = False)
