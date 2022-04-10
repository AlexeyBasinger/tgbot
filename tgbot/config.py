from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Qiwi_oplata:
    token: str
    wallet: str
    secret_token: str
    open_token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous
    qiwi: Qiwi_oplata


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous(),
        qiwi=Qiwi_oplata(
            token=env.str('QIWI_TOKEN'),
            wallet=env.str('WALLET_QIWI'),
            secret_token=env.str('SECRET_QIWI_KEY'),
            open_token=env.str('OPEN_QIWI_KEY')
        )
    )
