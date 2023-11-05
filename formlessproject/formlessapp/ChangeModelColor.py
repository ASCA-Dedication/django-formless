# Define the path to the MTL file you want to update
mtl_file_path = "static/mclaren/base.mtl"

# Read the existing MTL file and store its content in memory
with open(mtl_file_path, 'r') as mtl_file:
    mtl_lines = mtl_file.readlines()

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

# Find and modify the "Material.008" entry in the MTL file
# material_name = "Material.008"
material_name = "Material.001"
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
