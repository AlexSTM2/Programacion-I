from .. import login_manager
import jwt

@login_manager.user_loader
def load_user(token):
    try:
        jwt_options = {
            'verify_signature': False,
            'verify_exp': True,
            'verify_nbf': False,
            'verify_iat': True,
            'verify_aud': False
        }

        data = jwt.decode(token, options=jwt_options, algorithms=['HS256'])
        return {'id': data['ID Usuario'], 'email': data['email']}
    except jwt.excetions.InvalidTokenError:
        print('Invalid Token')
    except jwt.exceptions.DecodeError:
        print('Decode Error')

#--------------- Utilidades -----------------#
#Gracias copilot por ayudarme a escribir esto.