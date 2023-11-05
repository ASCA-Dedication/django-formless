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
# from pygltflib import GLTF2


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

    return render(request,'formlessapp/home.html')
    # return render(request,'formlessapp/loadobjModel.html')
    # return render(request,'formlessapp/loadModel.html')


def customemodel(request):
    # return HttpResponse('Teamzeffort    |      business Page')
    return render(request,'formlessapp/customemodel.html')

def test(request):
    # return HttpResponse('Teamzeffort    |      business Page')
    return render(request,'formlessapp/loadobjModel.html')

# Actions

@csrf_exempt  # To disable CSRF protection (not recommended for production)
def chat_view(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')  # Get the input field value
        print(f"Received input: {input_text}")  # Print the input in the terminal
        
        
        NER_result = filtertext(input_text)
        print("Chat - NER : ",NER_result)

        color_name = NER_result["Colors"][0]
        try:
            part_name = NER_result["Part_Names"][0]
            print("try - part_name selected : ", part_name)
        except:
            part_name = "tire"
        
            print("except - part_name selected : ", part_name)

        print("global - part_name selected : ", part_name)
        # changeModelColor(modelname, color_name)
        
        # changeScenLights(color_name)
        # Example usage:
        # color_name = "red"
        # light_diffuse = changeScenLights(color_name)
        # print(f'new BABYLON.Color3({light_diffuse[0]}, {light_diffuse[1]}, {light_diffuse[2]})')
        # print("light_diffuse : ", light_diffuse)

        modelname = "mclaren-tire"
        # part_name = "lambert2SG.001"
        visibility = 1.0
        Model_Edit(modelname, color_name, part_name, visibility)


        chatList.append(input_text)
        # params = {"chatList" : input_text}
        params = {
            "chatList" : chatList,
            # "light_diffuse" : light_diffuse
            }
    # return HttpResponse("Success")  # You can return any response you like
    return render(request,'formlessapp/customemodel.html', params)




# ---------------------------------------------------------------------------
# Custom Funtions
# ---------------------------------------------------------------------------

part_names = ["wheels", "wheel", "tires", "tire", "light", "exhaust","glass", "dashboard", "body", "spoiler", "spoilers", "wing", "lighting", "lights"]

colors = ["red", "black", "blue", "green", "white", "silver", "yellow", "purple", "orange", "gray", "pink", "brown", "turquoise", "gold", "maroon", "lavender", "teal", "cyan", "indigo", "violet"]

# red, black, blue, green, white, silver, yellow, purple, orange, gray, pink, brown, turquoise, gold, maroon, lavender, teal, cyan, indigo, violet


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
    # print(f"Input Text: {input_text} \t\t\t Colors: {colors_found} \t\t\t Part Names: {parts_found}")
    return data

def extract_color_and_part_from_text(input_text):
    color_matches = re.findall(r'\b(?:' + '|'.join(colors) + r')\b', input_text, flags=re.IGNORECASE)
    part_matches = re.findall(r'\b(?:' + '|'.join(part_names) + r')\b', input_text, flags=re.IGNORECASE)
    return color_matches, part_matches



    



def map_color_to_mtl(color_name, visibility=1.0):
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

    if color_name in colors:
        color_values = colors[color_name]
        print("mtl - color_name : ", color_name)
        mtlContent = {
            # 'Ns': '100.0',  # New shininess value
            'Ka': f'{color_values[0]:.6f} {color_values[1]:.6f} {color_values[2]:.6f}',  # Ambient color
            'Kd': f'{color_values[0]:.6f} {color_values[1]:.6f} {color_values[2]:.6f}',  # Diffuse color
            # 'Ks': '1.0 1.0 1.0',  # Specular color
            # 'Ke': '0.0 0.0 0.0',  # Emissive color
            # 'Ni': '1.5',  # Optical density
            'd': visibility,  # Opacity
            # 'illum': '3',  # Illumination model (3 for specular reflection)
        }
        return mtlContent
    else:
        default ={
            # 'Ns': '100.0',  # New shininess value
            'Ka': '0.1 0.0 0.0',  # New ambient color
            'Kd': '0.0 0.6 0.0',  # New diffuse color
            # 'Ks': '1.0 1.0 1.0',  # New specular color
            # 'Ke': '0.0 0.0 0.0',  # New emissive color
            # 'Ni': '1.5',  # New optical density
            'd': '1.0',  # opacity
            # 'illum': '3',  # New illumination model (3 for specular reflection)
        }
        return default

# # Example usage:
# color_name = "blue"  # Change this to the color you want
# new_material_properties = map_color_to_mtl(color_name)

# if new_material_properties:
#     print(f"New MTL properties for {color_name}:\n{new_material_properties}")
# else:
#     print(f"Color {color_name} not found in the color mapping dictionary.")


# def read_file(request):
#     file_path = 'formlessapp/modelfiles/mclaren/base.txt'  # Path relative to your app's 'static' directory

#     # Construct the full file path
#     full_file_path = os.path.join(static(""), file_path)

#     try:
#         with open(full_file_path, 'r') as file:
#             file_content = file.read()
#         return HttpResponse(file_content)
#     except FileNotFoundError:
#         return HttpResponse("File not found")



def Model_Edit(modelname, color_name, part_name, visibility):

    if modelname == "mclaren":
        mtl_file_path = "C:/Users\Atharva Pawar/Documents/GitHub/django-formless/formlessproject/formlessapp/static/formlessapp/modelfiles/maclaren-tire/tire.mtl"
    else:
        # mtl_file_path = "formlessapp/modelfiles/mclaren-tire/base.mtl"

        mtl_file_path = "C:/Users\Atharva Pawar/Documents/GitHub/django-formless/formlessproject/formlessapp/static/formlessapp/modelfiles/maclaren-tire/tire.mtl"

    # Construct the full file path
    # mtl_file_path = os.path.join(static("formlessapp"), mtl_file_path)

    # file_path = 'formlessapp/modelfiles/mclaren/base.txt'  # Path relative to your app's 'static' directory

    # Construct the full file path
    full_file_path = os.path.join(settings.STATIC_ROOT, mtl_file_path)
    print("full_file_path : ", mtl_file_path)

    # Read the existing MTL file and store its content in memory
    with open(mtl_file_path, 'r') as mtl_file:
        mtl_lines = mtl_file.readlines()

    '''
    # Define the new values you want to set for the "Material.008" entry
    new_material_properties = {
        'Ns': '100.0',  # New shininess value
        'Ka': '0.1 0.0 0.0',  # New ambient color
        'Kd': '0.0 0.6 0.0',  # New diffuse color
        'Ks': '1.0 1.0 1.0',  # New specular color
        'Ke': '0.0 0.0 0.0',  # New emissive color
        'Ni': '1.5',  # New optical density
        'd': '1.0',  # opacity
        'illum': '3',  # New illumination model (3 for specular reflection)
    }
    '''

    # Find and modify the "Material.008" entry in the MTL file
    # material_name = "Material.008"

    new_material_properties = map_color_to_mtl(color_name, visibility)

    # part_names = ["wheels", "wheel", "tires", "tire", "light", "exhaust","glass", "dashboard", "body", "spoiler", "spoilers", "wing", "lighting", "lights"]

    model_parts_names = {
    "wheels" : "lambert2SG.001",
    "wheel" : "lambert2SG.001",
    "tire" : "lambert2SG.001",
    "tires" : "lambert2SG.001",
    "light" : "Material.012, Material.011, Material.009",
    "lights" : "Material.012, Material.011, Material.009",
    "lighting" : "Material.012, Material.011, Material.009",
    "exhaust" : "Material.008",
    "glass" : "Material.003",
    "dashboard" : "Material.002",
    "body" : "Material.001",
    }

    

    material_name = model_parts_names[part_name]
    print("render html file : ", material_name)
    in_material = False

    for i, line in enumerate(mtl_lines):
        if line.startswith('newmtl ') and line.split()[1] == material_name:
            in_material = True
        elif in_material:
            # Stop when reaching the next "newmtl" entry
            if line.startswith('newmtl '):
                in_material = False
                break
            else:
                # Update the properties in memory
                for key, value in new_material_properties.items():
                    if line.startswith(key):
                        mtl_lines[i] = f'{key} {value}\n'

    # Write the updated content back to the MTL file
    with open(mtl_file_path, 'w') as mtl_file:
        mtl_file.writelines(mtl_lines)

    print(f"Updated material '{material_name}' in the MTL file.")
    















'''
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

'''


'''
def about(request):
    return render(request,'formlessapp/about.html')

def contact(request):
    coreMem = Contact.objects.filter(mem_tag="core")
    teamMem = Contact.objects.filter(mem_tag="team")
    # print(f"coreMem: {coreMem} \n teamMem: {teamMem}")

    return render(request, 'formlessapp/contact.html', {'core':coreMem,'team':teamMem })

def productView(request, myslug):
    # Fetch the product using the id
    product = Product.objects.filter(slug=myslug)
    prodCat = product[0].category
    # print(prodCat)
    recproduct = Product.objects.filter(category=prodCat)
    # print(recproduct)

    # randomObjects = random.sample(recproduct, 2)
    randomObjects = random.sample(list(recproduct), 2)


    return render(request, 'formlessapp/prodView.html', {'product':product[0],'recprod':randomObjects })


def index(request):
    return HttpResponse('Teamzeffort    |      index Page')

'''