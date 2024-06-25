# import streamlit as st
# from PIL import Image

# def main():
#     st.set_page_config(layout="wide")

#     # Custom CSS to style the interface
#     st.markdown("""
#     <style>
#     .stApp {
#         background-color: #1e1e1e;
#         color: white;
#     }
#     .chat-container {
#         background-color: #2d2d2d;
#         height: 500px;
#         border-radius: 10px;
#         padding: 20px;
#         margin-bottom: 20px;
#     }
#     .stTextInput > div > div > input {
#         background-color: #3a3a3a;
#         color: white;
#         border: none;
#         border-radius: 20px;
#         padding: 10px 20px;
#     }
#     .stButton > button {
#         background-color: #3a3a3a;
#         color: white;
#         border: none;
#         border-radius: 20px;
#         padding: 10px 20px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     st.title("Fashion Chatbot")

#     # Split the screen into two columns
#     left_column, right_column = st.columns([1, 1])

#     with left_column:
#         st.write("## Chat")
#         messages = st.container(height=300)
            
#         if "messages" not in st.session_state:
#             st.session_state.messages = []
        
#         if prompt := st.chat_input("Say something"):
#             st.session_state.messages.append({"role": "user", "content": prompt})

#             response = "How Can I Help You?"
#             st.session_state.messages.append({"role": "assistant", "content": response})

#             for message in st.session_state.messages:
#                 messages.chat_message(message['role']).write(message["content"])


#     with right_column:
#         st.write("## Products")

#         # Display products in a grid
#         cols = st.columns(2)
#         for i in range(4):
#             with cols[i % 2]:
#                 st.image("./data/Trend Analysis/pinterest/a4b7e7fa-fff0-3122-8508-ba87c5c4f042.png")
#                 st.button(f"View Product {i+1}")



# if __name__ == "__main__":
#     main()


# import streamlit as st
# from PIL import Image
# import requests
# from io import BytesIO

# def load_image(url):
#     response = requests.get(url)
#     img = Image.open(BytesIO(response.content))
#     return img

# def main():
#     st.set_page_config(layout="wide", page_title="Fashion Chatbot")

#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap');

#     .stApp {
#         background-color: #f5f5f5;
#         color: #333333;
#         font-family: 'Roboto', sans-serif;
#     }
#     .stTextInput > div > div > input {
#         background-color: #e0e0e0;
#         color: #333333;
#         border: none;
#         border-radius: 20px;
#         padding: 10px 20px;
#     }
#     .stButton > button {
#         background: linear-gradient(45deg, #6b9cff, #79b7e6);
#         color: #ffffff;
#         border: none;
#         border-radius: 20px;
#         padding: 10px 20px;
#         font-weight: 500;
#         transition: all 0.3s ease;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.1);
#     }
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 4px 10px rgba(0,0,0,0.15);
#     }
#     .chat-container {
#         background-color: #ffffff;
#         border-radius: 10px;
#         padding: 20px;
#         margin-bottom: 20px;
#         height: 400px;
#         overflow-y: auto;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.05);
#     }
#     .chat-message {
#         padding: 10px;
#         margin-bottom: 10px;
#         border-radius: 10px;
#         animation: fadeIn 0.5s ease;
#     }
#     .chat-message.user {
#         background-color: #d0e8ff;
#         margin-left: 20px;
#     }
#     .chat-message.assistant {
#         background-color: #e6f4ff;
#         margin-right: 20px;
#     }
#     .product-grid {
#         display: grid;
#         grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
#         gap: 20px;
#     }
#     .product-item {
#         background-color: #ffffff;
#         border-radius: 10px;
#         padding: 10px;
#         text-align: center;
#         transition: all 0.3s ease;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.1);
#     }
#     .product-item:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 5px 15px rgba(107, 156, 255, 0.3);
#     }
#     .product-item img {
#         max-width: 100%;
#         border-radius: 5px;
#         height: 200px;
#         object-fit: cover;
#     }
#     h1, h2 {
#         font-weight: 500;
#         color: #6b9cff;
#         margin-bottom: 20px;
#     }
#     @keyframes fadeIn {
#         from { opacity: 0; transform: translateY(10px); }
#         to { opacity: 1; transform: translateY(0); }
#     }
#     .fashion-icon {
#         font-size: 48px;
#         text-align: center;
#         margin-top: 20px;
#         animation: float 3s ease-in-out infinite;
#     }
#     @keyframes float {
#         0% { transform: translateY(0px); }
#         50% { transform: translateY(-10px); }
#         100% { transform: translateY(0px); }
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
#     </style>
#     """, unsafe_allow_html=True)

    
#     st.title("Fashion Chatbot")

