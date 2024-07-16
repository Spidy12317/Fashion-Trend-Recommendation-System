from time import sleep
import streamlit as st
from PIL import Image
import numpy as np
from utils.vector_store import *
from utils.clip_model import *
from utils.prompt import *
import re

import os
import PIL.Image
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

import base64
from io import BytesIO


# Load vector store
vector_store = NumPyVectorStore.load("./data/app_data/vector_indices/vector_db.pkl")


# Load CLIP model
model_path = "./CLIP" 
embedding_model, embedding_processor = load_clip_model(model_path)

# Configure Generative AI
GOOGLE_API_KEY=os.getenv('API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
llm_model = genai.GenerativeModel('gemini-1.5-flash')


def generate(prompt, img=None):
    response = llm_model.generate_content(prompt)
    return response.text


def generate_suggestion_based_on_purchase_history(image:Image,model:genai.GenerativeModel)->list[str]:

    try:
        response = model.generate_content([SUGGEST_ITEM_PROMPT, image], stream=False)
    except:
        return []
    
    if("text:" not in str(response.candidates)): return []

    return(list(filter(lambda x: x != "" and x!= '<Search Queries:>',map(str.strip,response.text.split("#")))))


def load_and_resize_image(path, size=(720, 1080)):
    try:
        img = Image.open(path)
        img = img.resize(size, Image.LANCZOS)
        return img
    except Exception as e:
        st.error(f"Error loading image from {path}: {str(e)}")
        return None


def serach_myntra_dataset_image_input(image_path):
    global product_data 
    global title_text 

    query_vector = get_image_embedding(embedding_model, embedding_processor, image_path)
    query_vector = np.array(query_vector[0])
    results = vector_store.search("available_stocks", query_vector, k=3)
    product_data = [{"image": result['metadata']['image_path'][1:]} for result in results]
    st.session_state.product_data = product_data
    
    # response = generate(query_response_prompt(query))
    # response = response.split(":")[-1].strip().strip("\"")
    response = "Here are some of the similar products"

    st.session_state.text_title = "Here Are Some Matching Options"
    return response


def serach_myntra_dataset_text_input(query):
    global product_data 
    global title_text 

    enhanced_query = generate(query_enhancer_prompt(query))
    query_vector = get_text_embedding(embedding_model, embedding_processor, enhanced_query)
    query_vector = np.array(query_vector[0])
    results = vector_store.search("available_stocks", query_vector, k=3)
    product_data = [{"image": result['metadata']['image_path'][1:]} for result in results]
    st.session_state.product_data = product_data

    response = generate(query_response_prompt(query))
    response = response.split(":")[-1].strip().strip("\"")

    
    st.session_state.text_title = "Here Are Some Matching Options"
    return response


def classify_user_query(query):
    classification_response = generate(query_classification_prompt(query))
    pattern = r'#([^#]+)#'
    matches = re.findall(pattern, classification_response)
    if matches:
        return matches[0]
    return None


def get_random_products(index,k=3):
    
    count = 0
    imgs = []
    while(count<k):        
        vect = np.random.rand(768)
        results = vector_store.search(index,vect,k = 50)
        prd = {"image": np.random.choice(results)['metadata']['image_path'][1:]}
        
        if(prd not in imgs):
            imgs.append(prd)
            count += 1
    return imgs
              

def render_files(on_click_func=None):
        st.markdown("""
        <div class="navbar">
            <span class="logo">M</span>
            <a href="#" class="navbar-item">MEN</a>
            <a href="#" class="navbar-item">WOMEN</a>
            <a href="#" class="navbar-item">KIDS</a>
            <a href="#" class="navbar-item">HOME & LIVING</a>
            <a href="#" class="navbar-item">BEAUTY</a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<h2 class="category-title">{st.session_state.text_title}</h2>', unsafe_allow_html=True)

        featured_products = st.columns(3)
        
        for idx, (col, product) in enumerate(zip(featured_products, st.session_state.product_data)):
            with col:
                img = load_and_resize_image(product["image"])
                if img:
                    st.image(img, use_column_width=True)

                    if(st.session_state.allow_product_selection):
                        if st.button(f"Select Product {idx+1}", key=f"select_{idx}",on_click=on_click_func,args=(idx,)):
                            if st.session_state.selected_product == product:
                                st.session_state.selected_product = None
                            else:
                                st.session_state.selected_product = product
                    else:
                        st.session_state.selected_product = None


def recommend_on_purchase_history(key):
    img = Image.open(st.session_state.product_data[key]['image'])
    fashion_item_suggestion =  generate_suggestion_based_on_purchase_history(img,llm_model)

    print(*fashion_item_suggestion,sep="\n------------\n")

    recommendations = []
    for suggested_item_description in fashion_item_suggestion:
        query_vector = get_text_embedding(embedding_model, embedding_processor, suggested_item_description)
        query_vector = np.array(query_vector[0])
        
        results = vector_store.search("available_stocks", query_vector, k=5)

        count = 0
        for result in results:
            prd = {"image": result['metadata']['image_path'][1:]}
            if(prd not in recommendations):
                recommendations.append(prd)
                count += 1
            
            if(count ==1):break
        
    st.session_state.product_data = recommendations
    
    img.thumbnail((100, 100))  # Resize the image to a thumbnail
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Add the image to the messages
    st.session_state.messages.append({
        "role": "user", 
        "content": f'<img src="data:image/png;base64,{img_str}" alt="Uploaded Image" style="max-width: 100px; max-height: 100px;">'
    })

    response = "Here are some of the recommendations that compliments the above selected item."

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.session_state.text_title = "Here are some items that will go well together"
    
    st.session_state.allow_product_selection = False

    render_files()
    

def main():
    st.set_page_config(layout="wide", page_title="Fashion E-commerce")
        
    if "allow_product_selection" not in st.session_state:
        st.session_state.allow_product_selection = False

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    .stApp {
        background-color: #ffffff;
        color: #333333;
        font-family: 'Roboto', sans-serif;
    }
    .stTextInput > div > div > input {
        background-color: #f5f5f6;
        color: #333333;
        border: 1px solid #d4d5d9;
        border-radius: 4px;
        padding: 8px 12px;
    }
    .stButton > button {
        background-color: #ff3f6c;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #ff527b;
    }
    .top-banner {
        background-color: #ffeaef;
        color: #333333;
        padding: 10px;
        text-align: center;
        font-weight: 500;
        margin-bottom: 20px;
    }
    .product-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
    }
    .product-item {
        border: 1px solid #d4d5d9;
        border-radius: 4px;
        padding: 10px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .product-item:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .product-item img {
        width: 200px;
        height: 200px;
        object-fit: cover;
    }
    .product-brand {
        font-weight: 500;
        margin-top: 10px;
    }
    .product-discount {
        color: #ff3f6c;
        font-weight: 500;
    }
    h1, h2 {
        font-weight: 700;
        color: #333333;
        margin-bottom: 20px;
    }
    .category-title {
        font-size: 24px;
        font-weight: 700;
        text-align: center;
        margin: 40px 0 20px;
    }
    .navbar {
        background-color: #ffffff;
        padding: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    .navbar-item {
        display: inline-block;
        margin-right: 20px;
        font-weight: 500;
        color: #333333;
        text-decoration: none;
    }
    .logo {
        font-size: 24px;
        font-weight: 700;
        color: #ff3f6c;
    }
    .user_message {
        text-align: right;
        background-color: #cfe0f1;
        color: #333333;
        font-family: 'Roboto', sans-serif;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #b6c9e0;
    }

    .assistant_message {
        text-align: left;
        background-color: #ffffff;
        color: #333333;
        font-family: 'Roboto', sans-serif;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #e0e0e0;
    }


    .file-upload-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 40px;
        width: 40px;
        position: relative;
        top: 756px;
        left: 30px;
        z-index: 1;
    }

    .file-upload-wrapper input[type="file"] {
        font-size: 100px;
        position: absolute;
        opacity: 0;
        height: 100%;
        width: 100%;
        cursor: pointer;
    }

    .file-upload-wrapper::before {
        content: '\\1F4CE'; /* Paperclip Emoji */
        font-size: 20px;
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("Fashion Assistant")

    if "text_title" not in st.session_state:
        st.session_state.text_title = "Here are some TRENDY PRODUCTS"

    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "classify_query" not in st.session_state:
        st.session_state.classify_query = None

    if 'upload_key' not in st.session_state:
        st.session_state.upload_key = 0

    if 'last_uploaded_file' not in st.session_state:
        st.session_state.last_uploaded_file = None

    if "selected_product" not in st.session_state:
        st.session_state.selected_product = None

    if "product_data" not in st.session_state:
        st.session_state.product_data = get_random_products("available_stocks")
        render_files()

    col1, col2 = st.sidebar.columns([3, 1])

    with col1:
        chat_container = st.sidebar.container(height=700)
        prompt = st.sidebar.chat_input("Say something")

    with col2:
        # st.markdown('<div id = "upload_imgae" class="file-upload-wrapper"><input type="file" accept=".jpg,.jpeg,.png" ></div>', unsafe_allow_html=True)
        uploaded_file = st.sidebar.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], key="file_uploader")


    if uploaded_file is not None and uploaded_file != st.session_state.last_uploaded_file:
        response = serach_myntra_dataset_image_input(uploaded_file)
        st.session_state.last_uploaded_file = uploaded_file
        
        img_bytes = uploaded_file.getvalue()
        img = Image.open(BytesIO(img_bytes))
        img.thumbnail((100, 100))  # Resize the image to a thumbnail
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Add the image to the messages
        st.session_state.messages.append({
            "role": "user", 
            "content": f'<img src="data:image/png;base64,{img_str}" alt="Uploaded Image" style="max-width: 100px; max-height: 100px;">'
        })

        st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.session_state.upload_key += 1
        render_files()

        # st.rerun()
        


    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        classify_query = classify_user_query(prompt)
        st.session_state.classify_query = classify_query
        response = ""

        if classify_query == "SQ":
            response = serach_myntra_dataset_text_input(prompt)
            render_files()

        if classify_query == "PH":
            st.session_state.allow_product_selection = True
            st.session_state.product_data = get_random_products("purchase_data")
            response = "Please select one of the previous purchased items"
            render_files(on_click_func=recommend_on_purchase_history)        


        if classify_query == "WB":
            st.session_state.allow_product_selection = True
            st.session_state.product_data = get_random_products("wardrobe_images")
            response = "Please select one of the items from wardrobe"
            render_files(on_click_func=recommend_on_purchase_history)
            # render_files()
        
        if classify_query =="GQ":
            response = generate(general_query_response_prompt(prompt))
            response = response.split(":")[-1].strip().strip("\"")
            render_files()


        st.session_state.messages.append({"role": "assistant", "content": response})

    for message in st.session_state.messages:
        if message["role"] == "user":
            chat_container.markdown(f'<div class="user_message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            chat_container.markdown(f'<div class="assistant_message">{message["content"]}</div>', unsafe_allow_html=True)


    # render_files()

    

if __name__ == "__main__":
    main()
    print("Entered Main", end="\n----------------\n")










































# import streamlit as st
# from PIL import Image
# import numpy as np
# from utils.vector_store import *
# from utils.clip_model import *
# from utils.prompt import *
# import re

# import os
# import PIL.Image
# from dotenv import load_dotenv
# import google.generativeai as genai
# load_dotenv()

# import base64
# from io import BytesIO


# # Load vector store
# vector_store = NumPyVectorStore.load("./data/app_data/vector_indices/vector_db.pkl")
# title_text = "Here are some TRENDY PRODUCTS"

# # Load CLIP model
# model_path = "./CLIP" 
# embedding_model, embedding_processor = load_clip_model(model_path)

# # Configure Generative AI
# GOOGLE_API_KEY=os.getenv('API_KEY')
# genai.configure(api_key=GOOGLE_API_KEY)
# llm_model = genai.GenerativeModel('gemini-1.5-flash')


# def generate(prompt, img=None):
#     response = llm_model.generate_content(prompt)
#     return response.text


# def load_and_resize_image(path, size=(720, 1080)):
#     try:
#         img = Image.open(path)
#         img = img.resize(size, Image.LANCZOS)
#         return img
#     except Exception as e:
#         st.error(f"Error loading image from {path}: {str(e)}")
#         return None

# def serach_myntra_dataset_image_input(image_path):
#     global product_data 
#     global title_text 

#     query_vector = get_image_embedding(embedding_model, embedding_processor, image_path)
#     query_vector = np.array(query_vector[0])
#     results = vector_store.search("available_stocks", query_vector, k=3)
#     product_data = [{"image": result['metadata']['image_path'][1:]} for result in results]
#     st.session_state.product_data = product_data
    
#     # response = generate(query_response_prompt(query))
#     # response = response.split(":")[-1].strip().strip("\"")
#     response = "Here are some of the similar products"

#     title_text = "Here Are Some Matching Options"
#     return response

# def serach_myntra_dataset_text_input(query):
#     global product_data 
#     global title_text 

#     enhanced_query = generate(query_enhancer_prompt(query))
#     query_vector = get_text_embedding(embedding_model, embedding_processor, enhanced_query)
#     query_vector = np.array(query_vector[0])
#     results = vector_store.search("available_stocks", query_vector, k=3)
#     product_data = [{"image": result['metadata']['image_path'][1:]} for result in results]
#     st.session_state.product_data = product_data

#     response = generate(query_response_prompt(query))
#     response = response.split(":")[-1].strip().strip("\"")

#     title_text = "Here Are Some Matching Options"
#     return response

# def classify_user_query(query):
#     classification_response = generate(query_classification_prompt(query))
#     pattern = r'#([^#]+)#'
#     matches = re.findall(pattern, classification_response)
#     if matches:
#         return matches[0]
#     return None




# def main():
#     st.set_page_config(layout="wide", page_title="Fashion E-commerce")

#     if "product_data" not in st.session_state:
#         product_data = []
#         for _ in range(3):        
#             vect = np.random.rand(768)
#             results = vector_store.search("available_stocks",vect,k = 20)
#             product_data.append({"image":np.random.choice(results)['metadata']['image_path'][1:]})

#         st.session_state.product_data = product_data

#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

#     .stApp {
#         background-color: #ffffff;
#         color: #333333;
#         font-family: 'Roboto', sans-serif;
#     }
#     .stTextInput > div > div > input {
#         background-color: #f5f5f6;
#         color: #333333;
#         border: 1px solid #d4d5d9;
#         border-radius: 4px;
#         padding: 8px 12px;
#     }
#     .stButton > button {
#         background-color: #ff3f6c;
#         color: #ffffff;
#         border: none;
#         border-radius: 4px;
#         padding: 8px 16px;
#         font-weight: 500;
#         transition: all 0.3s ease;
#     }
#     .stButton > button:hover {
#         background-color: #ff527b;
#     }
#     .top-banner {
#         background-color: #ffeaef;
#         color: #333333;
#         padding: 10px;
#         text-align: center;
#         font-weight: 500;
#         margin-bottom: 20px;
#     }
#     .product-grid {
#         display: grid;
#         grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
#         gap: 20px;
#     }
#     .product-item {
#         border: 1px solid #d4d5d9;
#         border-radius: 4px;
#         padding: 10px;
#         text-align: center;
#         transition: all 0.3s ease;
#     }
#     .product-item:hover {
#         box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#     }
#     .product-item img {
#         width: 200px;
#         height: 200px;
#         object-fit: cover;
#     }
#     .product-brand {
#         font-weight: 500;
#         margin-top: 10px;
#     }
#     .product-discount {
#         color: #ff3f6c;
#         font-weight: 500;
#     }
#     h1, h2 {
#         font-weight: 700;
#         color: #333333;
#         margin-bottom: 20px;
#     }
#     .category-title {
#         font-size: 24px;
#         font-weight: 700;
#         text-align: center;
#         margin: 40px 0 20px;
#     }
#     .navbar {
#         background-color: #ffffff;
#         padding: 10px 0;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#         position: sticky;
#         top: 0;
#         z-index: 1000;
#     }
#     .navbar-item {
#         display: inline-block;
#         margin-right: 20px;
#         font-weight: 500;
#         color: #333333;
#         text-decoration: none;
#     }
#     .logo {
#         font-size: 24px;
#         font-weight: 700;
#         color: #ff3f6c;
#     }
#     .user_message {
#         text-align: right;
#         background-color: #cfe0f1;
#         color: #333333;
#         font-family: 'Roboto', sans-serif;
#         padding: 10px;
#         border-radius: 8px;
#         margin-bottom: 10px;
#         border: 1px solid #b6c9e0;
#     }

#     .assistant_message {
#         text-align: left;
#         background-color: #ffffff;
#         color: #333333;
#         font-family: 'Roboto', sans-serif;
#         padding: 10px;
#         border-radius: 8px;
#         margin-bottom: 10px;
#         border: 1px solid #e0e0e0;
#     }


#     .file-upload-wrapper {
#         display: flex;
#         justify-content: center;
#         align-items: center;
#         height: 40px;
#         width: 40px;
#         position: relative;
#         top: 756px;
#         left: 30px;
#         z-index: 1;
#     }

#     .file-upload-wrapper input[type="file"] {
#         font-size: 100px;
#         position: absolute;
#         opacity: 0;
#         height: 100%;
#         width: 100%;
#         cursor: pointer;
#     }

#     .file-upload-wrapper::before {
#         content: '\\1F4CE'; /* Paperclip Emoji */
#         font-size: 20px;
#         color: #000000;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     # Sidebar
#     st.sidebar.title("Fashion Assistant")

#     if "messages" not in st.session_state:
#         st.session_state.messages = []
        
#     if "classify_query" not in st.session_state:
#         st.session_state.classify_query = None


#     if 'upload_key' not in st.session_state:
#         st.session_state.upload_key = 0

#     if 'last_uploaded_file' not in st.session_state:
#         st.session_state.last_uploaded_file = None

#     col1, col2 = st.sidebar.columns([3, 1])

#     with col1:
#         chat_container = st.sidebar.container(height=700)
#         prompt = st.sidebar.chat_input("Say something")

#     with col2:
#         # st.markdown('<div id = "upload_imgae" class="file-upload-wrapper"><input type="file" accept=".jpg,.jpeg,.png" ></div>', unsafe_allow_html=True)
#         uploaded_file = st.sidebar.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], key="file_uploader")


#     if uploaded_file is not None and uploaded_file != st.session_state.last_uploaded_file:
#         response = serach_myntra_dataset_image_input(uploaded_file)
#         st.session_state.last_uploaded_file = uploaded_file
        
#         img_bytes = uploaded_file.getvalue()
#         img = Image.open(BytesIO(img_bytes))
#         img.thumbnail((100, 100))  # Resize the image to a thumbnail
#         buffered = BytesIO()
#         img.save(buffered, format="PNG")
#         img_str = base64.b64encode(buffered.getvalue()).decode()
        
#         # Add the image to the messages
#         st.session_state.messages.append({
#             "role": "user", 
#             "content": f'<img src="data:image/png;base64,{img_str}" alt="Uploaded Image" style="max-width: 100px; max-height: 100px;">'
#         })

#         st.session_state.messages.append({"role": "assistant", "content": response})

        

#         st.session_state.upload_key += 1
#         st.rerun()


#     if prompt:
#         st.session_state.messages.append({"role": "user", "content": prompt})

#         classify_query = classify_user_query(prompt)
#         st.session_state.classify_query = classify_query
#         response = ""

#         if classify_query == "SQ":
#             response = serach_myntra_dataset_text_input(prompt)
        
#         if classify_query == "PH":
#             response = "Still Working on it (PH)"

#         if classify_query == "WB":
#             response = "Still Working on it (WB)"
        
#         if classify_query =="GQ":
#             response = generate(general_query_response_prompt(prompt))
#             response = response.split(":")[-1].strip().strip("\"")


#         st.session_state.messages.append({"role": "assistant", "content": response})

#     for message in st.session_state.messages:
#         if message["role"] == "user":
#             chat_container.markdown(f'<div class="user_message">{message["content"]}</div>', unsafe_allow_html=True)
#         else:
#             chat_container.markdown(f'<div class="assistant_message">{message["content"]}</div>', unsafe_allow_html=True)

#     # Main content
#     st.markdown("""
#     <div class="navbar">
#         <span class="logo">M</span>
#         <a href="#" class="navbar-item">MEN</a>
#         <a href="#" class="navbar-item">WOMEN</a>
#         <a href="#" class="navbar-item">KIDS</a>
#         <a href="#" class="navbar-item">HOME & LIVING</a>
#         <a href="#" class="navbar-item">BEAUTY</a>
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown(f'<h2 class="category-title">{title_text}</h2>', unsafe_allow_html=True)

#     featured_products = st.columns(3)
    
#     for col, product in zip(featured_products, st.session_state.product_data):
#         with col:
#             img = load_and_resize_image(product["image"])
#             if img:
#                 st.image(img, use_column_width=True)


# if __name__ == "__main__":

#     main()
#     print("Entered Main",end="\n----------------\n")
