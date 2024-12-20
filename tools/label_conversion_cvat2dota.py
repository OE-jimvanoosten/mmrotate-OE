import os
import xml.etree.ElementTree as ET
import math

def convert_xml_to_txt(xml_file_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    for image in root.findall("image"):
        image_name = image.get("name")
        image_width = float(image.get("width"))
        image_height = float(image.get("height"))

        txt_file_name = os.path.splitext(image_name)[0] + ".txt"
        txt_file_path = os.path.join(output_folder, txt_file_name)

        with open(txt_file_path, "w") as txt_file:
            for box in image.findall("box"):
                label = box.get("label")
                xtl = float(box.get("xtl"))
                ytl = float(box.get("ytl"))
                xbr = float(box.get("xbr"))
                ybr = float(box.get("ybr"))
                rotation = float(box.get("rotation"))

                # Calculate the rotated box coordinates
                cx, cy = (xtl + xbr) / 2, (ytl + ybr) / 2
                w, h = xbr - xtl, ybr - ytl
                angle_rad = math.radians(rotation)

                dx = w / 2
                dy = h / 2

                corners = [
                    (-dx, -dy),
                    (dx, -dy),
                    (dx, dy),
                    (-dx, dy)
                ]

                rotated_corners = []
                for corner in corners:
                    rx = cx + corner[0] * math.cos(angle_rad) - corner[1] * math.sin(angle_rad)
                    ry = cy + corner[0] * math.sin(angle_rad) + corner[1] * math.cos(angle_rad)
                    rotated_corners.append((rx, ry))

                # Write the coordinates and label to the TXT file
                txt_file.write(
                    "{} {} {} {} {} {} {} {} {} 1\n".format(
                        *[f"{round(coord, 1)}" for point in rotated_corners for coord in point],
                        label
                    )
                )

# Specify the input XML file and output folder
xml_file = "/home/jim.vanoosten/annotations.xml"
output_folder = "/home/jim.vanoosten/annfiles"

convert_xml_to_txt(xml_file, output_folder)
print(f"Converted annotations saved in folder: {output_folder}")
