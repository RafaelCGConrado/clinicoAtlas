from langchain_core.prompts import ChatPromptTemplate  
from langchain_ollama.llms import OllamaLLM
import pandas as pd
import re
from pathlib import Path
import subprocess
import config

#templates for relationship labels
templates = {
"no_shot_simple_prompt" :
"""
Contex: 
find a word to descibre the relationship among a pair of entitys 
Pair: {question}

you should answer like this:
Pair: [repeat the given Pair]
reasoning: [write how you got to the answer]
Answer: [first word of the pair(as you were given), second word(as you were given),relationship among them] 
""",
"no_shot_complex_prompt" :
"""
Contex: 
A semantic network is a knowledge base that represents semantic relations between concepts in a network, you will be given two words from relatade to medice and have to inffer the best word to describe their relationship among them for a semantic network

Pair: {question}

you should answer like this:
Pair: [repeat the given Pair]
reasoning: [write how you got to the answer]
Answer: [first word of the pair(as you were given), second word(as you were given),relationship among them] 

""",
"simple_prompt" :
""""
Contex: 
A semantic network is a knowledge base that represents semantic relations between concepts in a network, you will be given two words from a medical context and have to inffer the best word to describe their relationship among them for a semantic network
you should answer like this:
Pair: [repeat the given Pair]
reasoning: [write how you got to the answer]
Answer: [first word of the pair(as you were given), second word(as you were given),relationship among them] 

example:
Pair: [human,apple]
Reasoning: in our world humans use to eat apples
Answer: human,apple,eats

example2:
Pair: [Paris,France]
Reasoning: paris is the capital of France 
Answer: paris,france,capital

example3:
Pair: [fire,Wood]
Reasoning: we know that when fire and wood get together the wood burns
Answer: fire,wood,burns

example3:
Pair: [Wood,fire]
Reasoning: we know that when fire and wood get together the fire gets bigger
Answer: wood,fire,strengthens

Pair to answer: {question}

""",
"complex_prompt" :
""""
Contex: 
find a word to descibre the relationship among a pair of entitys 

you should answer like this:
Pair: [repeat the given Pair]
reasoning: [write how you got to the answer]
Answer: [first word of the pair(as you were given), second word(as you were given),relationship among them] 

example:
Pair: [human,apple]
Reasoning: in our world humans use to eat apples
Answer: human,apple,eats

example2:
Pair: [Paris,France]
Reasoning: paris is the capital of France 
Answer: paris,france,capital

example3:
Pair: [fire,Wood]
Reasoning: we know that when fire and wood get together the wood burns
Answer: fire,wood,burns

example3:
Pair: [Wood,fire]
Reasoning: we know that when fire and wood get together the fire gets bigger
Answer: wood,fire,strengthens

Pair to answer: {question}

"""
}

#Templates for features
ft_templates = {"initial_template":"""
Context: {Contex} 
        
Question: What is the meaning of the {feature} of node {concept1} (concept 1) connected by edges to nodes with values related to the medical concept {concept2} (concept 2),{using_weight}?

Task: You should give the semantic meaning of the {feature} value in a relationship between the two medical concepts.
Provide a straightforward explanation and the clinical interpretation for the domain specialist who is a health practitioner.
Your answer should have the following structure:

Pair of concepts: [repeat the given pair of concepts]
Reasoning: [write how you got to the answer]
Your answer: [first word of the pair (as you were given), second word of the pair (as you were given), explanation of the {feature} for the pair of medical concepts]
Short description: [1 to 4 words explaining the measure]
"""}

#Features Names explanation
explainft = {"in_degree":"The in-degree measure of a given node A indicates the number of distinct nodes connected A from incoming edges.",
                "out_degree":"The out-degree measure of a given node A indicates the number of distinct nodes connected A from outgoing edges.",
                "in_average_IAT":"The in-average-IAT is the average inter-arrival time between consecutive incoming edges of a given node A, i.e., the average time interval between one incoming edge to another.",
                "out_average_IAT":"The out-average-IAT is the average inter-arrival time between consecutive outgoing edges of a given node A, i.e., the average time interval between one outgoing edge to another.",
                "weighted_in_degree":"The weighted-in-degree in a directed graph is the sum of the weights of all incoming edges to that node. If edges have a weight (a numerical value representing strength, frequency, or importance), the weighted-in-degree is the sum of these weights. Otherwise, the weighted-in-degree is the count of incoming edges.",
                "weighted_out_degree":"The weighted-out-degree in a directed graph is the sum of the weights of all outgoing edges from that node. If edges have a weight (a numerical value representing strength, frequency, or importance), the weighted-out-degree is the sum of these weights. Otherwise, the weighted-out-degree is the count of outgoing edges.",
                "core_number":"The core-number in a graph represents the largest k-core in which the node is included."}


# def Verify_LLM_Existence(LLM_Name:list):
#     result = subprocess.run(["ollama","list"], capture_output=True, text=True)
#     result = result.stdout.split()
#     # if LLM_Name not in result:
#     #     print(f"Some requirements were not satisfied LLM {LLM_Name} is not locally downloaded")
#     #     return 0 
#     return 1


def generate_prompt(prompt_type, prompt_class):
    template = ""
    if prompt_class == "relationship":
        template = templates[prompt_type]
    
    if prompt_class == "feature":
        template = ft_templates[prompt_type]

    
    prompt = ChatPromptTemplate.from_template(template)
    return prompt


#Generate relationship label
def generate_label(model, prompt, concept_pair):
    current_model = OllamaLLM(model=f"{model}")
    chain = prompt | current_model
    response = chain.invoke({"question":concept_pair})

    #Encontrar qualquer linha que começa com "Answer"
    regex = r"^Answer\b.*"
    response = re.findall(regex, response, re.MULTILINE)

    # Remover o prefixo "Answer:"
    regex1 = r"^Answer:\s*"
    response = [re.sub(regex1, "", r) for r in response]

    # Substituir palavras por elas mesmas entre aspas
    regex2 = r"\b\w+\b"
    response = [re.findall(r'"(.*?)"', re.sub(regex2, r'"\g<0>"', r)) for r in response]
    return response

#Generate feature meaning
def generate_labelft(model:str, prompt:str, concept_triplet:list)-> str:
    """
    calls LLMs for graph feature explain  

    Args:
        models (str): Model to use.
        prompts (str): Prompts to use.
        concept_triplet (list): [concept1,concept2,feature]


    """
    current_model = OllamaLLM(model=f"{model}")

    chain = prompt | current_model
    if concept_triplet[2].startswith("w"):
        using_weight = "using as the edge weight the count of incoming edges?"
    else:
        using_weight = ""
    print(concept_triplet[0],concept_triplet[1],concept_triplet[2],using_weight)
    response = chain.invoke(input = {"concept1":concept_triplet[0],
                                            "concept2":concept_triplet[1],
                                            "feature":concept_triplet[2],
                                            "using_weight":using_weight,
                                            "Contex":explainft[concept_triplet[2]]
                                            })
        
        
    #remover o caracter "*"
    response = re.sub(string=response,pattern="\*",repl="")
    
    #Encontrar a linha que começa com "Short description"
    regex = r"^Short description:.*"
    response = re.findall(regex, response, re.MULTILINE)

    # Remover o prefixo "Short description:"
    regex1 = r"^Short description:"
    response = re.sub(regex1,"", response[0])

    return response


