from srModule.Database import Base,initSession,createDB

db,engine = initSession()
createDB(Base,engine)