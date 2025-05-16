import time
import logging
import contextlib
from typing import List, Tuple, Any, Optional, Union, Dict, Callable
import mysql.connector
from mysql.connector.cursor import MySQLCursor
from mysql.connector import MySQLConnection
import pandas as pd
import config

logger = logging.getLogger('db_functions')


class DatabaseOperation:
    """Context manager for database operations with a new connection."""
    
    def __init__(self, operation_name: str = "database operation"):
        """Initialize a new database operation context.
        
        Args:
            operation_name: Name of the operation for logging purposes
        """
        self.connection = None
        self.cursor = None
        self.operation_name = operation_name
        
    def __enter__(self):
        """Set up the database connection and cursor."""
        try:
            # Wait a small amount to ensure any previous operations finish
            time.sleep(0.2)
            
            # Create a fresh connection
            self.connection = mysql.connector.connect(
                host=config.SQL_HOST,
                user=config.SQL_USR,
                password=config.SQL_PWD,
                database=config.SQL_WP_DB,
                auth_plugin='mysql_native_password'
            )
            # Use buffered cursor to ensure results are always consumed
            self.cursor = self.connection.cursor(buffered=True)
            logger.debug(f"Created new connection for {self.operation_name}")
            return self
        except Exception as e:
            logger.error(f"Failed to create database connection for {self.operation_name}: {e}")
            # Clean up partial resources if needed
            self._cleanup()
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources and handle any errors."""
        if exc_type is not None:
            # If an exception occurred, roll back any changes
            logger.error(f"Error during {self.operation_name}: {exc_val}")
            if self.connection is not None and self.connection.is_connected():
                try:
                    self.connection.rollback()
                    logger.debug(f"Rolled back transaction for {self.operation_name}")
                except Exception as e:
                    logger.error(f"Failed to rollback transaction: {e}")
        
        # Always clean up resources
        self._cleanup()
        
        # Don't suppress the exception
        return False
    
    def _cleanup(self):
        """Clean up database resources."""
        try:
            if self.cursor is not None:
                self.cursor.close()
            if self.connection is not None and self.connection.is_connected():
                self.connection.close()
                logger.debug(f"Closed connection for {self.operation_name}")
        except Exception as e:
            logger.error(f"Error closing database resources: {e}")
    
    def execute(self, sql: str, params=None) -> bool:
        """Execute a single SQL statement.
        
        Args:
            sql: The SQL statement to execute
            params: Parameters for the SQL statement
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.cursor.execute(sql, params)
            
            # For non-SELECT queries, commit changes
            if not sql.strip().upper().startswith("SELECT"):
                self.connection.commit()
                logger.debug(f"Executed and committed: {sql[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Error executing SQL: {e}\nSQL: {sql}\nParams: {params}")
            return False
    
    def executemany(self, sql: str, params_list=None) -> int:
        """Execute a SQL statement with multiple parameter sets.
        
        Args:
            sql: The SQL statement to execute
            params_list: List of parameter tuples
            
        Returns:
            int: Number of rows affected
        """
        try:
            self.cursor.executemany(sql, params_list)
            self.connection.commit()
            rowcount = self.cursor.rowcount
            logger.debug(f"Executed batch with {rowcount} rows affected")
            return rowcount
        except Exception as e:
            logger.error(f"Error executing batch SQL: {e}\nSQL: {sql}")
            return 0
    
    def query(self, sql: str, params=None) -> List[Tuple]:
        """Execute a SELECT query and return results.
        
        Args:
            sql: The SQL query
            params: Parameters for the query
            
        Returns:
            List[Tuple]: Query results
        """
        try:
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            logger.debug(f"Query returned {len(result)} rows")
            return result
        except Exception as e:
            logger.error(f"Error executing query: {e}\nSQL: {sql}\nParams: {params}")
            return []
            
    def delete(self, table: str, condition: str = None, params=None) -> bool:
        """Delete records from a table.
        
        Args:
            table: Table name
            condition: WHERE clause without the 'WHERE' keyword
            params: Parameters for the condition
            
        Returns:
            bool: True if successful, False otherwise
        """
        sql = f"DELETE FROM {table}"
        if condition:
            sql += f" WHERE {condition}"
        return self.execute(sql, params)


