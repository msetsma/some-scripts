import argparse
import os
import trimesh
import numpy as np

from svgpathtools import svg2paths


def svg_to_3d(svg_file, height_mm, depth_mm, width_mm, output_file):
    # Parse SVG file
    paths, _ = svg2paths(svg_file)
    
    # Create a 2D polygon from the SVG paths
    points = []
    for path in paths:
        points.extend([complex(p.real, p.imag) for p in path.point(np.linspace(0, 1, 100))])
    
    # Convert complex numbers to 2D points
    points_2d = [(p.real, p.imag) for p in points]
    
    # Create a 2D mesh
    mesh_2d = trimesh.creation.extrude_polygon(points_2d, height_mm)
    
    # Scale the mesh to the desired width and depth in mm
    scale_x = width_mm / mesh_2d.extents[0]
    scale_y = depth_mm / mesh_2d.extents[1]
    scale_z = 1  # Height is already set
    mesh_2d.apply_scale([scale_x, scale_y, scale_z])
    
    # Export the 3D mesh
    mesh_2d.export(output_file)

def main():
    parser = argparse.ArgumentParser(description="Convert SVG to 3D file (dimensions in mm)")
    parser.add_argument("svg_file", help="Input SVG file")
    parser.add_argument("height_mm", type=float, help="Height of the 3D object in mm")
    parser.add_argument("depth_mm", type=float, help="Depth of the 3D object in mm")
    parser.add_argument("width_mm", type=float, help="Width of the 3D object in mm")
    parser.add_argument("output_file", help="Output 3D file (e.g., output.stl)")
    
    args = parser.parse_args()
    
    svg_to_3d(args.svg_file, args.height_mm, args.depth_mm, args.width_mm, args.output_file)
    print(f"3D file created: {args.output_file}")
    print(f"Dimensions: {args.width_mm}mm x {args.depth_mm}mm x {args.height_mm}mm")

if __name__ == "__main__":
    main()