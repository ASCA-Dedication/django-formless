#  i have created this file - GTA
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
# from .models import Product, Contact
# import random

from django.templatetags.static import static
import os
from django.conf import settings



# NER 
import spacy
nlp = spacy.load("en_core_web_sm")# Load the spaCy model with NER component

import re
import nltk
from nltk.stem import PorterStemmer

# Model Edit
from pygltflib import GLTF2


# ---------------------------------------------------------------------------
# Routes Funtions
# ---------------------------------------------------------------------------


# Create your views here.
chatList = ["hello"]

def home(request):
    # products = Product.objects.all()

    # all_prods = []
    # catProds = Product.objects.values('category', 'Product_id')
    # cats = {item['category'] for item in catProds}
    # for cat in cats:
    #     prod = Product.objects.filter(category=cat)
    #     n = len(products)
    #     all_prods.append([prod, n]) 

    # params = {
    #     'catproducts' : all_prods,
    #     'allproducts' : products,
    #           }

    # return render(request,'formlessapp/index.html', params)

    # return render(request,'formlessapp/home.html')
    return render(request,'formlessapp/loadobjModel.html')
    # return render(request,'formlessapp/loadModel.html')


def customemodel(request):
    # return HttpResponse('Teamzeffort    |      business Page')
    return render(request,'formlessapp/customemodel.html')

# Actions