# Convenience functions for creating a new connection for each operation
def with_new_connection(operation_name: str = "operation"):
    """Context manager for database operations with a new connection.
    
    Usage:
        with with_new_connection("my operation") as db:
            db.execute("INSERT INTO table VALUES (%s)", (value,))
    """
    return DatabaseOperation(operation_name)


def execute_with_new_connection(sql: str, params=None, operation_name: str = "SQL execute") -> bool:
    """Execute an SQL statement with a fresh connection.
    
    Args:
        sql: The SQL statement
        params: Parameters for the SQL statement
        operation_name: Name for logging
        
    Returns:
        bool: True if successful, False otherwise
    """
    with DatabaseOperation(operation_name) as db:
        return db.execute(sql, params)


def query_with_new_connection(sql: str, params=None, operation_name: str = "SQL query") -> List[Tuple]:
    """Execute a query with a fresh connection.
    
    Args:
        sql: The SQL query
        params: Parameters for the SQL query
        operation_name: Name for logging
        
    Returns:
        List[Tuple]: Query results
    """
    with DatabaseOperation(operation_name) as db:
        return db.query(sql, params)


def batch_insert_with_new_connection(table: str, columns: List[str], values_list: List[Tuple], 
                                   operation_name: str = "batch insert") -> int:
    """Insert multiple rows with a fresh connection.
    
    Args:
        table: Table name
        columns: List of column names
        values_list: List of value tuples
        operation_name: Name for logging
        
    Returns:
        int: Number of rows inserted
    """
    placeholders = ", ".join(["%s"] * len(columns))
    columns_str = ", ".join(columns)
    sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
    
    with DatabaseOperation(operation_name) as db:
        return db.executemany(sql, values_list)

def mysql_exec(cursor: MySQLCursor, sql: Union[str, List[str]], val: Optional[Union[Tuple[Any, ...], List[Tuple[Any, ...]]]] = None) -> None:
    """
    Execute SQL commands with proper error handling and retry logic.
    
    Args:
        cursor: MySQL cursor object
        sql: SQL command or list of SQL commands
        val: Parameters for SQL command or list of parameters for SQL commands
    
    Raises:
        Exception: If SQL execution fails after retry
    """
    def _consume_if_needed(cursor, sql_cmd):
        """Helper to consume results if needed to prevent 'unread result' errors"""
        if hasattr(cursor, '_have_unread_result') and cursor._have_unread_result():
            # Only consume results for non-SELECT queries
            if not sql_cmd.strip().upper().startswith("SELECT"):
                cursor.fetchall()
    
    if isinstance(sql, list):
        for idx, (s, v) in enumerate(zip(sql, val or [])):
            try:
                cursor.execute(s, v)
                _consume_if_needed(cursor, s)
            except Exception as e:
                logger.warning(f"SQL execution failed (attempt 1): {e}\nSQL: {s}\nValues: {v}")
                time.sleep(0.2)
                try:
                    cursor.execute(s, v)
                    _consume_if_needed(cursor, s)
                except Exception as e:
                    logger.error(f"SQL execution failed (attempt 2): {e}\nSQL: {s}\nValues: {v}")
                    raise
    else:
        try:
            cursor.execute(sql, val)
            _consume_if_needed(cursor, sql)
        except Exception as e:
            logger.warning(f"SQL execution failed (attempt 1): {e}\nSQL: {sql}\nValues: {val}")
            time.sleep(0.2)
            try:
                cursor.execute(sql, val)
                _consume_if_needed(cursor, sql)
            except Exception as e:
                logger.error(f"SQL execution failed (attempt 2): {e}\nSQL: {sql}\nValues: {val}")
                raise
    return

