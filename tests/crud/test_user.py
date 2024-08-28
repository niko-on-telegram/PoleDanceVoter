import pytest

from database.models import User
from database.crud.user import (inc_dec_vote_to_db,
                                get_user_from_db_by_tg_id,
                                get_all_users_ids,
                                add_user_to_db)
