
import sys
import sqlite3

db_file = 'data.db'


def create_tables():
    # Create categories table:
    create_table = "CREATE TABLE IF NOT EXISTS categories " \
                   "(id INTEGER PRIMARY KEY ASC, " \
                   "name varchar(250) NOT NULL)"
    _run_query(create_table)
    # Create items table:
    create_table = "CREATE TABLE IF NOT EXISTS items " \
                   "(id INTEGER PRIMARY KEY ASC," \
                   "name varchar(250) NOT NULL," \
                   "description varchar(250) NOT NULL," \
                   "category_id INTEGER NOT NULL," \
                   "last_modified datetime NOT NULL," \
                   "FOREIGN KEY (category_id) REFERENCES restaurant(id))"
    _run_query(create_table)


def _run_query(query, *args):
    '''
    Run a query on the "news" database
    :param query: string containing the query's SQL statement
    :return: Query result
    '''
    global db_file
    try:
        connection = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print("Unable to connect to database!")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)
    else:
        cursor = connection.cursor()
        result = cursor.execute(query, args)
        connection.commit()
        connection.close()
        return result


if __name__ == '__main__':
    create_tables()
