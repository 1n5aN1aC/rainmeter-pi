#!python
import threading

# Thread class with a stop() method.
# The thread itself has to check regularly for the self.RUN condition.
class Stoppable_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.RUN = True
		self.daemon = True
		self.start()
	
	def stop(self):
		self.RUN = False
