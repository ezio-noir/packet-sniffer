import textwrap
import colorama


# Prints raw data of a packet
def print_raw(data, width=70, indent='\t', color=None):
    data_hexa = ' '.join([f'{byte:02X}' for byte in data])
    data_hexa = textwrap.fill(data_hexa, width=width, initial_indent=indent, subsequent_indent=indent)
    print_with_color(data_hexa, color)


# Prints text with color
def print_with_color(data, color=None):
    if color:
        print(color + data + colorama.Style.RESET_ALL)
    else:
        print(data)