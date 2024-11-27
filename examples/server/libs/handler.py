import json
import logging
import threading
import time
from collections import deque, namedtuple

from .base_handler import ZlibPacketHandler, proxy_list

logger = logging.getLogger('judge.bridge')
json_log = logging.getLogger('judge.json.bridge')

UPDATE_RATE_LIMIT = 5
UPDATE_RATE_TIME = 0.5
SubmissionData = namedtuple('SubmissionData', 'time memory short_circuit pretests_only contest_no attempt_no user_id')


class JudgeHandler(ZlibPacketHandler):
    proxies = proxy_list([])

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.handlers = {
            'grading-begin': self.on_grading_begin,
            'grading-end': self.on_grading_end,
            'compile-error': self.on_compile_error,
            'compile-message': self.on_compile_message,
            'batch-begin': self.on_batch_begin,
            'batch-end': self.on_batch_end,
            'test-case-status': self.on_test_case,
            'internal-error': self.on_internal_error,
            'submission-terminated': self.on_submission_terminated,
            'submission-acknowledged': self.on_submission_acknowledged,
            'ping-response': self.on_ping_response,
            'supported-problems': self.on_supported_problems,
            'handshake': self.on_handshake,
        }
        self._working = False
        self._no_response_job = None
        self._problems = []
        self.executors = {}
        self.problems = {}
        self.latency = None
        self.time_delta = None
        self.load = 1e100
        self.name = None
        self.is_disabled = False
        self.tier = None
        self.batch_id = None
        self.in_batch = False
        self._stop_ping = threading.Event()
        self._ping_average = deque(maxlen=6)  # 1 minute average, just like load
        self._time_delta = deque(maxlen=6)

        # each value is (updates, last reset)
        self.update_counter = {}
        self.judge = None
        self.judge_address = None

        self._submission_cache_id = None
        self._submission_cache = {}

    def on_connect(self):
        self.timeout = 15
        logger.info('Judge connected from: %s', self.client_address)
        json_log.info(self._make_json_log(action='connect'))

    def on_disconnect(self):
        self._stop_ping.set()
        if self._working:
            logger.error('Judge %s disconnected while handling submission %s', self.name, self._working)
        if self.name is not None:
            self._disconnected()
        logger.info('Judge disconnected from: %s with name %s', self.client_address, self.name)

        json_log.info(self._make_json_log(action='disconnect', info='judge disconnected'))

    def _authenticate(self, id, key):
        # TODO: Implement a better way to authenticate judges
        return True

    def _connected(self):
        # TODO: Handle the connection
        pass

    def _disconnected(self):
        # TODO: Handle the disconnection
        pass

    def _update_ping(self):
        # TODO: Handle the ping update
        pass

    def send(self, data):
        super().send(json.dumps(data, separators=(',', ':')))

    def on_handshake(self, packet):
        if 'id' not in packet or 'key' not in packet:
            logger.warning('Malformed handshake: %s', self.client_address)
            self.close()
            return

        if not self._authenticate(packet['id'], packet['key']):
            self.close()
            return

        self.timeout = 60
        self._problems = packet['problems']
        self.problems = dict(self._problems)
        self.executors = packet['executors']
        self.name = packet['id']

        self.send({'name': 'handshake-success'})
        logger.info('Judge authenticated: %s (%s)', self.client_address, packet['id'])
        threading.Thread(target=self._ping_thread).start()
        self._connected()

    def can_judge(self, problem, executor, judge_id=None):
        return problem in self.problems and executor in self.executors and  \
            ((not judge_id and not self.is_disabled) or self.name == judge_id)

    @property
    def working(self):
        return bool(self._working)

    def get_related_submission_data(self, submission):
        # TODO: Implement a way to handle the submission data, check for related data
        pass

    def disconnect(self, force=False):
        if force:
            # Yank the power out.
            self.close()
        else:
            self.send({'name': 'disconnect'})

    def submit(self, id, problem, language, source):
        data = self.get_related_submission_data(id)
        self._working = id
        self._no_response_job = threading.Timer(20, self._kill_if_no_response)
        self.send({
            'name': 'submission-request',
            'submission-id': id,
            'problem-id': problem,
            'language': language,
            'source': source,
            'time-limit': data.time,
            'memory-limit': data.memory,
            'short-circuit': data.short_circuit,
            'meta': {
                'pretests-only': data.pretests_only,
                'in-contest': data.contest_no,
                'attempt-no': data.attempt_no,
                'user': data.user_id,
            },
        })

    def _kill_if_no_response(self):
        logger.error('Judge failed to acknowledge submission: %s: %s', self.name, self._working)
        self.close()

    def on_timeout(self):
        if self.name:
            logger.warning('Judge seems dead: %s: %s', self.name, self._working)

    def on_submission_processing(self, packet):
        pass

    def on_submission_wrong_acknowledge(self, packet, expected, got):
        pass

    def on_submission_acknowledged(self, packet):
        pass

    def abort(self):
        self.send({'name': 'terminate-submission'})

    def get_current_submission(self):
        return self._working or None

    def ping(self):
        self.send({'name': 'ping', 'when': time.time()})

    def on_packet(self, data):
        try:
            try:
                data = json.loads(data)
                if 'name' not in data:
                    raise ValueError
            except ValueError:
                self.on_malformed(data)
            else:
                handler = self.handlers.get(data['name'], self.on_malformed)
                handler(data)
        except Exception:
            logger.exception('Error in packet handling (Judge-side): %s', self.name)
            self._packet_exception()
            # You can't crash here because you aren't so sure about the judges
            # not being malicious or simply malformed. THIS IS A SERVER!

    def _packet_exception(self):
        json_log.exception(self._make_json_log(sub=self._working, info='packet processing exception'))

    def _submission_is_batch(self, id):
        # TODO: Return is the submission is a batch
        pass

    def on_supported_problems(self, packet):
        pass

    def on_grading_begin(self, packet):
        logger.info('%s: Grading has begun on: %s', self.name, packet['submission-id'])
        self.batch_id = None
        
        # TODO: Implement the grading begin, announce the submission is being graded
        pass

    def on_grading_end(self, packet):
        
        pass

    def on_compile_error(self, packet):
        pass

    def on_compile_message(self, packet):
        pass

    def on_internal_error(self, packet):
        pass
    def on_submission_terminated(self, packet):
        pass

    def on_batch_begin(self, packet):
        pass

    def on_batch_end(self, packet):
        pass

    def on_test_case(self, packet, max_feedback=100):
        pass

    def on_malformed(self, packet):
        logger.error('%s: Malformed packet: %s', self.name, packet)
        json_log.exception(self._make_json_log(sub=self._working, info='malformed json packet'))

    def on_ping_response(self, packet):
        end = time.time()
        self._ping_average.append(end - packet['when'])
        self._time_delta.append((end + packet['when']) / 2 - packet['time'])
        self.latency = sum(self._ping_average) / len(self._ping_average)
        self.time_delta = sum(self._time_delta) / len(self._time_delta)
        self.load = packet['load']
        self._update_ping()

    def _ping_thread(self):
        try:
            while True:
                self.ping()
                if self._stop_ping.wait(10):
                    break
        except Exception:
            logger.exception('Ping error in %s', self.name)
            self.close()
            raise

    def _make_json_log(self, packet=None, sub=None, **kwargs):
        data = {
            'judge': self.name,
            'address': self.judge_address,
        }
        if sub is None and packet is not None:
            sub = packet.get('submission-id')
        if sub is not None:
            data['submission'] = sub
        data.update(kwargs)
        return json.dumps(data)

    def _post_update_submission(self, id, state, done=False):
        pass

    def on_cleanup(self):
        pass
