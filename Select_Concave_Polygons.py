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

    #print(f"Checking polygon {poly_index}:")
    #print(f" - Vertices: {verts}")

    # Iterate over the triangular parts of the polygon
    for i in range(len(poly_points)):
        # Current triangle
        tri_points = [
            poly_points[i],
            poly_points[(i + 1) % len(poly_points)],
            poly_points[(i + 2) % len(poly_points)],
        ]

        # Check if any other vertex is inside this triangle
        for j in range(len(poly_points)):
            if j not in {i, (i + 1) % len(poly_points), (i + 2) % len(poly_points)}:
                point = poly_points[j]
                if is_point_inside_triangle(point, tri_points):
                    #print(f"Polygon {poly_index} is identified as concave.")
                    return True

    #print(f"Polygon {poly_index} is convex.")
    return False


def select_concave_polygons_by_containment():
    """
    Finds and selects concave polygons using containment testing.
    """
    selected_objs = rt.selection
    if len(selected_objs) != 1:
        rt.messageBox("Please select one Editable Poly object.", title="Error")
        return

    obj = selected_objs[0]

    if not rt.isKindOf(obj, rt.Editable_Poly):
        rt.messageBox("The selected object is not an Editable Poly.", title="Error")
        return

    face_count = rt.polyOp.getNumFaces(obj)
    concave_faces = rt.BitArray(face_count)  # Set the correct size for the array
    print(f"Checking {face_count} polygons.")

    # Clear all flags in the BitArray
    for i in range(0, face_count):  # Start at 0 for BitArray
        concave_faces[i] = False

    # Iterate over all polygons
    for i in range(1, face_count + 1):  # Indexing starts at 1 in 3ds Max
        try:
            if is_polygon_concave_by_containment(obj, i):
                concave_faces[i - 1] = True  # Shift index by 1 for BitArray
        except RuntimeError as e:
            print(f"Error processing polygon {i}: {e}")
            continue

    # Output information
    if concave_faces.numberset > 0:
        rt.polyOp.setFaceSelection(obj, concave_faces)
        rt.redrawViews()
        print(f"{concave_faces.numberset} concave polygons selected.")
    else:
        rt.messageBox("No concave polygons found.", title="Result")


# Execute
select_concave_polygons_by_containment()
