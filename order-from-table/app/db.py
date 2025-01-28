import psycopg2
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
import logging
from typing import Optional, Any
import urllib.parse

logger = logging.getLogger(__name__)

class DatabaseHandler:
    def __init__(self, database_url: str):
        """Initialize database handler with connection pool."""
        try:
            # Parse the database URL to get individual components
            parsed = urllib.parse.urlparse(database_url)
            
            self.pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                host=parsed.hostname,
                port=parsed.port or 5432,
                dbname=parsed.path[1:],  # Remove leading slash
                user=parsed.username,
                password=parsed.password
            )
            logger.info("Database connection pool initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise

    @contextmanager
    def get_connection(self):
        """Context manager for getting a connection from the pool."""
        conn = self.pool.getconn()
        try:
            yield conn
        finally:
            self.pool.putconn(conn)

    @contextmanager
    def get_cursor(self, conn):
        """Context manager for database cursor operations."""
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

    def execute_query(self, query, params=None, fetchone=False, fetchall=False):
        """Execute a query with error handling."""
        try:
            with self.get_connection() as conn:
                with self.get_cursor(conn) as cursor:
                    cursor.execute(query, params)
                    if fetchone:
                        return cursor.fetchone()
                    if fetchall:
                        return cursor.fetchall()
        except psycopg2.Error as e:
            logger.error(f"Database error in execute_query: {e}")
            raise

    def close_pool(self):
        """Close the connection pool."""
        if self.pool:
            self.pool.closeall()
            logger.info("Database connection pool closed")