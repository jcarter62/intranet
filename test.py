from decouple import config


def dumpe():
    print('debug:' + config('DEBUG'))
    print('allowed_hosts:' + config('ALLOWED_HOSTS'))
    print('csrf_use_sessions:' + config('CSRF_USE_SESSIONS'))
    print('csrf_trusted_origins:' + config('CSRF_TRUSTED_ORIGINS'))
    print('secret_key:' + config('SECRET_KEY'))
    print('dbpath:' + config('DBPATH'))
    print('default_from_email:' + config('DEFAULT_FROM_EMAIL'))
    print('email_host:' + config('EMAIL_HOST'))
    print('email_port:' + config('EMAIL_PORT'))
    print('host:' + config('HOST'))
    print('port:' + config('PORT'))
    return