@csrf_exempt  # To disable CSRF protection (not recommended for production)
def chat_view(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')  # Get the input field value
        print(f"Received input: {input_text}")  # Print the input in the terminal
        
        
        NER_result = filtertext(input_text)
        print("Chat - NER : ",NER_result)

        color_name = NER_result["Colors"]
        # modelname = NER_result["Part_Names"]
        # changeModelColor(modelname, color_name)
        
        # changeScenLights(color_name)
        # Example usage:
        # color_name = "red"
        light_diffuse = changeScenLights(color_name)
        # print(f'new BABYLON.Color3({light_diffuse[0]}, {light_diffuse[1]}, {light_diffuse[2]})')
        print("light_diffuse : ", light_diffuse)




        chatList.append(input_text)
        # params = {"chatList" : input_text}
        params = {
            "chatList" : chatList,
            "light_diffuse" : light_diffuse
            }
    # return HttpResponse("Success")  # You can return any response you like
    return render(request,'formlessapp/customemodel.html', params)




# ---------------------------------------------------------------------------
# Custom Funtions
# ---------------------------------------------------------------------------

part_names = ["wheels", "tires", "tire", "suspension", "exhaust", "spoiler", "spoilers", "wing", "lighting"]
colors = ["red", "black", "blue", "green", "white", "silver", "yellow", "purple", "orange", "gray", "pink", "brown", "turquoise", "gold", "maroon", "lavender", "teal", "cyan", "indigo", "violet"]


# Function to remove stop words from a chat
def remove_stop_words(chat):
    doc = nlp(chat)
    filtered_words = [token.text for token in doc if not token.is_stop]
    return " ".join(filtered_words)

# Function to perform lemmatization on a chat
def lemmatize_chat(chat):
    doc = nlp(chat)
    lemmatized_words = [token.lemma_ for token in doc]
    return " ".join(lemmatized_words)

# Function to make every word in a chat lowercase
def make_chat_lowercase(chat):
    return chat.lower()

# Function to remove symbols from a chat
def remove_symbols(chat):
    chat_without_symbols = re.sub(r'[,.\'";?@-]', '', chat)
    return chat_without_symbols

def filtertext(input_text):
    # input_text = "I'm thinking about customizing my car with black Wheels."

    # Apply all text processing steps to the input_text
    processed_text = remove_stop_words(input_text)
    processed_text = lemmatize_chat(processed_text)
    processed_text = make_chat_lowercase(processed_text)
    processed_text = remove_symbols(processed_text)

    colors_found, parts_found = extract_color_and_part_from_text(processed_text) # Extract color and part name from the input_text

    data = {
        "Input_Text" : input_text,
        "Colors" : colors_found,
        "Part_Names" : parts_found,
    }

    # print(f"Input Text: {input_text}")
    # print(f"Colors: {colors_found}")
    # print(f"Part Names: {parts_found}")

    return data

def extract_color_and_part_from_text(input_text):
    color_matches = re.findall(r'\b(?:' + '|'.join(colors) + r')\b', input_text, flags=re.IGNORECASE)
    part_matches = re.findall(r'\b(?:' + '|'.join(part_names) + r')\b', input_text, flags=re.IGNORECASE)
    return color_matches, part_matches


part_names = ["wheels", "tires", "tire", "suspension", "exhaust", "spoiler", "spoilers", "wing", "lighting"]


def changeModelColor(modelname, color):
    # Load the .glb file
    # gltf = GLTF2().load("static\spoke.glb")
    allmodel_paths = {
        "wheels"        : "formlessapp\modelfiles\wheels.glb",
        "tires"         : "formlessapp/static/formlessapp/modelfiles/wheels.glb",
        "tire"          : "wheels",
        "suspension"    : "wheels",
        "exhaust"       : "wheels",
        "spoiler"       : "wheels",
        "spoilers"      : "wheels",
        "wing"          : "wheels",
        "lighting"      : "wheels",
    }

    file_path = 'formlessapp/modelfiles/wheels.glb'  # Replace with the actual path

    # Construct the full file path
    # full_file_path = os.path.join(settings.STATIC_ROOT, file_path)



    # gltf = GLTF2().load(allmodel_paths[modelname])
    gltf = GLTF2().load(r"formlessapp\static\formlessapp\modelfiles\wheels.glb")

    material = gltf.materials[0] # Access the material

    # Define the list of colors and their corresponding RGB values
    colors = {
        "red": [1.0, 0.0, 0.0, 1.0],
        "black": [0.0, 0.0, 0.0, 1.0],
        "blue": [0.0, 0.0, 1.0, 1.0],
        "green": [0.0, 1.0, 0.0, 1.0],
        "white": [1.0, 1.0, 1.0, 1.0],
        "silver": [0.75, 0.75, 0.75, 1.0],
        "yellow": [1.0, 1.0, 0.0, 1.0],
        "purple": [0.5, 0.0, 0.5, 1.0],
        "orange": [1.0, 0.65, 0.0, 1.0],
        "gray": [0.5, 0.5, 0.5, 1.0],
        "pink": [1.0, 0.75, 0.8, 1.0],
        "brown": [0.65, 0.16, 0.16, 1.0],
        "turquoise": [0.25, 0.88, 0.82, 1.0],
        "gold": [1.0, 0.84, 0.0, 1.0],
        "maroon": [0.5, 0.0, 0.0, 1.0],
        "lavender": [0.71, 0.49, 0.86, 1.0],
        "teal": [0.0, 0.5, 0.5, 1.0],
        "cyan": [0.0, 1.0, 1.0, 1.0],
        "indigo": [0.29, 0.0, 0.51, 1.0],
        "violet": [0.93, 0.51, 0.93, 1.0]
    }

    # List of colors
    color_names = ["red", "black", "blue", "green", "white", "silver", "yellow", "purple", "orange", "gray", "pink", "brown", "turquoise", "gold", "maroon", "lavender", "teal", "cyan", "indigo", "violet"]

    # Create RGB color lists for each color
    rgb_color_lists = {color: colors[color] for color in color_names}

    # rgb_color_lists['red']
    # material.pbrMetallicRoughness.baseColorFactor = rgb_color_lists['black']
    # material.pbrMetallicRoughness.baseColorFactor = [0.0, 0.0, 0.0, 1.0]
    material.pbrMetallicRoughness.baseColorFactor = [0.0, 1.0, 0.0, 1.0]

    # Change the color
    # material.pbrMetallicRoughness.baseColorFactor = [1.0, 0.0, 0.0, 1.0] # Red color
    # material.pbrMetallicRoughness.baseColorFactor = [0.0, 1.0, 0.0, 1.0] # Green color
    # material.pbrMetallicRoughness.baseColorFactor = [0.0, 0.0, 1.0, 1.0] # Blue color


    # Save the changes
    # gltf.save(fr"formlessapp\static\formlessapp\modelfiles\{modelname}.glb")
    gltf.save(r"formlessapp\static\formlessapp\modelfiles\wheels.glb")
    

# Dictionary to map color names to RGB values
color_mapping = {
    "red": (1.0, 0.0, 0.0),
    "black": (0.0, 0.0, 0.0),
    "blue": (0.0, 0.0, 1.0),
    "green": (0.0, 1.0, 0.0),
    "white": (1.0, 1.0, 1.0),
    "silver": (0.75, 0.75, 0.75),
    "yellow": (1.0, 1.0, 0.0),
    "purple": (0.5, 0.0, 0.5),
    "orange": (1.0, 0.65, 0.0),
    "gray": (0.5, 0.5, 0.5),
    "pink": (1.0, 0.75, 0.8),
    "brown": (0.65, 0.16, 0.16),
    "turquoise": (0.25, 0.88, 0.82),
    "gold": (1.0, 0.84, 0.0),
    "maroon": (0.5, 0.0, 0.0),
    "lavender": (0.71, 0.49, 0.86),
    "teal": (0.0, 0.5, 0.5),
    "cyan": (0.0, 1.0, 1.0),
    "indigo": (0.29, 0.0, 0.51),
    "violet": (0.93, 0.51, 0.93)
}


    
def changeScenLights(color_name):
    
    all_color_names = ["red", "black", "blue", "green", "white", "silver", "yellow", "purple", "orange", "gray", "pink", "brown", "turquoise", "gold", "maroon", "lavender", "teal", "cyan", "indigo", "violet"]
    
    # color_present = False
    color_ = str(color_name[0])
    
    if color_ in all_color_names:
        rgb_values = color_mapping[color_]
        print("if - rgb_values : ", rgb_values)
        return rgb_values  # Return the RGB values as a tuple

    else:
        print("else - rgb_values : ", rgb_values)

        return (0, 0.2, 0.8)  # Default RGB values
    

    # for item in all_color_names:
    #     print("color_ : ", color_, type(color_), "item : ", str(item), type(item))
    #     if color_  == item:
    #         color_present = True
    #     else:
    #         color_present = False

    # if color_present:
    #     print("if -  fun - color_name : ", color_)
    #     rgb_values = color_mapping[color_]
    #     print("rgb_values : ", rgb_values)
    #     return rgb_values
    # else:
    #     print("else fun - color_name : ", color_)

    #     return (0, 0.2, 0.8)  # Default RGB values


    # colorDisplay.innerHTML = 'light.diffuse = new BABYLON.Color3(0, 0.2, 0.8); // Change the light color to {{ color_name }}';


    # [red, green, blue, opacity]
    # [1.0, 0.0, 0.0, 1.0] # Red color
    # [0.0, 1.0, 0.0, 1.0] # Green color
    # [0.0, 0.0, 1.0, 1.0] # Blue color






# def about(request):
#     return render(request,'formlessapp/about.html')

# def contact(request):
#     coreMem = Contact.objects.filter(mem_tag="core")
#     teamMem = Contact.objects.filter(mem_tag="team")
#     # print(f"coreMem: {coreMem} \n teamMem: {teamMem}")

#     return render(request, 'formlessapp/contact.html', {'core':coreMem,'team':teamMem })

# def productView(request, myslug):
#     # Fetch the product using the id
#     product = Product.objects.filter(slug=myslug)
#     prodCat = product[0].category
#     # print(prodCat)
#     recproduct = Product.objects.filter(category=prodCat)
#     # print(recproduct)

#     # randomObjects = random.sample(recproduct, 2)
#     randomObjects = random.sample(list(recproduct), 2)


#     return render(request, 'formlessapp/prodView.html', {'product':product[0],'recprod':randomObjects })


# def index(request):
#     return HttpResponse('Teamzeffort    |      index Page')
