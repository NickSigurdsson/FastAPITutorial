# Describes to sqlalchemy what kind of database files we're going to be creating in the future
# A database table is the actual record that will be inside the database table

from database import Base
from sqlalchemy import Column, Integer, String, Boolean

# This will create the table of todos WITHOUT any records
class Todos(Base):
    __tablename__ = 'todos'

    # index = true will increase performance as it means its unique and queryable
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    description = Column(String)
    priority = Column(String)
    complete = Column(Boolean, default = False)
    