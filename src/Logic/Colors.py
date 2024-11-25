import flet as ft
from flet_contrib.color_picker import ColorPicker 

# Class representing an RGB color model
class MyColorRGB:
    def __init__(self, r, g, b) -> None:
        """
        Initializes an RGB color instance.

        Args:
            r (int): Red component (0-255)
            g (int): Green component (0-255)
            b (int): Blue component (0-255)
        """
        self.red = r
        self.green = g
        self.blue = b

# Function to convert RGB to Hexadecimal
def RGB_to_hex(color: MyColorRGB):
    """
    Converts an RGB color into a hexadecimal string.

    Args:
        color (MyColorRGB): An instance of MyColorRGB representing the color.

    Returns:
        str: The hexadecimal representation of the color in the format "#rrggbb".
    """
    # Convert each number to its hexadecimal representation
    hex_r = format(color.red, '02x')
    hex_g = format(color.green, '02x')
    hex_b = format(color.blue, '02x')
    
    # Combine the hex values into a single string
    hex_color = f"#{hex_r}{hex_g}{hex_b}"
    
    return hex_color

# Function to convert Hexadecimal to RGB
def hex_to_RGB(hex_color: str):
    """
    Converts a hexadecimal color string to an RGB color.

    Args:
        hex_color (str): Hexadecimal color string, e.g. "#ff0000".

    Returns:
        MyColorRGB: An instance of MyColorRGB with the corresponding RGB values.
    """
    # Remove '#' if present
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]

    # Split the string into red, green, and blue components
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    return MyColorRGB(r, g, b)

# Class for a custom color picker container
class MyColorPicker(ft.Container):

    def __init__(self) -> None:
        """
        Initializes a custom color picker container using Flet's ColorPicker widget.
        """
        super().__init__(
            content=ColorPicker(width=200)  # Create the ColorPicker widget
        )
    
    def set_color(self, color: MyColorRGB):
        """
        Set the current color in the color picker to a specified RGB color.

        Args:
            color (MyColorRGB): The RGB color to be set in the color picker.
        """
        color_hex = RGB_to_hex(color)
        self.content.color = color_hex
        self.content.update()  # Update the UI with the new color

    def get_color(self):
        """
        Get the current color from the color picker.

        Returns:
            MyColorRGB: The current color in the picker, converted to RGB format.
        """
        color_hex = self.content.color
        color_rgb = hex_to_RGB(color_hex)
        return MyColorRGB(color_rgb.red, color_rgb.green, color_rgb.blue)

    def update_color(self, color: MyColorRGB):
        """
        Update the color picker with a new RGB color.

        Args:
            color (MyColorRGB): The RGB color to update in the color picker.
        """
        color_hex = RGB_to_hex(color)
        self.content.color = color_hex


#=
#def main(page : ft.page):
#    color_picker = MyColorPicker()
#    def cambiar_color():
#        print(RGB_to_hex(color_picker.get_color()))
#        print(color_picker.set_color(MyColorRGB(100, 10, 10)),"\n"*10)
#          
#    boton = ft.TextButton(
#          text = "Cambiar",
#          on_click= lambda e : cambiar_color()
#    )
#    page.add(color_picker, boton)
#
#ft.app(target=main)

