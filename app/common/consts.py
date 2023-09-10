import environ


# 환경변수 init
env = environ.Env()
env.read_env(env.str("ENV_PATH", ".env"))

ALLOWED_HOSTS: list = env("ALLOWED_HOSTS").split(" ")

# database
DB_URL = f"postgresql://{env('DB_USER')}:{env('DB_PASSWORD')}@{env('DB_HOST')}/{env('DB_NAME')}"

# jwt
JWT_SECRET = env("JWT_SECRET")
JWT_ALGORITHM = env("JWT_ALGORITHM")

# nice api
NICE_URL = "https://open.neis.go.kr/hub"
NICE_API_KEY = env("NICE_API_KEY")

# django
DJANGO_SECRET_KEY = env("DJANGO_SECRET_KEY")
