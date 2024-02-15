def gen_prompt(Category_specific_Aspect, Category_Keywords, Category_specific_Elements, Category_specific_Features, Category_specific_Setting, Category_specific_Scene, Example_Settings, Category_specific_Content, keywords_output=True):
    
    keywords_output = "Keywords:  "
    general_prompt = f"""As the helpful Stock Photography Assistant, responsible for crafting SEO-optimized titles and descriptions for images.
    Analyze the following image and generate an SEO-optimized, clear, straightforward title and a description.
    OBJECTIVE is to create a title and description that accurately reflect the {Category_specific_Aspect} of the image, while also being optimized for search engines.

    Use formal sentence structures to create titles, that are easy to read and understand.Titles are 70 characters or fewer. Include keywords and essential phrases related to {Category_Keywords}. 
    Titles MUST Maintain a professional, straightforward tone, aiming for a descriptive, engaging, SEO-friendly style without poetic phrases or changing styles.

    Include a maximum of 50 keywords, and don’t include technical data.
    
    Descriptions should be detailed yet concise, within up to 40 words. Description HAS TO BE, informative, and accurately reflects the content and mood of the image, focusing on {Category_specific_Elements}. The description should be straightforward and not poetic.

    The tone MUST be professional and objective, suitable for an SEO-optimized, image-description context.
    
    The audience is users searching for images on iStock, requiring clear and precise information about the content of the images.
    
    In the title and description:
    - HAVE TO BE Straight to the point
    - DO include specific {Category_specific_Features} visible in the image.
    - DO mention the type of {Category_specific_Setting} (e.g., {Example_Settings}).
    - DO highlight any notable or unique aspects of the {Category_specific_Scene}.

    Do NOT:
    - Use dashes, colons, and commas in titles.
    - Treat titles like lists of keywords.
    - Use words like  'heartwarming,' 'captures,' 'amidst,' 'this image represents,' 'focus,' 'on this photo,' 'experiences,' 'illustrating the excitement,' 'atmosphere,' 'witness the scene,' 'showcasing', 'now unfold', 'embracing', and 'capture' or similar.
    - Include generic or vague terms that do not specifically describe the image.
    - Overuse technical jargon that may not be widely understood by a general audience.
    - Provide inaccurate or misleading information about the {Category_specific_Content}.
    - Use repetitive or redundant phrases that do not add value to the description.

    OUTPUT in the following FORMAT: 
    Title: "This is the title."
    Description: "This is a description."
    {keywords_output}
    """
    
    return general_prompt


def technology_innovation_spec():
    Category_specific_Aspect = "innovative and technological aspects",
    Category_Keywords= "technology, innovation, gadgets, software",
    Category_specific_Elements= "technological devices and innovative concepts",
    Category_specific_Features= "technological elements like devices, machines, software interfaces",
    Category_specific_Setting= "type of technological environment (e.g., labs, tech companies)",
    Category_specific_Scene= "technology and innovation scenes",
    Example_Settings= "research labs, tech startups, computer workshops",
    Category_specific_Content= "technology and innovative processes"
    return Category_specific_Aspect, Category_Keywords, Category_specific_Elements,Category_specific_Features, Category_specific_Setting, Category_specific_Scene,Example_Settings, Category_specific_Content
        
    

def landscapes_nature_spec():
    Category_specific_Aspect = "natural landscapes and scenery"
    Category_Keywords = "nature, landscapes, scenery, outdoors"
    Category_specific_Elements = "geographical features, flora, and fauna"
    Category_specific_Features = "natural elements like mountains, rivers, forests"
    Category_specific_Setting = "type of natural setting (e.g., mountains, beaches, forests)"
    Category_specific_Scene = "natural landscapes and outdoor scenes"
    Example_Settings = "national parks, beaches, mountain ranges"
    Category_specific_Content = "natural landscapes and environments"
    return Category_specific_Aspect, Category_Keywords, Category_specific_Elements, Category_specific_Features, Category_specific_Setting, Category_specific_Scene, Example_Settings, Category_specific_Content


