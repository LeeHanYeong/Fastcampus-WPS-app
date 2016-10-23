import requests
import json
from ..facebook import APP_ID, SECRET_CODE, APP_ACCESS_TOKEN


def get_access_token(code, redirect_uri):
    url_request_access_token = 'https://graph.facebook.com/v2.8/oauth/access_token?' \
                               'client_id={cliend_id}&' \
                               'redirect_uri={redirect_uri}&' \
                               'client_secret={client_secret}&' \
                               'code={code}'.format(
                                    cliend_id=APP_ID,
                                    redirect_uri=redirect_uri,
                                    client_secret=SECRET_CODE,
                                    code=code
                                )
    r = requests.get(url_request_access_token)
    dict_access_token = r.json()
    print(json.dumps(dict_access_token, indent=2))
    access_token = dict_access_token.get('access_token')
    return access_token


def get_user_id_from_access_token(access_token):
    uri_request_user_id = 'https://graph.facebook.com/debug_token?' \
                          'input_token={access_token}&' \
                          'access_token={app_access_token}'.format(
                                access_token=access_token,
                                app_access_token=APP_ACCESS_TOKEN
                            )
    r = requests.get(uri_request_user_id)
    dict_user_id = r.json()
    print(json.dumps(dict_user_id, indent=2))
    user_id = dict_user_id['data'].get('user_id')
    return user_id


def get_user_info(user_id, access_token, fields=None):
    default_fields = ['id', 'name', 'first_name', 'last_name', 'age_range', 'link', 'gender', 'locale', 'picture', 'timezone', 'updated_time', 'verified', 'email']
    if fields is None:
        fields = default_fields
    url_request_user_info = 'https://graph.facebook.com/v2.8/' \
                            '{user_id}?' \
                            'fields={fields}&' \
                            'access_token={access_token}'.format(
                                user_id=user_id,
                                fields=','.join(fields),
                                access_token=access_token
                            )
    r = requests.get(url_request_user_info)
    dict_user_info = r.json()
    # print(dict_user_info)
    print(json.dumps(dict_user_info, indent=2))
    return dict_user_info