import smbus2

def read_battery_soc(bus, address=0x32):
    try:
        # Open the I2C bus
        with smbus2.SMBus(bus) as smbus:
            # Read two bytes from the SOC register (0x04)
            # MAX17040G typically uses 2 bytes for SOC, with MSB first
            data = smbus.read_i2c_block_data(address, 0x04, 2)
            soc = (data[0] << 8 | data[1]) / 256  # Convert the 16-bit value to a percentage
            return soc
    except Exception as e:
        print(f"Error reading from UPS: {e}")
        return None

# Example usage
bus_number = 1  # Raspberry Pi I2C bus 1
battery_soc = read_battery_soc(bus_number)
if battery_soc is not None:
    print(f"Battery SOC: {battery_soc:.2f}%")
else:
    print("Could not read battery SOC.")
