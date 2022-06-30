import streamlit as st
import pandas as pd
import numpy as np
import itertools

# Page Configuration
st.set_page_config(
    page_title='My Fridge Data', 
    layout='wide',
    initial_sidebar_state='auto'
)

st.title("My Fridge Data")
st.write("Like [MyFridgeFood](https://myfridgefood.com/) but for data. Select the data (ingredients) you have and it'll show you the analyses (recipes) you can do with that data. You can also search analyses by use case, as well as combine the data you have with your desired use cases to show relevant analyses.")
st.info("Note: this is very much in POC phase")
st.write("---")

with st.sidebar:
    st.subheader("Settings")
    combine_search = st.checkbox(label="Combine data & use case search", value=False)
    show_incomplete = st.checkbox(label="Show analyses I have incomplete data for", value=True)

analyses_dict = {
    "Market Basket Analysis": {
        "required_data": ["Product Name", "Product Quantity", "Order ID"],
        "description": """Market basket analysis is a data mining technique used by retailers to increase sales by better understanding customer purchasing patterns. It involves analyzing large data sets, such as purchase history, to reveal product groupings, as well as products that are likely to be purchased together.""",
        "use_cases": ["Customize promotions", "Identify sales influencers", "Arrange SKU display", "Product pricing"],
        "more_info": ["https://medium.com/analytics-vidhya/market-basket-analysis-127c73f353d7"],
        "examples": ["https://www.kaggle.com/code/xvivancos/market-basket-analysis/report"],
    },
    "RFM Analysis": {
        "required_data": ["Customer ID", "Order ID", "Order Date", "Product Quantity", "Unit Price"],
        "description": """RFM analysis is a marketing technique used to quantitatively rank and group customers based on the recency, frequency and monetary total of their recent transactions to identify the best customers and perform targeted marketing campaigns.""",
        "use_cases": ["Personalized targeting"],
        "more_info": ["https://www.actioniq.com/blog/what-is-rfm-analysis/"],
        "examples": ["https://www.kaggle.com/code/sarahm/customer-segmentation-using-rfm-analysis/notebook"],
    },
    "Cohort Analysis": {
        "required_data": ["Customer ID", "Order ID", "Order Date", "Product Quantity", "Unit Price"],
        "description": """Cohort analysis is a subset of behavioral analytics that takes the data from a given eCommerce platform, web application, or online game and rather than looking at all users as one unit, it breaks them into related groups for analysis. These related groups, or cohorts, usually share common characteristics or experiences within a defined time-span.""",
        "use_cases": ["Increase retention", "Reduce churn"],
        "more_info": ["https://en.wikipedia.org/wiki/Cohort_analysis"],
        "examples": ["https://www.kaggle.com/code/mahmoudelfahl/cohort-analysis-customer-segmentation-with-rfm/notebook"],
    },
    "Product Recommendation": {
        "required_data": ["Customer ID", "Order ID", "Order Date", "Product Rating"],
        "description": """Product recommendations are part of an ecommerce personalization strategy wherein products are dynamically populated to a user on a webpage, app, or email based on data such as customer attributes, browsing behavior, or situational context—providing a personalized shopping experience.""",
        "use_cases": ["Personalized targeting", "Increase conversions", "Increase avg. order value"],
        "more_info": ["https://kibocommerce.com/blog/product-recommendations/#:~:text=Product%20recommendations%20are%20part%20of,providing%20a%20personalized%20shopping%20experience."],
        "examples": ["https://www.kaggle.com/code/shawamar/product-recommendation-system-for-e-commerce/notebook"],
    },
}

def get_unique_from_nested(dict, key):
    nested = [d[key] for d in dict.values()]
    results = np.unique(list(itertools.chain.from_iterable(nested)))
    return results

def match_all_from_selected(dict, selected, key):
    available = []
    for k, v in dict.items():
        if all(j in selected for j in v[key]):
            available.append(k)
    return available

def match_any_from_selected(dict, selected, key):
    available = []
    for k, v in dict.items():
        if any(j in selected for j in v[key]):
            available.append(k)
    return available

def list_to_md_bullets(list):
    str = ""
    for item in list:
        str += "* " + item + "\n"
    return str

available_data = get_unique_from_nested(analyses_dict, "required_data")
available_use_cases = get_unique_from_nested(analyses_dict, "use_cases")

c1, c2 = st.columns(2)
selected_data = c1.multiselect(label="Select your data", options=available_data)
selected_use_cases = c2.multiselect(label="Select your use cases", options=available_use_cases)

if show_incomplete:
    analyses_by_data = match_any_from_selected(analyses_dict, selected_data, "required_data")
else:
    analyses_by_data = match_all_from_selected(analyses_dict, selected_data, "required_data")

analyses_by_use_case = match_any_from_selected(analyses_dict, selected_use_cases, "use_cases")
joined_analyses = [*analyses_by_data, *analyses_by_use_case]

available_analyses = []
if combine_search and analyses_by_use_case:
    available_analyses = np.unique(list(set(analyses_by_data) & set(analyses_by_use_case)))
else:
    available_analyses = np.unique(joined_analyses)

# Display results
for a in available_analyses:
    st.subheader(a)
    use_case_list = list_to_md_bullets(analyses_dict[a]["use_cases"])
    more_info_list = list_to_md_bullets(analyses_dict[a]["more_info"])
    examples_list = list_to_md_bullets(analyses_dict[a]["examples"])
    
    c1, c2, c3, c4, c5 = st.columns([6,1,2,2,1])
    with c1:
        st.write("**Description**")
        st.write(analyses_dict[a]["description"])
        st.write("**More Info**")
        st.markdown(more_info_list)
        st.write("**Examples**")
        st.markdown(examples_list)

    with c3:
        st.write("**Use Cases**")
        st.markdown(use_case_list)
    
    c4.write("**Required Data**")
    required_data = analyses_dict[a]["required_data"]
    for d in required_data:
        if d in selected_data:            
            c4.checkbox(label=d, value=True, key=a + d)
        else:
            c4.checkbox(label=d, value=False, key=a + d)

    st.write("---")   
