from config.env import env

EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_USE_TLS = env("EMAIL_USE_TLS", default=True)
EMAIL_PORT = env("EMAIL_PORT", default=587)
# fake values below exist to avoid any ImproperlyConfigured exception.
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="fakemail@gmail.com")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="fakepassword")
