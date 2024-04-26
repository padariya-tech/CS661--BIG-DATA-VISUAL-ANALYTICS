import vtk


## Load data
#######################################
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName('isabel_3D.vti')
reader.Update()
data = reader.GetOutput()
# print(data)

# numCells = data.GetNumberOfCells()
# print("number of cells = ",numCells)

## Create volume color
volumeColor = vtk.vtkColorTransferFunction()
volumeColor.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)
volumeColor.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
volumeColor.AddRGBPoint(-1873.9, 0.0, 0.0, 0.5)
volumeColor.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)
volumeColor.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)
volumeColor.AddRGBPoint(2594.97, 1.0, 1.0, 0.0)

## Create scalar opacity
volumeScalarOpacity = vtk.vtkPiecewiseFunction()
volumeScalarOpacity.AddPoint(-4931.54, 1.00)
volumeScalarOpacity.AddPoint(101.815, 0.002) 
volumeScalarOpacity.AddPoint(2594.97, 0.0)

## Create volume property
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(volumeColor)
volumeProperty.SetScalarOpacity(volumeScalarOpacity)
volumeProperty.SetInterpolationTypeToLinear() 

## ask user to give value of phong  want to see or not
user_input = input("Enter 1 to see Phong, 0 to not: ")
if user_input == '1':
    volumeProperty.ShadeOn()
    volumeProperty.SetAmbient(0.5)
    volumeProperty.SetDiffuse(0.5)
    volumeProperty.SetSpecular(0.5)

## Create volume mapper
volumeMapper = vtk.vtkSmartVolumeMapper()
volumeMapper.SetInputData(reader.GetOutput())

## Create outline
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())
actor2 = vtk.vtkActor()
actor2.SetMapper(outlineMapper)
actor2.GetProperty().SetColor(1.0,1.0,1.0)

## Create volume
volume = vtk.vtkVolume()
volume.SetProperty(volumeProperty) 
volume.SetMapper(volumeMapper)



## Create renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.5,0.5,0.5)
renderer.AddVolume(volume)
renderer.AddActor(actor2)

## Create render window
render_window = vtk.vtkRenderWindow()
render_window.SetSize(800, 800)
render_window.AddRenderer(renderer)

## Create interactor
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

## Start interactor
render_window_interactor.Start()
