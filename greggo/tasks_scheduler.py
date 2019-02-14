from tasks import app


def fanout(user_id, activities):
    result = app.send_task('tasks.fanout', args=(user_id, activities))

if __name__ == "__main__":
    print(fanout(20, [100, 101, 102]))