def id_check(id_nums: dict, ids: list) -> dict:
    """ Boolean variable that states whether all passed-in ids exist in the database"""
    id_exists = True
    """ Check if Discord user id(s) are in the json database """
    for id in ids:
        if str(id) not in id_nums:
            print(str(id) + " does not exist in the database!")
            id_exists = False # If one of the ids passed in does not exist, return false so that the user can intialise themselves

    return id_exists