import time
from csmapi import CSMAPI


class Bridge():
    def __init__(self, host):
        self.csmapi = CSMAPI(host)
        self.pre_data_timestamp = {}

    def pull(self, device_id, df_name):
        data = self.csmapi.pull(device_id, df_name)
        if data and self.pre_data_timestamp.get(df_name) != data[0][0]:
            self.pre_data_timestamp[df_name] = data[0][0]
            if data[0][1]:
                return data[0][1]
        return None

if __name__ == '__main__':

    Url = 'IoTtalk Server Url'
    Source = Bridge(Url)
    data = Source.pull('SourceDeviceId', 'SourceDeviceFeatureName')
    if data: 
        print(data[0])
