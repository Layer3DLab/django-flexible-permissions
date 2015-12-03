from permissions.utils import normalize_value

"""
Maps of roles to actions
"""

ROLES = {}
ACTIONS = {}


def calculate_actions(roles):
    result = {}
    for role, actions in roles.items():
        for action in actions:
            result.setdefault(action, [])
            result[action].append(role)
            result[action] = list(set(result[action]))

    return result


def register_role(name, actions):
    global ACTIONS

    for action in actions:
        if action.count(".") != 1:
            raise ValueError(
                "Actions should have one period in them - the left portion"
                "should be the name of the object; the right the name of the"
                "action."
            )

    # Merge the actions together
    pre_existing_actions = ROLES.get(name, [])
    ROLES[name] = list(set(actions + pre_existing_actions))

    # Keep action map in sync
    ACTIONS = calculate_actions(ROLES)


def roles_to_actions(roles):
    roles = normalize_value(roles)
    return list(set([action for role in roles for action in ROLES[role]]))


def actions_to_roles(actions):
    actions = normalize_value(actions)
    return list(set([role for action in actions for role in ACTIONS[action]]))
