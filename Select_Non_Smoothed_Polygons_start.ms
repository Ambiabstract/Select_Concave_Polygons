macroscript Select_Non_Smoothed_Polygons_start
category:"Ambiabstract_scripts"
buttontext:"Select_Non_Smoothed_Polygons_start"
tooltip:"Select_Non_Smoothed_Polygons_start"

(
    -- Initialize Python
    python.Init()

    -- Execute the Python script with the correct path
    python.ExecuteFile @"C:/Program Files/Autodesk/3ds Max 2023/scripts/Select_Non_Smoothed_Polygons.py"

    -- Log errors if they occur
    if python.GetLastError() != "" do
        print python.GetLastError()
)
