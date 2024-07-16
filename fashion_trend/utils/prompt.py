query_enhancer_prompt = lambda query: f"""

# Fashion Query Enhancement Template

Given a user's search query for a fashion item, generate an enhanced query that includes more detailed information about the item's characteristics. Consider the following aspects:

1. Item type (e.g., dress, shirt, pants, shoes)
2. Style (e.g., casual, formal, bohemian, vintage)
3. Color(s)
4. Material(s)
5. Pattern (if applicable)
6. Occasion (e.g., everyday wear, party, work)
7. Season (if applicable)
8. Brand or designer (if mentioned)
9. Size or fit (if mentioned)

Original query: "blue jeans for women"
Enhanced query: A women's pair of jeans that is casual and suitable for everyday wear. It features a blue denim material with a solid design. This piece is perfect for all seasons and has a regular fit.

Original query: {query}
Enhanced_Query:

"""


query_response_prompt = lambda query: f""" 

Given a user's search query for a fashion item, generate a brief, engaging single-line response that encourages the user to check out the displayed product recommendations. The response should be tailored to the user's query without repeating specific product details.

Template:
"Based on your search for [QUERY_FOCUS], we've curated some [POSITIVE_ADJECTIVE] options that might catch your eye – take a look and see what you think!"

Examples:

1. User query: "summer dresses for beach vacation"
   Response: "We've lined up some breezy and stylish options perfect for your beach getaway – why not explore these summer stunners?"

2. User query: "men's formal shoes for office"
   Response: "Check out these sleek and professional choices we've selected – they might be just what you need to step up your office style!"

3. User query: "trendy sunglasses for women"
   Response: "We've gathered some eye-catching and fashion-forward shades that are sure to turn heads – have a peek at these cool options!"

4. User query: "comfortable running shoes for beginners"
   Response: "Take a look at these supportive and cushioned picks we've found – they could be your perfect companions for starting your running journey!"


1. User query: {query}
Response: 

"""



# query_classification_prompt = lambda query:f"""

# Given a user's query related to fashion, classify it into one of the following categories:
# 1. #SQ#: Search related Query
# 2. #PH#: Purchase History related Query
# 3. #WB#: Picking Outfit From Wardrobe related Query

# Analyze the query and determine which category it belongs to based on the following criteria:

# 1. #SQ# (Search related Query):
#    - Contains keywords related to finding or searching for specific items
#    - Asks about product availability, styles, or trends
#    - Inquires about general fashion information

# 2. #PH# (Purchase History related Query):
#    - References past purchases or orders
#    - Asks about order status, returns, or exchanges
#    - Inquires about previously bought items or recommendations based on past purchases

# 3. #WB# (Picking Outfit From Wardrobe related Query):
#    - Asks for advice on putting together outfits
#    - References items the user already owns
#    - Seeks suggestions for styling existing pieces

# Based on these criteria, classify the query as:

# Examples:

# 1. User Query: "Where can I find red high heels for a party?"
#    Classification: #SQ#

# 2. User Query: "When will my order of blue jeans arrive?"
#    Classification: #PH#

# 3. User Query: "How can I style my black dress for a casual day out?"
#    Classification: #WB#
# ```

# User Query: {query}
# Classification: [INSERT CLASSIFICATION HERE (#SQ#, #PH#, or #WB#)]
   
# """

query_classification_prompt = lambda query:f"""
Given a user's query related to fashion, classify it into one of the following categories:
1. #SQ#: Search related Query
2. #PH#: Purchase History related Query
3. #WB#: Picking Outfit From Wardrobe related Query
4. #GQ#: General Query

Analyze the query and determine which category it belongs to based on the following criteria:

1. #SQ# (Search related Query):
   - Contains keywords related to finding or searching for specific items
   - Asks about product availability, styles, or trends
   - Inquires about general fashion information

2. #PH# (Purchase History related Query):
   - References past purchases or orders
   - Asks about order status, returns, or exchanges
   - Inquires about previously bought items or recommendations based on past purchases

3. #WB# (Picking Outfit From Wardrobe related Query):
   - Asks for advice on putting together outfits
   - References items the user already owns
   - Seeks suggestions for styling existing pieces

4. #GQ# (General Query):
   - Any query not related to the above classifications

Based on these criteria, classify the query as:

Examples:

1. User Query: "Where can I find red high heels for a party?"
   Classification: #SQ#

2. User Query: "When will my order of blue jeans arrive?"
   Classification: #PH#

3. User Query: "How can I style my black dress for a casual day out?"
   Classification: #WB#

4. User Query: "What are some popular fashion events happening this month?"
   Classification: #GQ#

User Query: {query}
Classification: [INSERT CLASSIFICATION HERE (#SQ#, #PH#, #WB#, or #GQ#)]
"""



general_query_response_prompt = lambda query:f"""
You are a friendly AI assistant specialized in fashion. Your responses should be brief, casual, and have a hint of personality. When given a query, follow these guidelines:

1. If the query is fashion-related:
   - Provide a short, helpful response
   - Use a conversational tone
   - Feel free to add a touch of humor or enthusiasm when appropriate

2. If the query is not fashion-related:
   - Politely redirect the user to ask about fashion
   - Use a friendly, casual tone
   - Maybe throw in a fashion-related quip or pun

Examples:

User: "What's trending in summer fashion?"
Assistant: Ooh, summer vibes! Think breezy linen, bold prints, and oversized sunnies. Crop tops are having a moment too – if you dare!

User: "How do I solve this math equation?"
Assistant: Math? That's not really my strong suit. How about we talk threads instead of theorems? Got any fashion puzzles you need cracking?

User: "What should I wear to a beach wedding?"
Assistant: Beach wedding? Lucky you! Go for flowy fabrics in pastel shades. A breezy maxi dress or linen suit would be *chef's kiss*. Don't forget comfy sandals – sand and stilettos don't mix!

User: "Can you recommend a good restaurant?"
Assistant: Ah, I'm more about feeding your fashion appetite than your stomach! How about we dish on the latest style trends instead? What's your fashion craving?


User: {query}
Assistant:

"""




SUGGEST_ITEM_PROMPT = """ 
    Analyze the following image of a fashion product:

    Suggest 3 complementary fashion items that would pair well with this product, considering factors such as color coordination, style consistency, occasion appropriateness, and seasonal relevance.

    Format the response as follows, using '#' as a delimiter:

    #Complementary Item 1
    #Complementary Item 2
    #Complementary Item 3
    """