from database.models import User


empty_tg_id = 361557982


def get_default_user() -> User:
    return User(telegram_id=361557982, fullname="Greed", count_votes=0)


def get_default_user_username() -> User:
    return User(telegram_id=361557982, username="Uff", fullname="Greed", count_votes=0)


def get_defult_user_list() -> list[User]:
    return [
        User(telegram_id=361557982, fullname="User1", count_votes=0),
        User(telegram_id=361557984, fullname="User2", count_votes=1),
        User(telegram_id=361557985, fullname="User3", count_votes=2),
        User(telegram_id=361557986, fullname="User4", count_votes=3),
        User(telegram_id=361557987, fullname="User5", count_votes=4),
    ]


def get_defult_user_list_username() -> list[User]:
    return [
        User(telegram_id=361557982, fullname="User1", count_votes=0),
        User(telegram_id=361557984, fullname="User2", count_votes=1),
        User(telegram_id=361557985, fullname="User3", count_votes=2),
        User(telegram_id=361557986, fullname="User4", count_votes=3),
        User(telegram_id=361557987, fullname="User5", count_votes=4),
    ]
