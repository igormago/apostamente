from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

ENGINE_EXPLORER = 'mysql+mysqlconnector://root:root@localhost/doutorado_explorer'
ENGINE_RESULTADOS = 'mysql+mysqlconnector://root:root@localhost/doutorado_resultados'

class SessionFactory():
    def __init__(self, engine):
        self.engine = create_engine(engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def getSession(self):
        return self.session

sessionExplorer = SessionFactory(ENGINE_EXPLORER).getSession()
sessionResultados = SessionFactory(ENGINE_RESULTADOS).getSession()

Base = declarative_base()
