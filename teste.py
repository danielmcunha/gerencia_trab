from easysnmp import Session

session = Session(hostname='192.168.43.161', version=3, security_level='auth_with_privacy', security_username='MD5DESUser', auth_protocol='MD5', auth_password='senhasenhasenha', privacy_protocol='DES', privacy_password='senhasenhasenha')
#numInterfaces = int(session.get('hrProcessorLoad.0').value)
print(session.get('laLoad.1').value)
