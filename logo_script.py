from PIL import Image
import os


def create_icon_files(src_path, dist_path):
    # Ensure the source logo.png exists
    logo_path = os.path.join(src_path, "nadoo_whisperer.png")
    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"The source file {logo_path} does not exist.")

    # Open the source image
    img = Image.open(logo_path)

    # Define icon sizes for .ico file
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

    # Create the .ico file
    img.save(
        os.path.join(dist_path, "nadoo_whisperer.ico"), format="ICO", sizes=icon_sizes
    )

    # For .icns, macOS typically uses 10 different sizes
    icns_sizes = [16, 32, 64, 128, 256, 512, 1024]
    iconset_path = os.path.join(dist_path, "nadoo_whisperer.iconset")
    os.makedirs(iconset_path, exist_ok=True)

    for size in icns_sizes:
        icon = img.resize((size, size), Image.LANCZOS)
        icon.save(os.path.join(iconset_path, f"icon_{size}x{size}.png"))

    # Use `iconutil` to create the .icns file from the .iconset directory
    os.system(
        f'iconutil -c icns {iconset_path} -o {os.path.join(dist_path, "nadoo_whisperer.icns")}'
    )

    # Clean up the .iconset directory after creating the .icns file
    for file in os.listdir(iconset_path):
        os.remove(os.path.join(iconset_path, file))
    os.rmdir(iconset_path)


# Paths
source_path = "."
dist_path = "nadoo_whisperer_extension/icons"

# Create the icon files
create_icon_files(source_path, dist_path)
