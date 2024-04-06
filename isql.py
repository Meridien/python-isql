"""Interactive SQLITE prompt"""
# python-isql
# https://github.com/Meridien/python-isql

import sqlite3
import glob

import cmd2
from cmd2 import Cmd2ArgumentParser


def dict_factory(cursor, row):
    """return records as a dictionary object"""
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}


# ---- SETUP
parser = Cmd2ArgumentParser()
parser.add_argument("--new", "-n", action="store_true")
parser.add_argument("--dbfile", "-f", type=str, required=False)
args = parser.parse_args()


def select_db_file():
    """determine db to connect to"""

    db_files = list(glob.iglob("*.db"))
    db_file_selection = str("")

    if len(db_files) > 1:
        db_file_counter = int(0)
        for db_file in db_files:
            print(str(db_file_counter) + ": " + str(db_file))
            db_file_counter += 1
        print(str(db_file_counter) + ": " + "New DB")
        db_file_selector = int(input("Select DB File: "))
        if db_file_selector == db_file_counter:
            new_db_filename = input("Filename for New DB: ")
            db_file_selection = new_db_filename
        else:
            db_file_selection = db_files[db_file_selector]
    else:
        db_file_selection = str(db_files[0])

    if args.new is True:
        new_db_filename = input("Filename for New DB: ")
        db_file_selection = new_db_filename

    if args.dbfile is not None:
        db_file_selection = args.dbfile
    print("Database: " + db_file_selection + "\n")
    return db_file_selection


class SqliteShell(cmd2.Cmd):
    """Main class for isql - sql commands"""

    intro = "Welcome to the sqlite shell. Type help or ? to list commands.\n"
    prompt = "SQLITE> "
    file = None
    use_rawinput = True

    def __init__(self):
        super().__init__(
            allow_cli_args=False,
            multiline_commands=["echo"],
            persistent_history_file="isqlhist",
            persistent_history_length=100,
        )
        self.db_filename = select_db_file()
        self.db_instance = sqlite3.connect(self.db_filename)
        self.db_instance.row_factory = dict_factory
        self.cur = self.db_instance.cursor()

    def do_select(self, arg):
        """Select Records"""
        sql = parse(arg)
        res = self.cur.execute(str("select " + sql))
        for row in res.fetchall():
            print(row)

    def do_update(self, arg):
        """Update Records"""
        sql = parse(arg)
        res = self.cur.execute(str("update " + sql))
        sql = """select changes(),total_changes();"""
        res = self.cur.execute(sql)
        print(res.fetchall())
        commit = input("Commit? y or n: ")
        if commit == "y":
            self.db_instance.commit()
        print(res.fetchall())

    def do_insert(self, arg):
        """Insert Records"""
        sql = parse(arg)
        res = self.cur.execute(str("insert " + sql))
        sql = """select changes(),total_changes();"""
        res = self.cur.execute(sql)
        print(res.fetchall())
        commit = input("Commit? y or n: ")
        if commit == "y":
            self.db_instance.commit()
        print(res.fetchall())

    def do_delete(self, arg):
        """Delete Records"""
        sql = parse(arg)
        res = self.cur.execute(str("delete " + sql))
        sql = """select changes(),total_changes();"""
        res = self.cur.execute(sql)
        print(res.fetchall())
        commit = input("Commit? y or n: ")
        if commit == "y":
            self.db_instance.commit()
        print(res.fetchall())

    def do_create(self, arg):
        """Create Objects"""
        sql = parse(arg)
        res = self.cur.execute(str("create " + sql))
        sql = """select changes(),total_changes();"""
        res = self.cur.execute(sql)
        print(res.fetchall())
        commit = input("Commit? y or n: ")
        if commit == "y":
            self.db_instance.commit()
        res = self.cur.execute("""select * from sqlite_master""")
        for row in res:
            print(row)

    def do_alter(self, arg):
        """Alter Objects"""
        sql = parse(arg)
        res = self.cur.execute(str("alter " + sql))
        commit = input("Commit? y or n: ")
        if commit == "y":
            self.db_instance.commit()
        res = self.cur.execute("""select * from sqlite_master""")
        for row in res:
            print(row)

    def do_drop(self, arg):
        """Drop Objects"""
        sql = parse(arg)
        res = self.cur.execute(str("drop " + sql))
        commit = input("Commit? y or n: ")
        if commit == "y":
            self.db_instance.commit()
        res = self.cur.execute("""select * from sqlite_master""")
        for row in res:
            print(row)


def parse(arg):
    """just return a string"""
    return str(arg)


if __name__ == "__main__":
    # command loop
    SqliteShell().cmdloop()
