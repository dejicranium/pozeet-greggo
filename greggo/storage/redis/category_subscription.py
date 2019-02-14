from greggo.storage.redis.structures.set import RedisSet


class CategorySubscription(RedisSet):
    key_format = 'cat_sub:%(category_id)s'

    def __init__(self, category_id, redis=None):
        key = self.key_format % {'category_id': category_id}
        super().__init__(key, redis)

    def get_subscribers(self):
        subscribers = self.get_all()
        subscribers = [int(subscriber.decode('utf-8')) for subscriber in subscribers]
        return subscribers

    def add_subscriber(self, user_id):
        self.add(user_id)

    def remove_subscriber(self, user_id):
        self.delete(user_id)


if __name__ == '__main__':
    category = CategorySubscription(1)
    category.add_subscriber(439)

    print(category.get_subscribers())
