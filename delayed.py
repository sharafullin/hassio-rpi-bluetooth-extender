import redis
from delayed.queue import Queue
from delayed.worker import PreforkedWorker

def start_task_processing():
    conn = redis.Redis()
    queue = Queue(name='default', conn=conn)
    worker = PreforkedWorker(queue=queue)
    worker.run()