#     # Split the screen into two columns
#     left_column, right_column = st.columns([1, 1])


#     with left_column:
#         st.write("## Chat")
#         chat_container = st.container(height=600)

#         if "messages" not in st.session_state:
#             st.session_state.messages = []
        
#         if prompt := st.chat_input("Say something"):
#             st.session_state.messages.append({"role": "user", "content": prompt})

#             response = "How Can I Help You?"
#             st.session_state.messages.append({"role": "assistant", "content": response})

#             # for message in st.session_state.messages:
#             #     if message["role"] == "user":
#             #         chat_container.markdown(f'<div class="user_message">{message["content"]}</div>', unsafe_allow_html=True)
#             #     else:
#             #         chat_container.markdown(f'<div class="assistant_message">{message["content"]}</div>', unsafe_allow_html=True)

#         # if prompt := st.chat_input("Say something about fashion..."):
#         #     st.session_state.messages.append({"role": "user", "content": prompt})
#         #     response = "That's an interesting perspective on fashion! Can you tell me more about your style preferences?"
#         #     st.session_state.messages.append({"role": "assistant", "content": response})
#         #     st.experimental_rerun()

#     with right_column:
#         st.write("## Products")
        
#         # Using Streamlit's built-in columns for the product grid
#         col1, col2 = st.columns(2)
        
        
#         # Placeholder image URLs
#         placeholder_urls = [
#             "./data/Trend Analysis/pinterest/981577ad-f064-3640-800c-ba6866654b5b.png",
#             ]*4
        
#         for i, col in enumerate([col1, col2, col1, col2]):
#             with col:
#                 st.image(placeholder_urls[i], use_column_width=True)
#                 st.button(f"View Product {i+1}")


#     # Add a simple CSS animation
#     st.markdown('<div class="fashion-icon">👗</div>', unsafe_allow_html=True)

#     for message in st.session_state.messages:
#         if message["role"] == "user":
#             chat_container.markdown(f'<div class="user_message">{message["content"]}</div>', unsafe_allow_html=True)
#         else:
#             chat_container.markdown(f'<div class="assistant_message">{message["content"]}</div>', unsafe_allow_html=True)


# if __name__ == "__main__":
#     main()



import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def main():
    st.set_page_config(layout="wide", page_title="Fashion E-commerce")

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
        max-width: 100%;
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
    </style>
    """, unsafe_allow_html=True)

    # Navbar
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

    # Featured Products
    st.markdown('<h2 class="category-title">FEATURED PRODUCTS</h2>', unsafe_allow_html=True)
    
    featured_products = st.columns(3)
    
    product_data = [
        {"brand": "MANGO", "discount": "30-60% OFF", "image": "./data/Trend Analysis/pinterest/4f5e4054-12c6-3498-88e8-09b892a8251f.png"},
        {"brand": "HIGHLANDER", "discount": "MIN. 60% OFF", "image": "./data/Trend Analysis/pinterest/4f5e4054-12c6-3498-88e8-09b892a8251f.png"},
        {"brand": "Levi's", "discount": "30-60% OFF", "image": "https://placeholder.com/200x250"},
    ]

    for col, product in zip(featured_products, product_data):
        with col:
            st.image(product["image"], use_column_width=True)
            st.markdown(f'<div class="product-brand">{product["brand"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="product-discount">{product["discount"]}</div>', unsafe_allow_html=True)

    # Shop by Category
    st.markdown('<h2 class="category-title">SHOP BY CATEGORY</h2>', unsafe_allow_html=True)
    
    categories = st.columns(4)
    category_names = ["Men", "Women", "Kids", "Home & Living"]
    
    for col, name in zip(categories, category_names):
        with col:
            st.image("https://placeholder.com/200x200", use_column_width=True)
            st.button(name)

    # Chat Widget (simplified)
    st.sidebar.title("Fashion Assistant")
    user_input = st.sidebar.text_input("Ask about fashion:")
    if user_input:
        st.sidebar.write(f"You: {user_input}")
        st.sidebar.write("Assistant: How can I help you with your fashion needs today?")

if __name__ == "__main__":
    main()