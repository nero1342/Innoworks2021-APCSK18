import datetime
import time
import string
import random
import threading

from wisepaasdatahubedgesdk.EdgeAgent import EdgeAgent
import wisepaasdatahubedgesdk.Common.Constants as constant
from wisepaasdatahubedgesdk.Model.Edge import EdgeAgentOptions, MQTTOptions, DCCSOptions, EdgeData, EdgeTag, EdgeStatus, EdgeDeviceStatus, EdgeConfig, NodeConfig, DeviceConfig, AnalogTagConfig, DiscreteTagConfig, TextTagConfig
from wisepaasdatahubedgesdk.Common.Utils import RepeatedTimer

class DataHub():
    _nodeId = '6fc95c35-1382-4a6a-b68d-64a61c65ce1f'
    _apiUrl = 'https://api-dccs-ensaas.education.wise-paas.com/'
    _credentialKey = '73c8acf95c4c172434efac746e617c08'

    def __init__(self, configs):
        self.timer = None 
        edgeAgentOptions = EdgeAgentOptions(nodeId = self._nodeId)
        edgeAgentOptions.connectType = constant.ConnectType['DCCS']
        dccsOptions = DCCSOptions(apiUrl = self._apiUrl, credentialKey = self._credentialKey)
        edgeAgentOptions.DCCS = dccsOptions

        self._edgeAgent = EdgeAgent(edgeAgentOptions)
        self._edgeAgent.connect()

        print("Create config...")
        config = self.__generateConfig(configs)
        self._edgeAgent.uploadConfig(action = constant.ActionType['Create'], edgeConfig = config)

        print("Create device...")
        status = self.__generateStatus()
        self._edgeAgent.sendDeviceStatus(status)

    def __sendData(self):
        data = self.__generateData()
        self._edgeAgent.sendData(data)

    def sendData(self, deviceId = 'Device', tagName = 'PeopleCount', value = 0):
        edgeData = EdgeData()
        tag = EdgeTag(deviceId, tagName, value)
        edgeData.tagList.append(tag)
        edgeData.timestamp = datetime.datetime.now()
        print(datetime.datetime.now(), deviceId, tagName, value)
        
        self._edgeAgent.sendData(edgeData)

    def __generateStatus(self):
        deviceStatus = EdgeDeviceStatus()
        deviceId = 'Device'
        device = EdgeStatus(id = deviceId, status = constant.Status['Online'])
        deviceStatus.deviceList.append(device)
        return deviceStatus

    def __generateConfig(self, configs):
        config = EdgeConfig()
        nodeConfig = NodeConfig(nodeType = constant.EdgeType['Gateway'])
        config.node = nodeConfig

        for attr in configs:
            deviceConfig = DeviceConfig(id = attr,
                                        name = attr,
                                        description = attr,
                                        deviceType = attr,
                                        retentionPolicyName = '')
            for tag in configs[attr]:
                tagConfig = DiscreteTagConfig(
                    name = tag,
                    description = tag,
                    readOnly = True,
                    arraySize = 0,
                )
                deviceConfig.discreteTagList.append(tagConfig)
            config.node.deviceList.append(deviceConfig)

        return config
