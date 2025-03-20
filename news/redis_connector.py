# redis_connector.py
import redis

REDIS_HOST = 'redis-19370.c276.us-east-1-2.ec2.redns.redis-cloud.com'  # например: redis-12345.c123.us-east-1-4.ec2.cloud.redislabs.com
REDIS_PORT = 19370  # порт из endpoint
REDIS_PASSWORD = 'NL0FKPbhWxxX8OSIF0qpvp6Vcq36aOYm'  # пароль от вашей базы

# Подключение к Redis
redis_client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    # ssl=True,  # включаем SSL/TLS, если требуется вашим провайдером Redis
    decode_responses=True  # удобно для работы со строками
)

# Тест подключения
if __name__ == "__main__":
    redis_client.set('test_key', 'hello redis!')
    value = redis_client.get('test_key')
    print(value)  # должен вывести: hello redis!
