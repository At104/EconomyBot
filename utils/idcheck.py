def id_check(idNums: dict, id: int) -> dict:

    """ Check if Discord user id is in the json database """
    if str(id) not in idNums:
        idNums[str(id)] = [{"id": id,"amount": 0}]
        
    return idNums