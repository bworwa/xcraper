
"""Core libraries, do not change"""

from ..modules import common, time_mod

class Log:

	BASE_PATH_TO_LOG = common.dirname(common.dirname(common.dirname(common.dirname(common.abspath(__file__))))) + "/logs"

	current_path_to_log = None

	def __init__(self):

		# [Low] TODO

		pass

	def __del__(self):

		# [Low] TODO

		pass

	def log_this(self, message, section):

		if section and isinstance(section, str):

			"""
				Logs the current [message] in the directory /logs/[section]/[current_date].log.
				If [section] does not exist it is automatically created
			"""

			self.current_path_to_log = self.BASE_PATH_TO_LOG + "/" + section

			if not common.exists(self.current_path_to_log):

				common.makedirs(self.current_path_to_log)

			now = time_mod.datetime.now()

			self.current_path_to_log = (self.current_path_to_log + "/%d-%d-%d.log") % (now.day, now.month, now.year)

			message = (("[%d:%d:%d] " + message.replace("%", "%%")) % (now.hour, now.minute, now.second)).replace("%%", "%")

			log = open(self.current_path_to_log, "a")

			log.write(message)

			log.close()
