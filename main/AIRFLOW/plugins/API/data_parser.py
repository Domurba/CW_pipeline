def user_from_dict(data):
    return (
        data["ranks"]["overall"]["name"],
        data["username"],
        data["honor"],
        data["leaderboardPosition"],
        data["codeChallenges"]["totalCompleted"],
        *data["ranks"]["languages"].keys(),
    )


def kata_from_dict(kata):
    return (
        kata["id"],
        kata["name"],
        kata["completedAt"],
        tuple(kata["completedLanguages"]),
    )


def kata_info_from_dict(kata):
    return (kata["name"], kata["rank"]["id"], kata["description"])
