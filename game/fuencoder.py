import json, re
# inspired by https://github.com/python/cpython/blob/3.8/Lib/json/encoder.py

class GameEncoder(json.JSONEncoder):
	''' custom JSON encoder to output each record on single line
		
		default json output 
		{ 
			'a':
				[
					'foo',
					'bar'
				]
		} 
		when we want: 
		{
			'a': ['foo', 'bar']  <- all on single line
		}
	'''
	print(100)

	def iterencode(self, o, _one_shot=False):
		''' a customised implementation '''

		indent_ = 0

		for ln in super(GameEncoder, self).iterencode(o, _one_shot=_one_shot):

	  		if ln.startswith('['):
	  			indent_ += 1
	  			ln = re.sub(r'\s*', '', ln)

	  		elif 0 < indent_:
	  			ln = re.sub(r'\s*', '', ln)

	  		if ln.endswith(']'):
	  			indent_ -= 1
	  		
  			yield ln