def mysql_update(db: MySQLConnection, cursor: MySQLCursor, sql_list: Union[str, List[str]], 
                val_list: Optional[Union[Tuple[Any, ...], List[Tuple[Any, ...]]]] = None) -> None:
    """
    Execute SQL update commands and commit changes to database.
    
    Args:
        db: MySQL database connection
        cursor: MySQL cursor object
        sql_list: SQL command or list of SQL commands
        val_list: Parameters for SQL command or list of parameters for SQL commands
    """
    mysql_exec(cursor, sql_list, val_list)
    db.commit()
    time.sleep(0.2)
    return

def select_data(sql: str, params=None, operation_name: str = "Select data", include_columns: bool = False) -> Union[List[Tuple], Tuple[List[Tuple], List[str]]]:
    """Convenient query function, auto-create new connection
    
    Args:
        sql: SQL query statement
        params: SQL parameters
        operation_name: Operation name (for logging)
        include_columns: Whether to also return column names (default is False)
        
    Returns:
        If include_columns is False, only return query results list
        If include_columns is True, return a tuple of (query results list, column names list)
    """
    with DatabaseOperation(operation_name) as db:
        try:
            db.cursor.execute(sql, params)
            results = db.cursor.fetchall()
            
            if include_columns and db.cursor.description:
                columns = [desc[0] for desc in db.cursor.description]
                return results, columns
            return results
        except Exception as e:
            logger.error(f"Error in {operation_name}: {e}\nSQL: {sql}\nParams: {params}")
            if include_columns:
                return [], []
            return []


def get_dataframe(sql: str, params=None, operation_name: str = "Get DataFrame") -> pd.DataFrame:
    """Convert SQL query result to DataFrame directly
    
    Args:
        sql: SQL query statement
        params: SQL parameters
        operation_name: Operation name (for logging)
        
    Returns:
        pd.DataFrame: DataFrame containing query results, empty DataFrame if query fails
    """
    try:
        with DatabaseOperation(operation_name) as db:
            db.cursor.execute(sql, params)
            results = db.cursor.fetchall()
            if results and db.cursor.description:
                columns = [desc[0] for desc in db.cursor.description]
                return pd.DataFrame(results, columns=columns)
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error in {operation_name}: {e}\nSQL: {sql}\nParams: {params}")
        return pd.DataFrame()


def insert_data(table: str, data: Dict[str, Any], operation_name: str = "Insert data") -> bool:
    """Convenient insert function, auto-create new connection
    
    Args:
        table: Table name
        data: Dictionary of data to insert {column: value}
        operation_name: Operation name (for logging)
        
    Returns:
        Whether the operation was successful
    """
    columns = list(data.keys())
    placeholders = ", ".join([f"%s"] * len(columns))
    columns_str = ", ".join([f"`{col}`" for col in columns])
    values = tuple(data.values())
    
    sql = f"INSERT INTO `{table}` ({columns_str}) VALUES ({placeholders})"
    return execute_with_new_connection(sql, values, operation_name)


def update_data(table: str, data: Dict[str, Any], condition: str, condition_params=None, operation_name: str = "Update data") -> bool:
    """Convenient update function, auto-create new connection
    
    Args:
        table: Table name
        data: Dictionary of data to update {column: new_value}
        condition: WHERE condition (without WHERE keyword)
        condition_params: Condition parameters
        operation_name: Operation name (for logging)
        
    Returns:
        Whether successful
    """
    set_clauses = [f"`{col}` = %s" for col in data.keys()]
    set_clause = ", ".join(set_clauses)
    values = list(data.values())
    
    sql = f"UPDATE `{table}` SET {set_clause} WHERE {condition}"
    
    # 合并参数
    all_params = values
    if condition_params:
        if isinstance(condition_params, (list, tuple)):
            all_params.extend(condition_params)
        else:
            all_params.append(condition_params)
    
    return execute_with_new_connection(sql, tuple(all_params), operation_name)


