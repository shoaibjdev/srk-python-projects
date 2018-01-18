import sys
import os
import time
import stomp
import logging
import threading
import signal
from importlib import reload

reload(sys)
#sys.setdefaultencoding('utf-8')

console = logging.StreamHandler()
console.setFormatter(logging.Formatter('[%(asctime)s] %(name)-12s %(levelname)-8s %(message)s'))
logging.getLogger().addHandler(console)
logging.getLogger().setLevel(logging.INFO)
LOGGER = logging.getLogger('vstp')


class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_message(self, headers, message):
       print('#### Message Received: %s' % message)


    def on_disconnected(self):
        logging.info("stomp disconnected, try to reconnect")
        with self.conn.need_reconnect:
            self.conn.need_reconnect.notify()


class ConnectThread(threading.Thread):
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.daemon = True
        self.conn = conn
    def run(self):
        while True:
            try:
                if not self.conn.is_connected():
                    logging.info("I AM HERE TO CONNECT")
                    self.conn.start()
                    self.conn.connect(wait=True)
                    self.conn.subscribe(destination="/queue/test", id="foo-1", ack='auto')
                    with self.conn.need_reconnect:
                        self.conn.need_reconnect.wait()
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                logging.warning(message)
                time.sleep(5)



class ActiveDaemon(object):
    def __init__(self):
        self.stop = False
        signal.signal(signal.SIGINT, self.go_down)

        self.conn = stomp.Connection([('10.137.160.64', 61613)], keepalive=True, reconnect_attempts_max=1, heartbeats=(4000, 4000))
        self.conn.need_reconnect = threading.Condition()
        self.conn.set_listener('', MyListener(self.conn))

    def run(self):
        c = ConnectThread(self.conn)
        c.start()
        
        while not self.stop:
            time.sleep(2)
        
        self.conn.unsubscribe(destination="/queue/test", id="foo-1")
        self.conn.disconnect(receipt=None)

    def go_down(self, signum, frame):
        logging.info("got exit command")
        self.stop = True
      
if __name__ == "__main__":
    daemon = ActiveDaemon()
    daemon.run()

