# Import libraries
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import IntegrityError, OperationalError
import atexit 
from dscommon.log import LOG
from dscommon.util import QueryEnum

class DbHandler():
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.connect(database, user, password, host, port)

        atexit.register(self.close)
     
    def connect(self, database, user, password, host, port):
        conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        conn.autocommit = True
        self.conn = conn
    
    def ensure_connection(self):
        """Ensure that the connection to the database is active."""
        try:
            self.conn.cursor().execute('SELECT 1')
        except (OperationalError, psycopg2.InterfaceError) as e:
            LOG.warning(f"Connection lost: {e}. Reconnecting...")
            self.connect(self.database, self.user, self.password, self.host, self.port)
            
    def read(self, query):
        self.ensure_connection()
        if self.conn:
            results = None
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                sql = query
                cur.execute(sql)
                results = cur.fetchone()
            return results
    
    def read_many(self, query):
        self.ensure_connection()
        if self.conn:
            results = None
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                sql = query
                cur.execute(sql)
                results = cur.fetchall()
            return results

    def insert(self, query, data, hideerrormsg=False):
        self.ensure_connection()
        try:
            if self.conn:
               success = QueryEnum.FAIL
               with self.conn.cursor() as cur:
                   sql = query
                   cur.execute(sql, data)

                   if cur.rowcount >= 1:
                       success = QueryEnum.SUCCESS
                   else:
                       success = QueryEnum.FAIL
                   self.conn.commit()
               return success
        except IntegrityError as e:
            if not hideerrormsg:
                LOG.error(f"Insert operation failed due to duplicate key: {e}")
            return QueryEnum.DUPLICATE
        except Exception as e:
            LOG.error(f"{e}")
            return QueryEnum.FAIL
    
    def insert_many(self, query, data, hideerrormsg=False):
        self.ensure_connection()
        try:
            if self.conn:
               success = QueryEnum.FAIL
               with self.conn.cursor() as cur:
                   sql = query
                   cur.executemany(sql, data)

                   if cur.rowcount >= 1:
                       success = QueryEnum.SUCCESS
                   else:
                       success = QueryEnum.FAIL
                   self.conn.commit()
               return success
        except IntegrityError as e:
            if not hideerrormsg:
                LOG.error(f"Insert operation failed due to duplicate key: {e}")
            return QueryEnum.DUPLICATE
        except Exception as e:
            LOG.error(f"{e}")
            return QueryEnum.FAIL

    def update(self, query, data=None, hideerrormsg=False):
        self.ensure_connection()
        try:
            if self.conn:
               success = QueryEnum.FAIL
               with self.conn.cursor() as cur:
                    sql = query
                    if data is not None:
                        cur.execute(sql, data)
                    else:
                       cur.execute(sql)

                    if cur.rowcount >= 1:
                       success = QueryEnum.SUCCESS
                    else:
                       success = QueryEnum.FAIL
                    self.conn.commit()
               return success
        except IntegrityError as e:
            if not hideerrormsg:
                LOG.error(f"Update operation failed due to duplicate key: {e}")
            return QueryEnum.DUPLICATE
        except Exception as e:
            LOG.error(f"{e}")
            return QueryEnum.FAIL
    
    def general_no_data(self, query, hideerrormsg=False):
        self.ensure_connection()
        try:
            if self.conn:
               success = QueryEnum.FAIL
               with self.conn.cursor() as cur:
                    sql = query
                    cur.execute(sql)

                    # Delete tidak selalu rowcount >= 1
                    success = QueryEnum.SUCCESS
                #    if cur.rowcount >= 1:
                #        success = QueryEnum.SUCCESS
                #    else:
                #        success = QueryEnum.FAIL
                    self.conn.commit()
               return success, cur.rowcount
            else:
                LOG.error(f"No DB Connection")
                return QueryEnum.FAIL, 0
        except IntegrityError as e:
            if not hideerrormsg:
                LOG.error(f"{e}")
            return QueryEnum.DUPLICATE, 0
        except Exception as e:
            LOG.error(f"{e}")
            return QueryEnum.FAIL, 0
        
    def close(self):
        LOG.info('Database connection closed')
        if self.conn:
            self.conn.close()


if __name__ == '__main__':
    db = DbHandler(database="coba", user='postgres', password='bandung', host='localhost', port='5432')
    print(db.read(''))