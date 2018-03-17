from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, \
                         BadSignature, SignatureExpired
from functools import wraps
from base64 import b64decode
from flask import request
import flask
import time


def generate_auth_token(expiration=600):
	 # s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
	 s = Serializer('test1234@#$', expires_in=expiration)
	 # pass index of user
	 return s.dumps({'id': 1})

def verify_auth_token(token):
		s = Serializer('test1234@#$')
		try:
				data = s.loads(token)
		except SignatureExpired:
				return None    # valid token, but expired
		except BadSignature:
				return None    # invalid token
		return "Success"

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		# Get token
		token = request.args.get('token')

		if not token:
			return {"Unauthorized":"No token found"}, 401

		if verify_auth_token(token):
			return f(*args, **kwargs) # Run the underlying method
		else:
			return {"Unauthorized":"Token invalid"}, 401
	return decorated