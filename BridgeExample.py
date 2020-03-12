import time, datetime
from DAN import DAN 
from bridge import Bridge

communication_interval = 60 #seconds

ServerURL = 'Home_IoTtalk_URL'
Reg_addr = 'Bridge_form_Foreign_IoTtalk_Server' 
profile = {
    'dm_name': 'Bridge',
    'df_list': ['CO2', 'Luminance', 'Temperature', 'Humidity', 'PM2.5', 'Temperature1', 'CO2_1'],
    'd_name': 'Foreign_IoTtalk_Server'
}


Foreign = Bridge('Foreign_IoTtalk_Server_Url') #Foreign_IoTtalk_Server
def fetchData(df):
    data = {
        'Temperature' : lambda : Foreign.pull('Foreign_device_id1', 'Temperature'), #Indoor temp
        'Humidity'    : lambda : Foreign.pull('Foreign_device_id2', 'Humidity'), #Indoor humidity
        'CO2'         : lambda : Foreign.pull('Foreign_device_id3', 'CO2'), #Indoor CO2
        'PM2.5'       : lambda : Foreign.pull('Foreign_device_id4', 'PM2.5'), #Indoor PM2.5
        'Luminance'   : lambda : Foreign.pull('Foreign_device_id5', 'Illumination'), #Indoor Luminance
        'Temperature1': lambda : Foreign.pull('Foreign_device_id6', 'Temperature'), #Outdoor temp
        'CO2_1'       : lambda : Foreign.pull('Foreign_device_id7', 'CO2'), #Outdoor CO2
    }
    return data.get(df, lambda : None)()


if __name__ == '__main__':
    dan = DAN(profile, ServerURL, Reg_addr)
    dan.device_registration_with_retry()

    while True:
        try:
            for df in profile['df_list']:
                data = fetchData(df)
                if data and (data[0] != None):
                    print('{}: {}'.format(df, data[0]))
                    dan.push(df, data[0])
                time.sleep(5)
        except Exception as e:
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr is not found. Try to re-register...')
                dan.device_registration_with_retry()
            else:
                print('Connection failed due to unknow reasons.')
            time.sleep(1)    
        time.sleep(communication_interval)
