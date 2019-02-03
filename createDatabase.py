from srModule import Database
import sys


if __name__ == "__main__":
    print("Check connection with the database......",end="")
    status, code, msg = Database.checkDatabase()
    if status:
        print("Success!")
        print("Tables already exists")
        sys.exit()
    if code != "f405":
        print("Connect to database failed: %s" % msg)
        print("Please check your config")
        sys.exit()
    print("Creating tables......",end="")
    Database.createTables()
    print("Success! ")