import streamlit as st
import util
import config
import llm_interface
import streamlit.components.v1 as components


def semantics_tab():
    
    if not(config.prompt_flag):
        st.error("No prompt defined!")
    
    else:
        with st.expander("LLM Prompt and generated Label", expanded=True):
            prompt_form = st.form(key='prompt_form_label')
            config.relationship_prompt_text = llm_interface.generate_prompt(config.relationship_prompts, "relationship")


            prompt_statement = prompt_form.text_area("Prompt:", value=config.relationship_prompt_text)
            prompt_submitted = prompt_form.form_submit_button("Generate Concept Relationship Label")

            if(prompt_submitted):
                label_response = []
                while(not label_response or len(label_response[0]) != 3):
                    label_response = llm_interface.generate_label(config.model, config.relationship_prompt_text, [config.origin_concept, config.destination_concept])
                
                st.write(label_response)
                config.concepts_relationship_label = label_response[0][2]
                util.write_concept_relationship()
                
              
            if(st.button("Accept generated Concept Relationship Label")):
                config.graph_add_flag = True
                config.relationship_label_flag = True
                
                util.add_label_to_knowledge_dict(config.origin_concept, config.destination_concept,
                                                 config.concepts_relationship_label)
                # util.add_to_concept_list()
                # st.write(config.concepts_list)
                
            
        with st.expander("Knowledge Graph", expanded=True):
            if(config.KGraph is None):
                util.generate_graph()
            
            if(config.graph_add_flag):
                util.add_node()
                config.graph_add_flag = False

            util.plot_graph()
            
        
        with st.expander("LLM Prompt and generated Node-Features", expanded=True):
            config.selected_feature = st.selectbox(label="Node Feature", options=(config.features), index=None, placeholder="Features List")
            config.feature_prompt_text = llm_interface.generate_prompt(config.features_prompts, "feature")

            #ARRUMAR ISSO AQUI, TA COM MUITO IF
            if config.feature_prompt_text:
                prompt_form = st.form(key='prompt_form_features')
                prompt_statement = prompt_form.text_area("Prompt:", value=config.feature_prompt_text)
                prompt_submitted = prompt_form.form_submit_button("Generate Node-Features")

                if(prompt_submitted):
                    config.feature_response = llm_interface.generate_labelft(config.model, config.feature_prompt_text, [config.origin_concept, config.destination_concept, config.selected_feature])
                    
                    st.write(config.feature_response)
                if(st.button("Accept generated Concept Feature Label")):
                    util.add_feature_to_knowledge_dict(config.origin_concept, config.destination_concept, config.selected_feature, config.feature_response)
                    st.write(config.knowledge_dict[(config.origin_concept, config.destination_concept)])
                
            
        

            