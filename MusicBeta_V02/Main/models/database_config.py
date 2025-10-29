# models/database_config.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Base é onde seus modelos Usuario e CicloDeEstudo devem herdar.
Base = declarative_base()

# Session será usada nos controllers para queries e commits.
Session = scoped_session(sessionmaker())