def delete_data(table: str, condition: str = None, condition_params=None, operation_name: str = "Delete data") -> bool:
    """Convenient delete function, auto-create new connection
    
    Args:
        table: Table name
        condition: WHERE condition (without WHERE keyword)
        condition_params: Condition parameters
        operation_name: Operation name (for logging)
        
    Returns:
        Whether successful
    """
    sql = f"DELETE FROM `{table}`"
    if condition:
        sql += f" WHERE {condition}"
        
    return execute_with_new_connection(sql, condition_params, operation_name)

def get_strategy_name_list() -> List[str]:
    """Get list of all strategy names from database.
    
    Returns:
        List of strategy names
    """
    result = query_with_new_connection(
        "SELECT `strategy_name` FROM `onglory_strategies` WHERE 1",
        operation_name="Get strategy name list"
    )
    strategy_name_list = [name_tuple[0] for name_tuple in result]
    return strategy_name_list

def get_quant_name_list() -> List[str]:
    """Get list of all quantitative strategy names from database.
    
    Returns:
        List of quantitative strategy names
    """
    result = query_with_new_connection(
        "SELECT `strategy_name` FROM `onglory_strategies` WHERE `strategy_type`='QUANT'", 
        operation_name="Get quant name list"
    )
    quant_name_list = [name_tuple[0] for name_tuple in result]
    return quant_name_list

def get_quant_spot_name_list() -> List[str]:
    """Get list of all quantitative spot strategy names from database.
    
    Returns:
        List of quantitative spot strategy names
    """
    result = query_with_new_connection(
        "SELECT `strategy_name` FROM `onglory_strategies` WHERE `strategy_type`='QUANT' AND `strategy_subtype`='SPOT'",
        operation_name="Get quant spot name list"
    )
    quant_spot_name_list = [name_tuple[0] for name_tuple in result]
    return quant_spot_name_list

def get_quant_future_name_list() -> List[str]:
    """Get list of all quantitative futures strategy names from database.
        
    Returns:
        List of quantitative futures strategy names
    """
    result = query_with_new_connection(
        "SELECT `strategy_name` FROM `onglory_strategies` WHERE `strategy_type`='QUANT' AND `strategy_subtype`='FUTURE'",
        operation_name="Get quant future name list"
    )
    quant_future_name_list = [name_tuple[0] for name_tuple in result]
    return quant_future_name_list

def get_manual_name_list() -> List[str]:
    """Get list of all manual strategy names from database.
    
    Returns:
        List of manual strategy names
    """
    result = query_with_new_connection(
        "SELECT `strategy_name` FROM `onglory_strategies` WHERE `strategy_type`='MANUAL'",
        operation_name="Get manual name list"
    )
    manual_name_list = [name_tuple[0] for name_tuple in result]
    return manual_name_list

def get_grid_name_list() -> List[str]:
    """Get list of all grid strategy names from database.
    
    Returns:
        List of grid strategy names
    """
    result = query_with_new_connection(
        "SELECT `strategy_name` FROM `onglory_strategies` WHERE `strategy_type`='GRID'",
        operation_name="Get grid name list"
    )
    grid_name_list = [name_tuple[0] for name_tuple in result]
    return grid_name_list

def get_manual_asset_amount(strategy_name: Optional[str] = None) -> List[Tuple]:
    """
    Get manual asset amounts for a specific strategy or all strategies.
    
    Args:
        strategy_name: Optional strategy name to filter results
    
    Returns:
        List of tuples containing asset amounts
    """
    if strategy_name is None:
        return query_with_new_connection(
            "SELECT `asset`, `amount`, `strategy_name`, `subaccount_name` FROM `onglory_manual_asset_amount` WHERE 1",
            operation_name="Get manual asset amounts"
        )
    else:
        return query_with_new_connection(
            "SELECT `asset`, `amount`, `strategy_name`, `subaccount_name` FROM `onglory_manual_asset_amount` WHERE `strategy_name`=%s", 
            (strategy_name,),
            operation_name=f"Get manual asset amounts for {strategy_name}"
        )
