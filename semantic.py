#TESTE

#Rótulos Relações Semânticas
semantic_relationship_label = {
    ("person_id", "drug_concept_id") : "is exposed to",
    ("drug_concept_id", "person_id") : "exposes",
    ("ingredient_concept_id", "drug_concept_id") : "is ingredient of",
    ("drug_concept_id", "ingredient_concept_id") : "is composed of",
    ("observation_period_id", "person_id") : "is the observation period of",
    ("person_id", "observation_period_id") : "is observed in",
    ("person_id", "procedure_occurrence_id") : "is exposed to",
    ("procedure_occurrence_id", "person_id") : "exposes",
    ("person_id", "visit_occurrence") : "has", #?

}

#Nomes das Features
semantic_relationship_feature = {
    #drug -> person
    ("drug_concept_id", "person_id", "in_degree") : "Number of distinct drugs the person has been exposed to",
    ("drug_concept_id", "person_id", "out_degree") : "Number of distinct people exposed to the drug",
    ("drug_concept_id", "person_id", "core") : "How well connected the drugs the person take are with other patients as well",
    ("drug_concept_id", "person_id", "weighted_out_degree") : "Quantities of drugs the person was exposed to",
    ("drug_concept_id", "person_id", "weighted_in_degree") : "undefined",
    ("drug_concept_id", "person_id", "weighted_degree") : "Total amount of drugs the person was exposed to",

    #person -> drug
    ("person_id", "drug_concept_id", "in_degree") : "Number of distinct people exposed to the drug",
    ("person_id", "drug_concept_id", "out_degree") : "Number of distinct drugs the person has been exposed to",
    ("person_id", "drug_concept_id", "core") : "How well connected the people that take the drug are with other drugs as well",
    ("person_id", "drug_concept_id", "weighted_out_degree") : "Quantity of this drug people were exposed to",
    ("person_id", "drug_concept_id", "weighted_in_degree") : "undefined",
    ("person_id", "drug_concept_id", "weighted_degree") : "Total amount of this drug people were exposed to",

    #ingredient -> drug
    ("ingredient_concept_id", "drug_concept_id", "in_degree") : "Number of drugs composed by the ingredient",
    ("ingredient_concept_id", "drug_concept_id", "out_degree") : "Number of distinct ingredients that composes the drug",
    ("ingredient_concept_id", "drug_concept_id", "core") : "How well connected the drugs the ingredient composes are with other ingredients as well",
    ("ingredient_concept_id", "drug_concept_id", "weighted_out_degree") : "Amount of ingredient that composes drugs",
    ("ingredient_concept_id", "drug_concept_id", "weighted_in_degree") : "undefined",
    ("ingredient_concept_id", "drug_concept_id", "weighted_degree") : "Total amount of ingredient that composes drugs",

    #drug -> ingredient
    ("drug_concept_id", "ingredient_concept_id", "in_degree") : "Number of distinct ingredients of drug",
    ("drug_concept_id", "ingredient_concept_id", "out_degree") : "Number of distinct drugs composed by the ingredient",
    ("drug_concept_id", "ingredient_concept_id", "core") : "How well connected the ingredients that composes the drug are with other drugs as well",
    ("drug_concept_id", "ingredient_concept_id", "weighted_out_degree") : "Amount of ingredients that compose this drug",
    ("drug_concept_id", "ingredient_concept_id", "weighted_in_degree") : "undefined",
    ("drug_concept_id", "ingredient_concept_id", "weighted_degree") : "Total amount of ingredients that compose this drug",

    #observation period -> person
    ("observation_period_id", "person_id", "in_degree") : "Number of distinct people that had this observation period",
    ("observation_period_id", "person_id", "out_degree") : "Number of distint observation periods the person had",
    ("observation_period_id", "person_id", "core") : "How well connected the people that have the observation_period are with other observation periods as well",
    ("observation_period_id", "person_id", "weighted_out_degree") : "Amount of people that had this observation period",
    ("observation_period_id", "person_id", "weighted_in_degree") : "undefined",
    ("observation_period_id", "person_id", "weighted_degree") : "Total amount of people that had this observation period",

    #person -> observation_period
    ("person_id", "observation_period_id", "in_degree") : "Number of distint observation periods the person had",
    ("person_id", "observation_period_id", "out_degree") : "Number of distint people that had this observation period",
    ("person_id", "observation_period_id", "core") : "How well connected the observation_period the person has are with other patients as well",
    ("person_id", "observation_period_id", "weighted_out_degree") : "Amount of observation periods the person had",
    ("person_id", "observation_period_id", "weighted_in_degree") : "undefined",
    ("person_id", "observation_period_id", "weighted_degree") : "Total amount of observation periods the person had",

    #person -> procedure
    ("person_id", "procedure_occurrence_id", "in_degree") : "Number of distinct procedure occurrences the person was exposed to",
    ("person_id", "procedure_occurrence_id", "out_degree") : "Number of distinct  people that were exposed to the procedure",
    ("person_id", "procedure_occurrence_id", "core") : "How well connected the people that have the procedure_occurrence are with other procedures as well",
    ("person_id", "procedure_occurrence_id", "weighted_out_degree") : "Amount of procedures the person was exposed to",
    ("person_id", "procedure_occurrence_id", "weighted_in_degree") : "undefined",
    ("person_id", "procedure_occurrence_id", "weighted_degree") : "Total amount of procedures the person was exposed to",

    #procedure -> person
    ("procedure_occurrence_id", "person_id", "in_degree") : "Number of distinct people that were exposed to the procedure occurrence",
    ("procedure_occurrence_id", "person_id", "out_degree") : "Number of distinct procedure occurrences the person had",
    ("procedure_occurrence_id", "person_id", "core") : "How well connected the procedure_occurrence the person has are with other patients as well",
    ("procedure_occurrence_id", "person_id", "weighted_out_degree") : "Amount of people exposed to the procedure",
    ("procedure_occurrence_id", "person_id", "weighted_in_degree") : "undefined",
    ("procedure_occurrence_id", "person_id", "weighted_degree") : "Total amount of people exposed to the procedure",
}



def extract_semantic_label(table1, table2):
    if(table1, table2) in semantic_relationship_label:
        return semantic_relationship_label[(table1, table2)]
    else:
        return "undefined" 


def extract_semantic_feature(table1, table2, feature):
    if(table1, table2, feature) in semantic_relationship_feature:
        return semantic_relationship_feature[(table1, table2, feature)]
    else:
        return "undefined"
