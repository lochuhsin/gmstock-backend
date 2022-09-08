from utils.singleton import MongoDB


def get_collections():
    return MongoDB().db.list_collection_names()


def get_timserise_by_symbol(unique: str):

    collection = MongoDB().db[unique]
    return collection.find({})
