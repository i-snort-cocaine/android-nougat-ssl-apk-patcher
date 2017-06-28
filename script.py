import os
import time
import shutil
import xml.etree.ElementTree as ET


apk = input('apk name(place in same directory as script.py): ')
apk_name = apk
if apk[-4:] != '.apk':
    apk += '.apk'
print('to patch: '+apk)

print('decoding apk(may take a moment)')
os.system('java -jar apktool_2.2.3.jar -q -s d ' + apk)
print('apk successfully decoded')

ET.register_namespace('amazon', "http://schemas.amazon.com/apk/res/android")
ET.register_namespace('android', "http://schemas.android.com/apk/res/android")
tree = ET.parse(apk_name+'/AndroidManifest.xml')
tree.getroot().find('application').attrib['{http://schemas.android.com/apk/res/android}networkSecurityConfig'] = '@xml/network_security_config'
tree.write(apk_name+'/AndroidManifest.xml')
print('AndroidManifest.xml successfully patched')

shutil.copy2('network_security_config.xml', apk_name+'/res/xml/')
print('network_security_config.xml successfully copied into {}/res/xml/'.format(apk_name))

print('building apk(may take a moment)')
os.system('java -jar apktool_2.2.3.jar -q b {} -o {}_unsigned.apk'.format(apk_name, apk_name))
print('apk successfully rebuilt to {}_unsigned.apk'.format(apk_name))

os.system('keytool -noprompt -genkey -v -keystore {}.keystore -alias {} -keyalg RSA -keysize 2048 -validity 10000  -dname CN=CA -keypass password --storepass password'.format(apk_name+'_ks', apk_name+'_alias'))
print('keystore successfully generated')

os.system('java -jar apksignerx.jar sign --ks-pass pass:password --out {}.apk --ks-key-alias {} --ks {}.keystore {}.apk '.format(apk_name+'_signed', apk_name+'_alias', apk_name+'_ks', apk_name+'_unsigned', ))
print('apk successfully signed @ {}_signed.apk'.format(apk_name))

shutil.rmtree(apk_name)
os.remove(apk_name+'_ks.keystore')
os.remove(apk_name+'_unsigned.apk')
print('succesfully cleaned up')

print('finished')
