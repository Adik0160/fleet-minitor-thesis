import asyncio
import can
import RPi.GPIO as GP

#obłusgiwane pidsy Hyundai i30
#[0, 1, 4, 5, 12, 13, 15, 16, 17, 19, 28, 31, 32, 33, 35, 36, 44, 45, 48, 49, 51, 62, 64, 65, 66, 69, 73, 74, 76, 79]

fueltank = []
enginerpm = []
vehiclespeed = []
enginecoolant = []
batteryvoltage = []
mqttDataToSend ={}
vinNumber = 'Numer VIN pojazdu: '
deviceNr = 1234


PID01_20 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
PID21_40 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
PID41_60 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
PID61_80 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
PID81_A0 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
PIDA1_C0 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
PID01_20_S09 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


def print_message(msg):
    global fueltank
    global enginerpm
    global vehiclespeed
    global enginecoolant
    global batteryvoltage
    global PID01_20
    global PID21_40
    global PID41_60
    global PID61_80
    global PID81_A0
    global PIDA1_C0
    global PID01_20_S09
    global deviceNr

    dataLength = msg.data[0]
    if dataLength >= 10:
        return
    service = msg.data[1]
    PID = msg.data[2]
    if dataLength >= 3:
        A = msg.data[3]
    if dataLength >= 4:
        B = msg.data[4]
    if dataLength >= 5:
        C = msg.data[5]
    if dataLength >= 6:
        D = msg.data[6]

    if service == 0x41:
        if PID == 0x2f:
            formula = A*(100/255)
            fueltank.append(round(formula, 2))
            mqttDataToSend.clear()
            mqttDataToSend['deviceNr'] = deviceNr
            mqttDataToSend['fuel'] = round(formula, 2)
        elif PID == 0x0c:
            formula = (256*A + B)/4
            enginerpm.append(formula)
            mqttDataToSend['rotation'] = formula
        elif PID == 0x0d:
            formula = (A)
            vehiclespeed.append(formula)
            mqttDataToSend['speed'] = formula
        elif PID == 0x05:
            formula = (A - 40)
            enginecoolant.append(formula)
        elif PID == 0x00:
            formula = 16777216*A + 65536*B + 256*C + D
            PID01_20 = listbin(formula)
        elif PID == 0x20:
            formula = 16777216*A + 65536*B + 256*C + D
            PID21_40 = listbin(formula)
        elif PID == 0x40:
            formula = 16777216*A + 65536*B + 256*C + D
            PID41_60 = listbin(formula)
        elif PID == 0x60:
            formula = 16777216*A + 65536*B + 256*C + D
            PID61_80 = listbin(formula)
        elif PID == 0x80:
            formula = 16777216*A + 65536*B + 256*C + D
            PID81_A0 = listbin(formula)
        elif PID == 0xA0:
            formula = 16777216*A + 65536*B + 256*C + D
            PIDA1_C0 = listbin(formula)
        elif PID ==0x42:
            formula = (256*A + B)/1000
            batteryvoltage.append(formula)
            mqttDataToSend['voltage'] = formula
            print(mqttDataToSend)
    elif service == 0x49:
        if PID == 0x00:
            formula = 16777216*A + 65536*B + 256*C + D
            PID01_20_S09 = listbin(formula)
    try:
        print('<- odpowiedź ' + str(formula))
    except:
        print('brak pidsa w bazie danych')

def listbin(n):
    return [int(x) for x in bin(n)[2:].zfill(32)]

def showWorkingPids(x):
    return [i for i, val in enumerate(x) if val == 1]

