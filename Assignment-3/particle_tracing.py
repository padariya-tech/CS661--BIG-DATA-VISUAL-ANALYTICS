#!/usr/bin/env python
# coding: utf-8


import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
import matplotlib.pyplot as plt

# Function to perform Runge-Kutta 4th order (RK4) integration
def rk4_integration( seed, step_size, max_steps, boundry,data):
    streamline = [seed]
    step = 0
    while step < max_steps:
        if not all(boundry[i] <= seed[i] <= boundry[i + 1] for i in range(0, 3, 2)):
            break  # Stop if the seed is out of boundary
        k1 = step_size * get_vector_at_location(seed,data)
        k2 = step_size * get_vector_at_location(seed + k1 / 2,data)
        k3 = step_size * get_vector_at_location(seed + k2 / 2,data)
        k4 = step_size * get_vector_at_location(seed + k3,data)
        next_pt = seed + (k1 + 2*k2 + 2*k3 + k4) / 6
        streamline.append(seed)
        seed = next_pt
        step += 1
    return streamline



def get_vector_at_location(location,data):  # Function to get vector at a point
    probe = vtk.vtkProbeFilter()  # Create the probe filter
    probe.SetSourceData(data)  # Set the source data

    locations = vtk.vtkPoints()  # Create the points
    locations.InsertNextPoint(location.tolist())  # Insert the point
    polydata = vtk.vtkPolyData()  # Create the polydata
    polydata.SetPoints(locations)  # Set the points
 
    probe.SetInputData(polydata)  # Set the input
    probe.Update()  # Update the filter 0

    probed_data = probe.GetOutput()  # Get the output
    vectors = vtk_to_numpy(probed_data.GetPointData().GetVectors())  # Convert the vectors to a numpy array

    return vectors[0] if vectors is not None else np.array([0.0, 0.0, 0.0]) # Return the vector at the queried point

# Load the vector field dataset
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName("tornado3d_vector.vti")  # Use the uploaded file path
reader.Update()
data = reader.GetOutput()

# print(bounds)

# get seed input from
# Input format: x y z
coordinates = input("Enter the coordinates (x y z): ")
coordinates_list = coordinates.split()  # Split the input into a list of strings
seed_point = np.array([float(coord) for coord in coordinates_list])


# Seed point, step size, and max steps as per the assignment specifications
# seed_point = np.array([0, 0, 7])
step_size_RK4 = 0.05
max_steps_RK4 = 1000

# Perform the Runge-Kutta 4th order integration
# Generate streamline
streamline_forward = rk4_integration( seed_point, step_size_RK4, max_steps_RK4,data.GetBounds(),data)
streamline_backward = rk4_integration( seed_point, -step_size_RK4, max_steps_RK4,data.GetBounds(),data)


# Combine forward and backward streamlines
streamline = list(reversed(streamline_backward)) + streamline_forward


# Convert streamline to VTKPolyData
coordinates = vtk.vtkPoints()
lines = vtk.vtkCellArray()

_ = [(
    coordinates.InsertNextPoint(point.tolist()),
    lines.InsertNextCell(2, [i - 1, i]) if i > 0 else None
) for i, point in enumerate(streamline)]

polyData = vtk.vtkPolyData()
polyData.SetPoints(coordinates)
polyData.SetLines(lines)


writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName("particle_tracing.vtp")
writer.SetInputData(polyData)
writer.Write()




#The below code visualises the data i here itself 
# import plotly.graph_objects as go

# streamline_points = np.array(streamline)  # Convert streamline points for plotting

# fig = go.Figure()

# # Add trace for the streamline
# fig.add_trace(go.Scatter3d(
#     x=streamline_points[:, 0],
#     y=streamline_points[:, 1],
#     z=streamline_points[:, 2],
#     mode='lines',
#     line=dict(color='green', width=2),
#     name='Streamline'
# ))

# # Set layout properties
# fig.update_layout(
#     title='3D Streamline Visualization',
#     scene=dict(
#         xaxis=dict(title='X'),
#         yaxis=dict(title='Y'),
#         zaxis=dict(title='Z')
#     )
# )

# # Show the interactive plot
# fig.show()







