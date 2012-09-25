"""
Testing src/syncAPI

"""

import unittest
import ast

import src.settings


class SettingsTest(unittest.TestCase):
    
    def setUp(self):
        """Set up the test"""
        self.settingsInstance = src.settings.Settings()
        self.mockSettingsConf = {
            'nickname': 'Innocence',
            'realname': 'Motoko Kusanagi',
            'servers': {
                'quakenet': {
                    'address': 'irc.quakenet.org',
                    'port': '6697',
                    'ssl': True,
                    'channels': [
                        '#code'
                    ]
                }
            }
        }
        self.oldSettingsFileData = readSettingsFile('tests/test_settings2.conf')
    
    def tearDown(self):
        # Reset the file to it's original
        writeToSettingsFile('tests/test_settings2.conf', self.oldSettingsFileData)
    
    def test_settings_can_be_changed(self):
        self.assertNotEqual(self.settingsInstance.settings, self.mockSettingsConf)
        self.settingsInstance.settings = self.mockSettingsConf
        self.assertEqual(self.settingsInstance.settings, self.mockSettingsConf)
    
    def test_attributes_can_be_read_from_settings(self):
        self.settingsInstance.settings = self.mockSettingsConf
        self.assertEqual(self.settingsInstance.settings, self.mockSettingsConf)
        
        self.assertEqual(
            self.settingsInstance.settings['nickname'],
            self.mockSettingsConf['nickname']
        )
        self.assertEqual(
            self.settingsInstance.settings['servers']['quakenet']['port'],
            self.mockSettingsConf['servers']['quakenet']['port']
        )
    
    def test_settings_path_can_be_changed(self):
        mockSettingsConf1 = {
            'nickname': 'Innocence',
            'realname': 'Motoko Kusanagi'
        }
        mockSettingsConf2 = {
            'servers': {
                'freenode': {
                    'address': 'irc.freenode.net',
                    'port': '6667'
                }
            }
        }
        self.assertNotEqual(self.settingsInstance.settings, mockSettingsConf1)
        self.settingsInstance.settingsFilePath = 'tests/test_settings1.conf'
        self.assertEqual(self.settingsInstance.settings, mockSettingsConf1)
        
        self.assertNotEqual(self.settingsInstance.settings, mockSettingsConf2)
        self.settingsInstance.settingsFilePath = 'tests/test_settings2.conf'
        self.assertEqual(self.settingsInstance.settings, mockSettingsConf2)
    
    def test_settings_file_can_be_reloaded(self):
        mockSettingsConf1 = {
            'nickname': 'Innocence',
            'realname': 'Motoko Kusanagi'
        }
        settingsFile1 = 'tests/test_settings1.conf'
        settingsFile2 = 'tests/test_settings2.conf'
        self.settingsInstance.settingsFilePath = settingsFile2
        # Overwrite the settings file
        writeToSettingsFile(settingsFile2, readSettingsFile(settingsFile1))
        
        self.assertNotEqual(self.settingsInstance.settings, mockSettingsConf1)
        self.settingsInstance.reload()
        self.assertEqual(self.settingsInstance.settings, mockSettingsConf1)
        


def readSettingsFile(settingsFile):
    settingsFileData = None
    with open(settingsFile, 'r') as settingsFile:
        settingsFileData = settingsFile.read()
    return settingsFileData
    
def writeToSettingsFile(settingsFile, data):
    settingsFileData = None
    with open(settingsFile, 'w') as settingsFile:
        settingsFile.write(data)

if __name__ == '__main__':
    unittest.main()