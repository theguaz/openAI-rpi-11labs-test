import smbus2

# Function to read battery percentage
def read_battery_percentage(bus, address=0x32, register=0x0F):  # Adjust the 'register' as per your UPS documentation
    try:
        # Create an SMBus instance
        with smbus2.SMBus(bus) as smbus:
            # Read a single byte from the specified register
            battery_percentage = smbus.read_byte_data(address, register)
            return battery_percentage
    except Exception as e:
        print(f"Failed to read from the device: {e}")
        return None

# Example usage
bus_number = 1  # Raspberry Pi usually uses bus 1 for newer models
battery_percent = read_battery_percentage(bus_number)
if battery_percent is not None:
    print(f"Battery Percentage: {battery_percent}%")
else:
    print("Could not read the battery percentage.")