def urban_architecture_spec():
    Category_specific_Aspect = "urban landscapes and architectural details"
    Category_Keywords = "urban, architecture, buildings, cityscape"
    Category_specific_Elements = "urban landscapes and architectural styles"
    Category_specific_Features = "architectural features like facades, architectural lines, materials"
    Category_specific_Setting = "type of urban environment (e.g., downtown, historic district)"
    Category_specific_Scene = "urban and architectural scenes"
    Example_Settings = "skyscrapers, city squares, public buildings"
    Category_specific_Content = "architecture and urban environments"
    return Category_specific_Aspect, Category_Keywords, Category_specific_Elements, Category_specific_Features,Category_specific_Setting,Category_specific_Scene, Example_Settings, Category_specific_Content
                

def people_lifestyle_spec():
    Category_specific_Aspect = "daily life and human interactions"
    Category_Keywords = "people, lifestyle, culture, activities"
    Category_specific_Elements = "human activities, emotions, and interactions"
    Category_specific_Features = "elements like facial expressions, clothing, and activities"
    Category_specific_Setting = "type of lifestyle setting (e.g., home, urban life, countryside)"
    Category_specific_Scene = "scenes depicting people and everyday life"
    Example_Settings = "family homes, city streets, community events"
    Category_specific_Content = "human lifestyle and culture"
    return Category_specific_Aspect, Category_Keywords, Category_specific_Elements,Category_specific_Features, Category_specific_Setting,Category_specific_Scene, Example_Settings, Category_specific_Content

    

def business_finance_spec():
    Category_specific_Aspect = "business environments and financial activities"
    Category_Keywords = "business, finance, corporate, economy"
    Category_specific_Elements = "corporate settings, financial elements, business activities"
    Category_specific_Features = "elements like office spaces, business attire, financial charts"
    Category_specific_Setting = "type of business or financial environment (e.g., offices, stock markets)"
    Category_specific_Scene = "corporate and financial scenes"
    Example_Settings = "corporate offices, banks, business meetings"
    Category_specific_Content = "business and financial concepts"
    return Category_specific_Aspect, Category_Keywords, Category_specific_Elements,Category_specific_Features, Category_specific_Setting,Category_specific_Scene, Example_Settings, Category_specific_Content


def travel_world_cultures_spec():
    Category_specific_Aspect = "travel destinations and cultural landmarks"
    Category_Keywords = "travel, culture, landmarks, exploration"
    Category_specific_Elements = "tourist destinations, cultural practices, and historical sites"
    Category_specific_Features = "elements like famous landmarks, local customs, and scenic views"
    Category_specific_Setting = "type of travel or cultural setting (e.g., historic sites, cultural festivals)"
    Category_specific_Scene = "travel and cultural scenes"
    Example_Settings = "famous cities, cultural festivals, historic ruins"
    Category_specific_Content = "travel destinations and cultural heritage"
    return Category_specific_Aspect, Category_Keywords, Category_specific_Elements,Category_specific_Features, Category_specific_Setting,Category_specific_Scene, Example_Settings, Category_specific_Content

    


def food_drink_spec():
    Category_specific_Aspect = "culinary dishes and beverages"
    Category_Keywords = "food, cuisine, drinks, dining"
    Category_specific_Elements = "types of food, beverages, and dining settings"
    Category_specific_Features = "elements like dishes, ingredients, drink presentations"
    Category_specific_Setting = "type of culinary or beverage setting (e.g., restaurants, bars, kitchens)"
    Category_specific_Scene = "food and drink scenes"
    Example_Settings = "gourmet restaurants, home kitchens, street food stalls"
    Category_specific_Content = "culinary arts and beverages"
    return Category_specific_Aspect, Category_Keywords, Category_specific_Elements,Category_specific_Features, Category_specific_Setting,Category_specific_Scene, Example_Settings, Category_specific_Content

    

