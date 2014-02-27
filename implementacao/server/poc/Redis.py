import redis
import time

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
r.set('teste', '4')
r.expire('teste', 3)
print r.get('teste')

time.sleep(4)

print r.get('teste')
