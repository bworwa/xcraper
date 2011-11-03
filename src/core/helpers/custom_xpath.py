
"""Core libraries, do not change"""

# External
from xpath import find, findvalue

class Xpath:

	def __init__(self):

		# [Low] TODO

		pass

	def __del__(self):

		# [Low] TODO

		pass

	def find(self, query, context, get_value, charset, result_list):

		"""
		Appends to 'result_list' the result of applying the XPath query 'query' to the minidom Document 'context'
		'get_value' (True/False) will determine whether to use 'xpath.find' or 'xpath.findValue'

		All the results are encoded using the specified 'charset'
		"""

		if get_value:

			result_list.append(findvalue(query, context).encode(charset))

		else:

			xpath_result = find(query, context)

			for result in xpath_result:

				result_list.append(result.toxml().encode(charset))
