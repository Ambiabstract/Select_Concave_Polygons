macroscript Select_Non_Quad_Ngons_start
category:"Ambiabstract_scripts"
buttontext:"Select_Non_Quad_Ngons_start"
tooltip:"Select_Non_Quad_Ngons_start"

(
    -- Initialize Python
    python.Init()

    -- Execute the Python script with the correct path
    python.ExecuteFile @"C:/Program Files/Autodesk/3ds Max 2023/scripts/Select_Non_Quad_Ngons.py"

    -- Log errors if they occur
    if python.GetLastError() != "" do
        print python.GetLastError()
)
