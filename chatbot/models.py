from pony.orm import Database, Required, Json

from settings import DB_CONFIG

db = Database()
db.bind(**DB_CONFIG)


class UserState(db.Entity):
    """
    Состояние пользователя внутри сценария.
    Поля:
    - user_id: text, id пользователя
    - name: text, имя пользователя
    - photo: text, url-путь до аватара пользователя
    - scenario_name: text, имя текущего сценария
    - step_name: text, имя текуего шага
    - context: jsonb, контекст (словарь с ответами пользователя)
    """

    user_id = Required(str, unique=True)
    name = Required(str)
    photo = Required(str)
    scenario_name = Required(str)
    step_name = Required(str)
    context = Required(Json)


class Registration(db.Entity):
    """
    Зарегистрированный билет.
    Поля:
    - name: text, имя пользователя
    - context: jsonb, контекст (словарь с данными регистрации)
    """

    name = Required(str)
    context = Required(Json)


db.generate_mapping(create_tables=True)

