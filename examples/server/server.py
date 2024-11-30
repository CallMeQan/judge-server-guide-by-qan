from functools import partial
import threading
import logging

from libs.handler import JudgeHandler
from libs.ServerModel import Server

# Configure logging
logger = logging.getLogger('judge.bridge')

# Server setup
judge_server = Server([("", 9999)], partial(JudgeHandler))

threading.Thread(target=judge_server.serve_forever).start()

print('Judge server started, press 1 to exit.')

def shutdown():
    judge_server.shutdown()
    print('Judge server stopped.')

while True:
    try:
        if input() == '1':
            shutdown()
            break
        else:
            print('Press 1 to exit.')
    except KeyboardInterrupt:
        shutdown()
        break
    except Exception as e:
        logger.error(e)
        print('Error occurred, check logs for more information.')
        shutdown()
        break