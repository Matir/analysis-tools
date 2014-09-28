from string import uppercase, lowercase, maketrans

def rot_alpha(data, rot):

	upper = ''.join([uppercase[(i+rot)%26] for i in xrange(26)])
	lower = ''.join([lowercase[(i+rot)%26] for i in xrange(26)])
	table = maketrans(uppercase + lowercase, upper + lower)

	return data.translate(table)
