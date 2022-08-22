def id_check(id_nums: dict, ids: list) -> dict:

    """ Check if Discord user id(s) are in the json database """
    for id in ids:
        if str(id) not in id_nums:
            id_nums[str(id)] = [{"id": id,"amount": 0}]
        
    return id_nums
