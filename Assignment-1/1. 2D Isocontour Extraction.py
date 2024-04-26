#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install vtk


# In[16]:


## This program shows how to load a VTK Image data with extension *.vti and then
## how to access the cell data, extract one cell from the list of cells,
## access data values at each cell corner and then store the cell into a 
## vtkpolydata file format.
#################################################################################

## Import VTK
from vtk import *

## Load data
#######################################
reader = vtkXMLImageDataReader()
reader.SetFileName('isabel_2D.vti')
reader.Update()
data = reader.GetOutput()
# print(data)
## Query how many cells the dataset has
#######################################
numCells = data.GetNumberOfCells()
print("number of cells = ",numCells)

def linear_interpolation(p1, p2, v1, v2, c,data):
    x_cordinate= (v1-c)/(v1-v2)*(data.GetPoint(p2)[0]-data.GetPoint(p1)[0])+data.GetPoint(p1)[0];
    y_cordinate=    (v1-c)/(v1-v2)*(data.GetPoint(p2)[1]-data.GetPoint(p1)[1])+data.GetPoint(p1)[1];
    z_cordinate=(v1-c)/(v1-v2)*(data.GetPoint(p2)[2]-data.GetPoint(p1)[2])+data.GetPoint(p1)[2];
    return [x_cordinate,y_cordinate,z_cordinate]

# dim= data.GetDimensions()
# print(dim[0],dim[1],dim[2])


points = vtkPoints()  ## Create a vtkPoints object and store the points in it
dataArray = vtkFloatArray() ## The Data Array for holding data values
dataArray.SetName('Pressure')

c = int(input("Enter C value: ")) 
count =0
for i in range(numCells):
        
    cell = data.GetCell(i) ## cell index = 0

    ## Query the 4 corner points of the cell
    #########################################
    pid1 = cell.GetPointId(0)
    pid2 = cell.GetPointId(2)
    pid3 = cell.GetPointId(3)
    pid4 = cell.GetPointId(1)


    ## Extract the cell data values
    dataArr = data.GetPointData().GetArray('Pressure')
    val1 = dataArr.GetTuple1(pid1)
    val2 = dataArr.GetTuple1(pid2)
    val3 = dataArr.GetTuple1(pid3)
    val4 = dataArr.GetTuple1(pid4)
     
     ## Extract the cell data values
    cel=[0,0,0,0]
    if val1 > c: cel[0] = 1
    if val2 > c: cel[1] = 1
    if val3 > c: cel[2] = 1
    if val4 > c: cel[3] = 1

    ## Store the data values in the Data Array
    dataArray.InsertNextTuple1(val1)
    dataArray.InsertNextTuple1(val2)
    dataArray.InsertNextTuple1(val3)
    dataArray.InsertNextTuple1(val4)
#     print(cel) 
#
    match cel: ## match the cell 
                case [0, 0, 0, 0]:
                    pass
                case [0, 0, 0, 1]:
                    d1 = linear_interpolation(pid4,pid1,val4, val1,c,data)
                    d2 = linear_interpolation(pid4,pid3,val4, val3,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                    

                case [0, 0, 1, 0]:
                    d1 = linear_interpolation(pid3,pid2,val3, val2,c,data)
                    d2 = linear_interpolation(pid3,pid4,val3, val4,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                case [0, 0, 1, 1]:
                    d1 = linear_interpolation(pid4, pid1,val4, val1,c,data)
                    d2 = linear_interpolation(pid3, pid2,val3, val2,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                case [0, 1, 0, 0]:
                    d1 = linear_interpolation(pid2, pid1,val2, val1,c,data)
                    d2 = linear_interpolation(pid2, pid3,val2, val3,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                case [0, 1, 0, 1]:
                    d1 = linear_interpolation(pid2,pid1,val2, val1,c,data)
                    d2 = linear_interpolation(pid2,pid3,val2, val3,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                case [0, 1, 1, 0]:
                    d1 = linear_interpolation(pid2,pid1,val2, val1,c,data)
                    d2 = linear_interpolation(pid3,pid4,val3, val4,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                case [0, 1, 1, 1]:
                    d1 = linear_interpolation(pid2, pid1,val2, val1,c,data)
                    d2 = linear_interpolation(pid4,pid1,val4, val1,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                case [1, 0, 0, 0]:
                    d1 = linear_interpolation(pid1,pid2,val1, val2,c,data)
                    d2 = linear_interpolation(pid1,pid4,val1, val4,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                case [1, 0, 0, 1]:
                    d1 = linear_interpolation(pid1,pid2,val1, val2,c,data)
                    d2 = linear_interpolation(pid4,pid3,val4, val3,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                case [1, 0, 1, 0]:
                    d1 = linear_interpolation(pid1,pid2,val1, val2,c,data)
                    d2 = linear_interpolation(pid3,pid2,val3, val2,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                    pass
                case [1, 0, 1, 1]:
                    d1 = linear_interpolation(pid1, pid2,val1, val2,c,data)
                    d2 = linear_interpolation(pid3,pid2,val3, val2,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                case [1, 1, 0, 0]:
                    d1 = linear_interpolation(pid1,pid4,val1, val4,c,data)
                    d2 = linear_interpolation(pid2,pid3,val2, val3,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                case [1, 1, 0, 1]:
                    d1 = linear_interpolation(pid2,pid3,val2, val3,c,data)
                    d2 = linear_interpolation(pid4,pid3,val4, val3,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                case [1, 1, 1, 0]:
                    d1 = linear_interpolation(pid1,pid4,val1, val4,c,data)
                    d2 = linear_interpolation(pid3,pid4,val3, val4,c,data)
                    points.InsertNextPoint(d1)
                    points.InsertNextPoint(d2)
                case [1, 1, 1, 1]:
                    pass 



# create the polyLine object ....
poly_line = vtkPolyLine()
# Add point ids to the polyLine
num_of_points = points.GetNumberOfPoints()
## insert the points....
cells = vtkCellArray()
for i in range(0,num_of_points,2):

   
    poly_line.GetPointIds().SetNumberOfIds(2)
    poly_line.GetPointIds().SetId(0,i)
    poly_line.GetPointIds().SetId(1,i+1)
    # insert the polyLine....
    cells.InsertNextCell(poly_line)

# create the polyData object ....
p_data = vtkPolyData()
# Add points and cells to polydata
p_data.SetPoints(points)
p_data.SetLines(cells)



# write the polydata to the disk....
writer = vtkXMLPolyDataWriter()
writer.SetFileName("isocontour.vtp")
writer.SetInputData(p_data)
writer.Write()


### Load Data
########################
reader = vtkXMLPolyDataReader()
reader.SetFileName('isocontour.vtp') ## polyline.vtp
reader.Update()## update the reader

### get polydata object out from reader
#######################################
pdata = reader.GetOutput()
print(pdata)


### Setup mapper and actor
##########################
mapper = vtkPolyDataMapper()
mapper.SetInputData(pdata)
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetLineWidth(5) ## set line width
actor.GetProperty().SetColor(1,0,5) ## set line color red


### Setup render window, renderer, and interactor
##################################################
renderer = vtkRenderer()
renderer.SetBackground(1,1,1)
renderWindow = vtkRenderWindow()
renderWindow.SetSize(800,800)
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderer.AddActor(actor)


### Finally render the object
#############################
renderWindow.Render()
renderWindowInteractor.Start()


# In[ ]:





# In[ ]:




