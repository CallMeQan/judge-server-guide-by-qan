from functools import partial
import threading
import logging

from .libs.handler import JudgeHandler
from .libs.ServerModel import Server

# Configure logging
logger = logging.getLogger('judge.bridge')

# Server setup
judge_server = Server([("", 9999)], partial(JudgeHandler))

threading.Thread(target=judge_server.serve_forever).start()

print('Judge server started, press 1 to exit.')

while True:
    if input() == '1':
        judge_server.shutdown()
        print('Judge server stopped.')
        break