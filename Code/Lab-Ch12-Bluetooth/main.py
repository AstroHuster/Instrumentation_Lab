import struct
import asyncio
import bluetooth
import machine
import aioble

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / 0xffff

# For BLE advertising beacon
ble_name = "picow_cpu_temp"
ble_service_uuid = bluetooth.UUID(0x181A)
ble_characteristic_uuid = bluetooth.UUID(0x2A6E)
ble_appearance = 0x0300
ble_advertising_interval = 2000

# LED
led_pin = machine.Pin("LED", machine.Pin.OUT)
led_pin(0)

# Set up BLE
ble_service = aioble.Service(ble_service_uuid)
ble_characteristic = aioble.Characteristic(
    ble_service,
    ble_characteristic_uuid,
    read=True,
    notify=True)
aioble.register_services(ble_service)

# coroutine for beacon task
async def ble_task():
    while True:
        async with await aioble.advertise(
            ble_advertising_interval,
            name=ble_name,
            services=[ble_service_uuid],
            appearance=ble_appearance) as connection:
            print("Connection from", connection.device)
            await connection.disconnected()

def encode_temp(temperature):
    return struct.pack("<h", round(temperature * 100))

async def sensor_task():
    while True:
        reading = sensor_temp.read_u16() * conversion_factor
        temperature = 27 - (reading - 0.706) / 0.001721
        print("Temperature: ", temperature)
        ble_characteristic.write(encode_temp(temperature))
        led_pin.toggle()
        await asyncio.sleep_ms(2000)

async def main():
    task1 = asyncio.create_task(ble_task())
    task2 = asyncio.create_task(sensor_task())
    await asyncio.gather(task1, task2)

print("Launching Raspberry Pi Pico W BLE temperature sensor...")
asyncio.run(main())
print("# # D O N E # # ")

# EOF
