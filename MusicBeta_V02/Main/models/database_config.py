from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Base: Todos os seus modelos herdarão desta base.
Base = declarative_base()

# Session: Usada nos controllers para queries e commits.
Session = scoped_session(sessionmaker())