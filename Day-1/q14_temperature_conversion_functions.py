def celsius_to_fahrenheit(val):
    """Convert Celsius to Fahrenheit."""
    print(f"{val}C = {(val * 9/5) + 32:.2f}F") 

def fahrenheit_to_kelvin(val):
    """Convert Fahrenheit to Kelvin."""
    print(f"{val}F = {(val - 32) * 5/9 + 273.15:.2f}K") 

def kelvin_to_celsius(val):
    """Convert Kelvin to Celsius."""
    print(f"{val}K = {val - 273.15:.2f}C")  

celsius_to_fahrenheit(0)
fahrenheit_to_kelvin(32)
kelvin_to_celsius(300)