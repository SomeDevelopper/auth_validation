from cassandra.io.libevreactor import LibevConnection
from cassandra.cluster import Cluster
import uuid

query_keyspace = '''
    CREATE KEYSPACE IF NOT EXISTS surveillance
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
'''


query_create_table = '''
    CREATE TABLE IF NOT EXISTS wanted_infos (
    id UUID PRIMARY KEY,
    name TEXT,
    image BLOB
;)
'''

cluster = Cluster(contact_points=["52.47.174.221"])
session_log = cluster.connect('wanted_infos')

session_log.execute(query_keyspace)
session_log.set_keyspace('surveillance')
session_log.execute(query_create_table)

with open('data/vincent_parra.jpeg', 'rb') as image_file:
    image_byte = image_file.read()

session_log.execute('''
    INSERT INTO wanted_infos (id, name, image)
                    VALUES (%s, %s, %s)
''', (uuid.uuid4(), 'Vincent PARRA', image_byte))

print("✅ Image insérée dans Cassandra !")

data = session_log.execute('''SELECT * FROM wanted_infos''')
for row in data:
        print(f"ID: {row.id}, Text de retour: {row.nom}, Sentiment: {row.image}")