def animals_wildlife_spec():
    Category_specific_Aspect = "wildlife and animal behaviors"
    Category_Keywords = "animals, wildlife, nature, conservation"
    Category_specific_Elements = "animal species, habitats, and natural behaviors"
    Category_specific_Features = "elements like species types, habitat environments, animal interactions"
    Category_specific_Setting = "type of wildlife environment (e.g., savannahs, forests, oceans)"
    Category_specific_Scene = "wildlife scenes and animal interactions"
    Example_Settings = "national parks, wildlife reserves, underwater scenes"
    Category_specific_Content = "animal species and natural habitats"
    return Category_specific_Aspect, Category_Keywords, Category_specific_Elements, Category_specific_Features, Category_specific_Setting, Category_specific_Scene, Example_Settings, Category_specific_Content

    

def health_wellness_spec():
    Category_specific_Aspect = "health activities and wellness practices"
    Category_Keywords = "health, wellness, fitness, mental well-being"
    Category_specific_Elements = "healthcare settings, wellness activities, and fitness routines"
    Category_specific_Features = "elements like exercise equipment, yoga poses, medical facilities"
    Category_specific_Setting = "type of health or wellness setting (e.g., gyms, yoga studios, hospitals)"
    Category_specific_Scene = "health and wellness scenes"
    Example_Settings = "fitness centers, meditation retreats, medical clinics"
    Category_specific_Content = "health practices and wellness lifestyles"
    return Category_specific_Aspect, Category_Keywords, Category_specific_Elements, Category_specific_Features, Category_specific_Setting, Category_specific_Scene, Example_Settings, Category_specific_Content

    


def sports_recreation_spec():
    Category_specific_Aspect = "athletic activities and recreational sports"
    Category_Keywords = "sports, recreation, athletics, outdoor activities"
    Category_specific_Elements = "sports events, athletic training, and leisure activities"
    Category_specific_Features = "elements like sports equipment, athletic movements, recreational settings"
    Category_specific_Setting = "type of sports or recreational environment (e.g., stadiums, parks, gyms)"
    Category_specific_Scene = "sports activities and recreational scenes"
    Example_Settings = "football fields, hiking trails, community sports centers"
    Category_specific_Content = "athletic and recreational activities"
    return Category_specific_Aspect, Category_Keywords, Category_specific_Elements, Category_specific_Features, Category_specific_Setting, Category_specific_Scene, Example_Settings, Category_specific_Content

    


def arts_entertainment_spec():
    Category_specific_Aspect = "artistic performances and entertainment events"
    Category_Keywords = "arts, entertainment, performances, cultural events"
    Category_specific_Elements = "performing arts, visual arts, and entertainment settings"
    Category_specific_Features = "elements like art exhibits, stage performances, festival activities"
    Category_specific_Setting = "type of artistic or entertainment setting (e.g., theaters, galleries, concert venues)"
    Category_specific_Scene = "arts and entertainment scenes"
    Example_Settings = "music concerts, art exhibitions, theatrical productions"
    Category_specific_Content = "artistic expressions and entertainment"
    return Category_specific_Aspect, Category_Keywords, Category_specific_Elements, Category_specific_Features, Category_specific_Setting, Category_specific_Scene, Example_Settings, Category_specific_Content

    

def fashion_beauty_spec():
    Category_specific_Aspect = "fashion trends and beauty styles"
    Category_Keywords = "fashion, beauty, style, trends"
    Category_specific_Elements = "fashionable clothing, beauty products, and style presentations"
    Category_specific_Features = "elements like clothing designs, makeup, fashion accessories"
    Category_specific_Setting = "type of fashion or beauty setting (e.g., runways, photo shoots, salons)"
    Category_specific_Scene = "fashion and beauty scenes"
    Example_Settings = "designer boutiques, beauty salons, fashion shows"
    Category_specific_Content = "fashion designs and beauty trends"
    return Category_specific_Aspect, Category_Keywords, Category_specific_Elements, Category_specific_Features, Category_specific_Setting, Category_specific_Scene, Example_Settings, Category_specific_Content
 

    
