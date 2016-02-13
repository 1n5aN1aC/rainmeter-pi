#!python
from multiprocessing.connection import Listener
import traceback, logging

from Stoppable_Thread import *
import Now

# This class handles all server functions
class Server_Listener(Stoppable_Thread):
    def run(self):
        server = Listener( ('', 25000) )
        logging.getLogger("thread-listener").info("Connection listener initialized.")
        while self.RUN:
            try:
                client = server.accept()
                logging.getLogger("thread-listener").debug("Client connecting...")
                self.echo_client(client)
            except Exception:
                traceback.print_exc()
    
    def echo_client(itself, conn):
        try:
            while True:
                msg = conn.recv()
                now = Now.get()
                #Do we need to reset the current rainfall?
                if msg == "reset_rain":
                    now.Out_Rain_Since_Reset = 0
                conn.send(now)
        except EOFError:
            logging.getLogger("thread-listener").debug("Connection closed")
