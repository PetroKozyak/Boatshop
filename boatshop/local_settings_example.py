import datetime

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=5),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'education_studio_api.utils.jwt_response_payload_handler'
}