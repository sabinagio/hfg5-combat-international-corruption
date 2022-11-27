import streamlit as st
import pandas as pd
from venn import venn

databases = {"ICIJ Leaks": {"Addresses": "ICIJ/nodes-addresses.csv", "Entities": "ICIJ/nodes-entities.csv", \
    "Intermediaries": "ICIJ/nodes-intermediaries.csv", "Officers": "ICIJ/nodes-officers.csv", "Others": "ICIJ/nodes-others.csv"}, \
    "US State Cable Leaks": {"All Cables": "cable_sentences_through_October_2001.csv"}}

@st.cache
def read_dataframe(file):
    return pd.read_csv(file)
#icij_officers = pd.read_csv("ICIJ/nodes-officers.csv")
#icij_others = pd.read_csv("ICIJ/nodes-others.csv")

@st.cache
def get_addresses(datasets_dict):
    addresses = {}
    for dataset_name in datasets_dict.keys():
        addresses[dataset_name] = set(datasets_dict[dataset_name]["address"].to_list())
    return addresses

@st.cache
def create_venn(datasets_dict, dataset_names, column):
    venn_dict = {}
    for dataset_name in dataset_names:
        dataset = read_dataframe(datasets_dict[dataset_name])
        venn_dict[dataset_name] = set(dataset[column].to_list())
    return venn(venn_dict)


def display_info(dataframe):
    st.metric("Records", dataframe.shape[0], help=None)


def main():

    st.title("HFG5 - Dataset Visualization for Investigators", anchor=None)

    # Allow user to select databases
    database_label = "What databases do you want to look into?"
    database_options = ["ICIJ Leaks", "US State Cable Leaks", "Little Sis"]
    selected_database_options = st.multiselect(database_label, database_options, default=None, \
        key="database", help=None, on_change=None, args=None, kwargs=None, disabled=False, \
        max_selections=None)

    # Allow user to select info they're interested in
    if "ICIJ Leaks" in selected_database_options:
        dataset_label = "You selected the ICIJ database. What datasets are you interested in?"
        dataset_options = databases["ICIJ Leaks"]
        selected_dataset_options = st.multiselect(dataset_label, dataset_options, default=None, \
        key="dataset", help=None, on_change=None, args=None, kwargs=None, disabled=False, \
        max_selections=None)

        if selected_dataset_options:
            tab_no = len(selected_dataset_options)
            tabs = st.tabs(selected_dataset_options)

            for i in range(0, tab_no):
                with tabs[i]:
                   st.header(f"{selected_dataset_options[i]} database")
                   file = databases["ICIJ Leaks"][selected_dataset_options[i]]
                   dataframe = read_dataframe(file)
                   st.metric("Records", dataframe.shape[0], help=None)


            if tab_no == 2:
                first_df = read_dataframe(databases["ICIJ Leaks"][selected_dataset_options[0]])
                second_df = read_dataframe(databases["ICIJ Leaks"][selected_dataset_options[1]])
                common_columns = [col for col in first_df.columns if col in second_df.columns]
                    
                if common_columns:                
                    column_select_label = "Check the overlap between records"
                    column_select_options = common_columns
                    selected_column = st.selectbox(column_select_label, column_select_options, \
                        index=0, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False)
                    st.write(create_venn(dataset_options, selected_dataset_options, selected_column))
                    
                   


    

    # Filters
    #st.sidebar.markdown("**Filters**")
    #filter_year = st.sidebar.slider("Publication year", 2010, 2021, (2010, 2021), 1)
    #filter_citations = st.sidebar.slider("Citations", 0, 250, 0)
    #num_results = st.sidebar.slider("Number of search results", 10, 50, 10)

    # 1. Display datasets tables & tabs
    # 2. Display overlaps between datasets


    # Fetch results
    #if "ICIJ Leaks" in selected_database_options:
    #    datasets = read_icij_dataframes()
    #    addresses = get_addresses(datasets)
    #    st.write(venn(addresses))


if __name__ == "__main__":
    main()