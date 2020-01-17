def create_query_with_two(*args):
    print(args[0][0], args[0][1])


def create_query_with_one(arg):
    print(arg[0])


def query(create_query, *args):
    create_query(args)


query(create_query_with_one, "1")
query(create_query_with_two, "1", "2")

