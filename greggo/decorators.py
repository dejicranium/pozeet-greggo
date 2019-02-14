def fallback_to_ground_storage(storage):
    def decorator(func):
        def wrapper(*args, **kwargs):
            status = func(*args, **kwargs)
            #if status is None
            if not status:
                dbsession.query(storage).filter_by(storage.id==id)

        return wrapper

        
def add_to_redis_storgage(storage):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs):

        return wrapper
