import pymxs

rt = pymxs.runtime

def select_polygons_with_five_or_more_vertices():
    """
    Finds and selects polygons with 5 or more vertices.
    Triangles and quads are ignored.
    """
    selected_objs = rt.selection
    if not selected_objs:
        rt.messageBox("Please select at least one object.", title="Error")
        return

    total_selected_faces = 0

    for obj in selected_objs:
        # Check if the object is Editable Poly or has an Edit Poly modifier
        if not (rt.isKindOf(obj, rt.Editable_Poly) or has_edit_poly_modifier(obj)):
            print(f"Skipping object {obj.name} - not Editable Poly or Edit Poly.")
            continue

        # Convert to Editable Poly if it has an Edit Poly modifier
        if has_edit_poly_modifier(obj):
            rt.convertTo(obj, rt.Editable_Poly)

        face_count = rt.polyOp.getNumFaces(obj)
        selected_faces = rt.BitArray(face_count)

        for i in range(face_count):
            selected_faces[i] = False

        for i in range(1, face_count + 1):
            try:
                verts = rt.polyOp.getFaceVerts(obj, i)
                if len(verts) >= 5:
                    selected_faces[i - 1] = True
            except RuntimeError as e:
                print(f"Error processing polygon {i} in object {obj.name}: {e}")
                continue

        if selected_faces.numberset > 0:
            rt.polyOp.setFaceSelection(obj, selected_faces)
            total_selected_faces += selected_faces.numberset
            print(f"{selected_faces.numberset} polygons with 5 or more vertices found in object {obj.name}.")
        else:
            print(f"No polygons with 5 or more vertices found in object {obj.name}.")

    if total_selected_faces > 0:
        rt.redrawViews()
        print(f"Total {total_selected_faces} polygons with 5 or more vertices selected.")
    else:
        rt.messageBox("No polygons with 5 or more vertices found in the selected objects.", title="Result")


def has_edit_poly_modifier(obj):
    """
    Checks if the object has an Edit Poly modifier.
    """
    if not rt.isValidNode(obj):
        return False

    try:
        for mod in obj.modifiers:
            if rt.classOf(mod) == rt.Edit_Poly:
                return True
    except Exception as e:
        print(f"Error while checking modifiers for object {obj.name}: {e}")
    return False


# Execute the script
select_polygons_with_five_or_more_vertices()
