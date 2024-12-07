import numpy as np
import re
# Function to load the .off file
def load_off_file(file_path):
    if 'augmented' not in file_path :
        with open(file_path, 'r') as f:
            lines = f.readlines()
    
        # Check if the first line contains "OFF"
        if 'OFF' not in lines[0].strip():
            raise ValueError(f"Not a valid OFF file: {lines[0].strip()}")
    
        try:
            numbers = lines[1].strip().split()

            # Convert the found strings to integers
        
            num_vertices = int(float(numbers[0]))
            num_faces = int(float(numbers[1]))
            num_edges = int(float(numbers[2]))

        except ValueError as e:
            raise ValueError("Error parsing the number of vertices, faces, or edges") from e

    # Validate counts
    if num_vertices < 0 or num_faces < 0 or num_edges < 0:
        raise ValueError(f"Invalid counts: vertices={num_vertices}, faces={num_faces}, edges={num_edges}")
    
    # Load vertices
    vertices = []
    for i in range(2, 2 + num_vertices):
        vertices.append([float(coord) for coord in lines[i].strip().split()])
    return np.array(vertices), lines[2 + num_vertices:]

# Function to save the object back to an .off file
def save_off_file(vertices, faces, output_path):
    with open(output_path, 'w') as f:
        f.write('OFF\n')
        f.write(f"{vertices.shape[0]} {len(faces)} 0\n")
        for vertex in vertices:
            f.write(f"{vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            f.write(face)

# Rotation matrices for X, Y, and Z axes
def rotate_x(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def rotate_y(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def rotate_z(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

# Function to apply rotation to the vertices
def rotate_object(vertices, angle_x=0, angle_y=0, angle_z=0):
    Rx = rotate_x(angle_x)
    Ry = rotate_y(angle_y)
    Rz = rotate_z(angle_z)
    
    # Apply the rotations
    rotated_vertices = vertices @ Rx.T @ Ry.T @ Rz.T
    return rotated_vertices

# Main augmentation function
def augment_off_file(input_file, output_file, angle_x=0, angle_y=0, angle_z=0):
    vertices, faces = load_off_file(input_file)
    
    # Rotate the object
    rotated_vertices = rotate_object(vertices, angle_x, angle_y, angle_z)
    
    # Save the augmented object
    save_off_file(rotated_vertices, faces, output_file)

# Example of augmenting with random rotations
import random
import os
num_augmented_objects = 2

BASE_FOLDER = r"ModelNet40" 
categories = ['airplane', 'bathtub', 'bed', 'bookshelf', 'bottle', 'chair', 'cone', 'desk', 'door', 'dresser']
SUB_FOLDER_TRAIN = r"train"

for category in categories :
    category_path = os.path.join(BASE_FOLDER, CATEGORY)
    train_path = os.path.join(category_path, SUB_FOLDER_TRAIN)
    for j, object in enumerate(os.listdir(train_path)) :
        object_path = os.path.join(train_path, object)
    
        print(object_path)

        for i in range(num_augmented_objects) :
            angle_x = random.uniform(0, np.pi/4)  # Random rotation around X-axis
            angle_y = random.uniform(0, np.pi/4)  # Random rotation around Y-axis
            angle_z = random.uniform(0, np.pi/4)  # Random rotation around Z-axis
    
            output_off_file = os.path.join(train_path , f"{j}_{i}.off")
            augment_off_file(object_path, output_off_file, angle_x, angle_y, angle_z)