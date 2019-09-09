#TODO: Add logging
def db_size(db_name):
    return """SELECT pg_size_pretty(pg_database_size({})""".format(db_name)

