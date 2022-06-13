import enum

class StatusValues(enum.Enum):

	# TODO: Check if other states possible like partial 
	# TODO: Check how to add test cases for the same
	InProgress = 'in-progress'
	Completed = 'completed'
	Error = 'error'