import pymxs

rt = pymxs.runtime


def vector_from_points(p1, p2):
    """Creates a vector from two points."""
    return rt.Point3(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)


def cross_product(v1, v2):
    """Computes the cross product of two vectors."""
    return rt.cross(v1, v2)


def is_point_inside_triangle(point, tri_points):
    """
    Checks if a point lies inside a triangle.
    Uses the cross product to check all edges.
    """
    a, b, c = tri_points

    # Vectors for triangle edges
    ab = vector_from_points(a, b)
    bc = vector_from_points(b, c)
    ca = vector_from_points(c, a)

    # Vectors from the point to the triangle vertices
    ap = vector_from_points(a, point)
    bp = vector_from_points(b, point)
    cp = vector_from_points(c, point)

    # Cross products
    cross_ab_ap = cross_product(ab, ap)
    cross_bc_bp = cross_product(bc, bp)
    cross_ca_cp = cross_product(ca, cp)

    # Check the signs of all cross products
    return (rt.dot(cross_ab_ap, cross_bc_bp) > 0) and (rt.dot(cross_ab_ap, cross_ca_cp) > 0)


def is_polygon_concave_by_containment(poly_obj, poly_index):
    """
    Checks if a polygon is concave by vertex containment testing.
    """
    verts = rt.polyOp.getFaceVerts(poly_obj, poly_index)
    poly_points = [rt.polyOp.getVert(poly_obj, v) for v in verts]

    # Exclude triangles
    if len(poly_points) <= 3:
        return False

    for i in range(len(poly_points)):
        tri_points = [
            poly_points[i],
            poly_points[(i + 1) % len(poly_points)],
            poly_points[(i + 2) % len(poly_points)],
        ]

        for j in range(len(poly_points)):
            if j not in {i, (i + 1) % len(poly_points), (i + 2) % len(poly_points)}:
                point = poly_points[j]
                if is_point_inside_triangle(point, tri_points):
                    return True

    return False


def select_concave_polygons_by_containment():
    """
    Finds and selects concave polygons using containment testing.
    """
    selected_objs = rt.selection
    if not selected_objs:
        rt.messageBox("Please select at least one object.", title="Error")
        return

    total_concave_faces = 0

    for obj in selected_objs:
        # Check if the object is Editable Poly or has an Edit Poly modifier
        if not (rt.isKindOf(obj, rt.Editable_Poly) or has_edit_poly_modifier(obj)):
            print(f"Skipping object {obj.name} - not Editable Poly or Edit Poly.")
            continue

        # Convert to Editable Poly if it has Edit Poly modifier
        if has_edit_poly_modifier(obj):
            rt.convertTo(obj, rt.Editable_Poly)

        face_count = rt.polyOp.getNumFaces(obj)
        concave_faces = rt.BitArray(face_count)

        for i in range(face_count):
            concave_faces[i] = False

        for i in range(1, face_count + 1):
            try:
                if is_polygon_concave_by_containment(obj, i):
                    concave_faces[i - 1] = True
            except RuntimeError as e:
                print(f"Error processing polygon {i} in object {obj.name}: {e}")
                continue

        if concave_faces.numberset > 0:
            rt.polyOp.setFaceSelection(obj, concave_faces)
            total_concave_faces += concave_faces.numberset
            print(f"{concave_faces.numberset} concave polygons found in object {obj.name}.")
        else:
            print(f"No concave polygons found in object {obj.name}.")

    if total_concave_faces > 0:
        rt.redrawViews()
        print(f"Total {total_concave_faces} concave polygons selected.")
    else:
        rt.messageBox("No concave polygons found in the selected objects.", title="Result")


def has_edit_poly_modifier(obj):
    """
    Checks if the object has an Edit Poly modifier applied.
    """
    if not rt.isValidNode(obj):
        return False

    try:
        # Iterate over all modifiers on the object
        for mod in obj.modifiers:
            if rt.classOf(mod) == rt.Edit_Poly:
                return True
    except Exception as e:
        print(f"Error while checking modifiers for object {obj.name}: {e}")
    return False


# Execute
select_concave_polygons_by_containment()
