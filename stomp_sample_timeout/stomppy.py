
import time, sys, os, logging
import stomp
import requests

user = os.getenv("ACTIVEMQ_USER") or "admin"
password = os.getenv("ACTIVEMQ_PASSWORD") or "password"
host = os.getenv("ACTIVEMQ_HOST") or "10.137.160.64"
port = os.getenv("ACTIVEMQ_PORT") or 61613
destination = sys.argv[1:2] or ["/queue/event"]
destination = destination[0]

log = logging.getLogger('stomp.py')


def webhook_notify():
    print('Reached to Webhook Notify!')


def connect_and_subscribe(conn):
    conn.start()
    conn.connect(login=user,passcode=password, wait=True)
    conn.subscribe(destination=destination, id=1, ack='auto')
    print('Connection Established!')

class MyListener(stomp.ConnectionListener):

  def __init__(self, conn):
    self.conn = conn
    self.start = time.time()

  def on_error(self, headers, message):
    print('Received an Error %s' % message)

  def on_message(self, headers, message):
     print("Received Message: %s" % message)
     webhook_notify()

  def on_disconnected(self):
     print('disconnected')
     connect_and_subscribe(self.conn)

#conn = stomp.Connection(host_and_ports = [(host, port)], hearbeats=(4000, 4000))
conn = stomp.StompConnection12(host_and_ports= [(host, port)], heartbeats=(5000,5000), reconnect_attempts_max=5)

conn.set_listener('', MyListener(conn))
connect_and_subscribe(conn)
print("Waiting for messages...")
while 1:
  time.sleep(10)