async def vinRequest(bus):
    global vinNumber
    requestData = [0x02, 0x09, 0x02, 0x55, 0x55, 0x55, 0x55, 0x55]
    msg = can.Message (arbitration_id=0x7df, is_extended_id=False, data=requestData)
    await asyncio.sleep(0.5)
    workingPIDS = [1] + PID01_20_S09
    print('działające PIDy dla serwisu: 0x09')
    print(showWorkingPids(workingPIDS))
    if workingPIDS[0x02] == 0:
        print("brak PID w ECU")
        vinNumber = 'nie można odczytać numeru VIN'
        return
    flowContol = [0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    flow = can.Message(arbitration_id=0x7e0, is_extended_id=False, data=flowContol)
    bus.send(msg)
    vinNumber += bus.recv(0.5).data[5:].decode('ascii')
    bus.send(flow)
    vinNumber += bus.recv(0.5).data[1:].decode('ascii')
    vinNumber += bus.recv(0.5).data[1:].decode('ascii')
    print(vinNumber)


async def supportPIDsRequest(bus):
    global PID01_20
    global PID21_40
    global PID41_60
    global PID61_80
    global PID81_A0
    global PIDA1_C0
    GP.output(6, GP.HIGH)
    msg = can.Message(arbitration_id=0x7df, is_extended_id=False, data=[0x02, 0x01, 0x00, 0x55, 0x55, 0x55, 0x55, 0x55])
    bus.send(msg)
    await asyncio.sleep(0.5)
    if PID01_20[31] == 1:
        msg.data[2] = 0x20
        bus.send(msg)
        await asyncio.sleep(0.5)
    if PID21_40[31] == 1:
        msg.data[2] = 0x40
        bus.send(msg)
        await asyncio.sleep(0.5)
    if PID41_60[31] == 1:
        msg.data[2] = 0x60
        bus.send(msg)
        await asyncio.sleep(0.5)
    if PID61_80[31] == 1:
        msg.data[2] = 0x80
        bus.send(msg)
        await asyncio.sleep(0.5)
    if PID81_A0[31] == 1:
        msg.data[2] = 0xA0
        bus.send(msg)
        await asyncio.sleep(0.5)
    msg.data[1] = 0x09
    msg.data[2] = 0x00
    bus.send(msg)
    GP.output(6, GP.LOW)

async def sendRequest(bus, pid, serwis, sleep):
    requestData = [0x02, serwis, pid[0], 0x55, 0x55, 0x55, 0x55, 0x55]
    msg = can.Message(arbitration_id=0x7df, is_extended_id=False, data=requestData)
    workingPIDS = [1] + PID01_20 + PID21_40 + PID41_60 + PID61_80 + PID81_A0 + PIDA1_C0
    print('działające PIDy dla serwisu: 0x00')
    print(showWorkingPids(workingPIDS))
    while True:
        await asyncio.sleep(sleep)
        for i in pid:
            if workingPIDS[i] == 0:
                print("brak pidsa w ECU")
                continue
            msg.data[2] = i
            GP.output(6, GP.HIGH)
            bus.send(msg)
            print('-> pid: ' + str(hex(i)))
            await asyncio.sleep(0.2)
            GP.output(6, GP.LOW)

async def main():
    global fueltank
    global enginerpm
    global vehiclespeed
    global enginecoolant
    global batteryvoltage
    GP.setmode(GP.BCM)
    GP.setwarnings(False)
    GP.setup([5, 6, 13], GP.OUT)
    GP.output([5, 6, 13], [GP.LOW,GP.LOW,GP.LOW])
    can0 = can.Bus('vcan0', bustype='socketcan', bitrate=500000)
    filter = [{"can_id": 0x7e8, "can_mask": 0xff, "extended": False}]
    can0.set_filters(filter)

    listeners = [
        print_message
    ]
    loop = asyncio.get_event_loop()
    notifier = can.Notifier(can0, listeners, loop=loop)

    print("pytamy które pidsy w pierwszym i dziewiątym serwisie działają")
    await supportPIDsRequest(can0)
    print("zapytanie o numer vin")
    await vinRequest(bus=can0)
    print("cykliczne pytanie o aktualne dane")
    await sendRequest(bus=can0, pid=[0x05, 0x2f, 0x0c, 0x0d, 0x42], serwis=0x01, sleep=1) #0x0d, 0x0c, 0x05, 0x42, 0x2f

    GP.cleanup()
    notifier.stop()
    can0.shutdown()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
GP.cleanup()
loop.close()
