import os
from molar import ClientConfig, Client

molar_server = os.getenv('MOLAR_SERVER')
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
dbname1 = os.getenv('DBNAME1')
dbname2= os.getenv('DBNAME2')

print(molar_server)
