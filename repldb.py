import os

f=open("repldb.txt", "w")
f.write(os.environ["REPLIT_DB_URL"])
f.close()