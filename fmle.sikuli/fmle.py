"""
Sikuli wrapper around FlashMediaLiveEncoder.

3.1 mac is the only version currently supported.
"""


__all__ = ['fmle']


class ConnectionError(Exception):
	"""
	Raised when FMLE is unable to connect to the server
	"""


class StreamingError(Exception):
	"""
	Raised when a streaming error occurs.
	"""


class FlashMediaLiveEncoder(object):
	"""
	"""

	name = 'FlashMediaLiveEncoder'

	_connected = False
	_streaming = False

	def openApp(self, timeout=10):
		openApp(self.name)

		wait("1302557758680.png", timeout)

		self.checkForProfileValidation()
		self.setDefaults()


	def closeApp(self):
		closeApp(self.name)


	def setDefaults(self):
		"""
		When the app has first started, we do some simple
		checking of options to ensure a solid foundation
		which to work from.
		"""
		m = exists(Pattern("VInutVldeu.png").exact(), 0)

		if m:
			click(m)

		m = exists(Pattern("JOutputVldeo.png").exact(), 0)

		if m:
			click(m)

		m = exists(Pattern("VAudm.png").exact(), 0)

		if m:
			click(m)


	def checkForProfileValidation(self):
		"""
		FMLE can complain about profile validation when
		it first opens.
		"""
		if exists(Pattern("ProfileValid.png").exact(), 3):
			click("4.png")


	def connect(self, fmsUrl='rtmp://localhost/live',
				stream='livestream', backupUrl=None):
		if self._connected:
		    return

		m = find("FMSURL.png")
		m = click(m.right(20))
		type(m, "a", KEY_CMD)
		type(m, Key.DELETE)
		type(m, fmsUrl)

		m = find("BackupURL.png")
		m = click(m.right(20))
		type(m, "a", KEY_CMD)
		type(m, Key.DELETE)

		if backupUrl:
		    type(backupUrl)

		m = find("1302582451486.png")
		m = click(m.right(20))
		type(m, "a", KEY_CMD)

		type(m, stream)

		click("1302504754272.png")

		if exists("ProblemwithP.png"):
			click("1302582971794.png")

			raise ConnectionError()

		if not exists("1302582882469.png"):
			raise ConnectionError()

		self._connected = True


	def startStreaming(self):
		if not self._connected:
		    self.connect()

		if self._streaming:
		    return

		click("Start-1.png")
		if not exists("Qsqmpmy.png", 10):
			raise StreamingError('Unable to start streaming')

		self._streaming = True


	def stopStreaming(self):
		"""
		"""
		if not self._streaming:
			return

		click("1302585488172.png")

		if not exists("1302585508876.png", 5):
			raise StreamingError('Unable to stop streaming')

		self._streaming = False


	def disconnect(self):
		if not self._connected:
			return

		if not click("Disconnect.png"):
			raise ConnectionError('Not connected!!')

		if not exists("1302586095509.png"):
			raise ConnectionError('Not connected!!')

		self._connected = False


	def reset(self):
		"""
		Returns the application to a default state
		"""
		if self._streaming:
			self.stopStreaming()

		if self._connected:
			self.disconnect()


	def __enter__(self):
		try:
			self.openApp()
		except:
			self.closeApp()

			raise

		return self


	def __exit__(self, *args):
		self.closeApp()

		return False


fmle = FlashMediaLiveEncoder()
