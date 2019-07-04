from sinric.sinricpro import SinricPro
from credential import apiKey, deviceId
from sinric.communication.sinricproudp import SinricProUdp
from threading import Thread
import asyncio

# Don't forget to change """ from credential import apiKey, deviceId """ to
# """ from credentials import apiKey, deviceId """

tempStates = {
    'powerLevel': 0,
    'brightnessLevel': 0
}


def power_state(did, state):
    print(did, state['state'])
    return True, state['state']


def set_power_level(did, state):
    print(did, 'PowerLevel : ', state)
    tempStates['powerLevel'] = state

    return True, tempStates['powerLevel']


def adjust_power_level(did, state):
    print(did, 'PowerLevelDelta : ', state)

    tempStates['powerLevel'] += state

    if tempStates['powerLevel'] > 100:
        tempStates['powerLevel'] = 100
    elif tempStates['powerLevel'] < 0:
        tempStates['powerLevel'] = 0

    return True, tempStates['powerLevel']


def set_brightness(did, state):
    print(did, 'BrightnessLevel : ', state)
    tempStates['brightnessLevel'] = state
    return True, tempStates['brightnessLevel']


def adjust_brightness(did, state):
    print(did, 'AdjustBrightnessLevel : ', state)

    tempStates['brightnessLevel'] += state
    if tempStates['brightnessLevel'] > 100:
        tempStates['brightnessLevel'] = 100
    elif tempStates['brightnessLevel'] < 0:
        tempStates['brightnessLevel'] = 0

    return True, tempStates['brightnessLevel']


def set_color(did, r, g, b):
    print(did, 'Red: ', r, 'Green: ', g, 'Blue : ', b)

    return True


def set_color_temperature(did, value):
    print(did, value)
    return True


callbacks = {
    'powerState': power_state,
    'setPowerLevel': set_power_level,
    'adjustPowerLevel': adjust_power_level,
    'setBrightness': set_brightness,
    'adjustBrightness': adjust_brightness,
    'setColor': set_color,
    'setColorTemperature': set_color_temperature
}


def handle_queue(hande):
    asyncio.new_event_loop().run_until_complete(hande())


def handle_threads():
    ws_client = SinricPro(apiKey, deviceId, callbacks)
    ws_client.socket.enableRequestPrint(False)  # Set it to True to start printing request JSON
    udp_client = SinricProUdp(callbacks)
    t1 = Thread(target=handle_queue, args=(ws_client.socket.handle,))
    t2 = Thread(target=udp_client.listen)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    ws_client.handle()


if __name__ == '__main__':
    handle_threads()
