from app.models import User, UserRoles, ID_ROLE_MAP
import json
from app.util import date_converter


def get_all_users():
    users = User.query.all()
    json_data = json.dumps(User.serialize_list(users), default=date_converter)
    response = []
    if json_data:
        roles = []
        for jd in json.loads(json_data):
            user_roles = UserRoles.query.filter_by(user_id=jd['id'])
            if user_roles:
                for u_r in user_roles:
                    roles.append(ID_ROLE_MAP.get(u_r))
            response.append([
                jd['id'],
                jd['username'],
                jd['first_name'],
                jd['last_name'],
                jd['mobile'],
                jd['address'],
                roles
            ])
    return {"data": response}

