from model import DbConnections
from sqlalchemy import create_engine

################################################
########### DBCONNECTOR CLASS ###############
################################################

class DbConnector:

    def __init__(self, db_type, user, password, hostname, schema, port=None, name=None):
        
        # setting up propeties
        self.db_type = db_type
        self.schema = schema
        self.user = user
        self.password = password
        self.hostname = hostname
        self.port = port
        self.connection = None
        self.message = ''
        
        # assinging name - if no name is given then the name is composed of the type and schema
        if name or name == '':
            self.name = name
        else:
            self.name = self.db_type + self.schema

        # checking db type
        if self.port == '':
            if db_type == 'ORACLE':
                self.conn_string =f"oracle+cx_oracle://{self.user}:{self.password}@{self.hostname}/{self.schema}"
            elif db_type == 'SQLITE':
                self.conn_string = f'sqlite://{self.user}:{self.password}@{self.hostname}/{self.schema}'
            elif db_type == 'POSTGRESQL':
                self.conn_string = f"postgresql://{self.user}:{self.password}@{self.hostname}/{self.schema}"
            elif db_type == 'MYSQL':
                self.conn_string = f'mysql+mysqlconnector://{self.user}:{self.password}@{self.hostname}/{self.schema}'
            else:
                self.conn_string = None
                self.message = 'Database type not found. Possible types are :\n'
                'ORACLE, SQLITE, POSTGRESQL, MYSQL'
        else:
            if db_type == 'ORACLE':
                self.conn_string =f"oracle+cx_oracle://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.schema}"
            elif db_type == 'SQLITE':
                self.conn_string = f'sqlite://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.schema}'
            elif db_type == 'POSTGRESQL':
                self.conn_string = f"postgresql://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.schema}"
            elif db_type == 'MYSQL':
                self.conn_string = f'mysql+mysqlconnector://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.schema}'
            else:
                self.conn_string = None
                self.message = 'Database type not found. Possible types are :\n'
                'ORACLE, SQLITE, POSTGRESQL, MYSQL'
        # checking if we have a connection string and can try to connect
        if self.conn_string:
            try:
                self.connection = create_engine(self.conn_string, connect_args={'connect_timeout': 10})
                conn = self.connection.connect()
                conn.close()
                self.connection.dispose()
            except Exception as error:
                self.message = 'Someting went wrong while trying to connect.'
                try:
                    self.connection.dispose()
                except Exception as error:
                    pass
        # setting the connection status
        if self.message == '':
            self.status = 'valid'
        else:
            self.status = 'invalid'

    def save(self):
        # checking id connectiong is valid - cannot save invalid connection
        if self.status == 'invalid':
            self.message = 'Cannot save invalid connection'
            return

        # checking if the name exists - names must be unique
        if DbConnections.query.filter_by(name=self.name).first():
            self.message = 'cannot save - db name already exist'
            self.status = 'invalid'
            return
        # saving connection data to DB
        try:
            conn = DbConnections(self.db_type, self.user, self.password, self.hostname, self.port, self.schema, self.name, self.conn_string)
            db.session.add(conn)
            db.session.commit()
        except Exception as error:
            self.message = 'Something when wrong while saving to DB.'
            self.status = 'invalid'