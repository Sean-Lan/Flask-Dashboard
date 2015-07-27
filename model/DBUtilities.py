import sqlite3
from DBConfig import *

def connect_db(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn


class Model:
    """ORM class, support basic INSERT, DELETE, UPDATE and SELECT operation.
       No extra check to be done when excute SQL, and Use Exception to indicate
       record missing, etc.
    """
    def __init__(self, table_name):
        self.table_name = table_name
        self.conn = connect_db()
    
    def __del__(self):
        self.conn.close()

    def insert(self, column_dict):
        SQL = """INSERT INTO {table_name} {keys}
                 VALUES {values}
              """
        values = '(:'+ ', :'.join(column_dict.keys()) + ')'
        SQL = SQL.format(table_name = self.table_name, 
                keys = tuple(column_dict.keys()),
            values = values)
        self.conn.execute(SQL, column_dict)
        self.conn.commit()

    def update(self, column_dict, condition_dict):
        SQL = """UPDATE {table_name} 
                 {set_section}
                 WHERE {condition_section}
              """
        set_section = reduce(lambda sql, item: sql + item + '= :' + item + ',',
                column_dict.keys(), 'SET ').rstrip(',')
        condition_section = reduce(lambda sql, item: sql + item + '= :' + item + ' AND ',
                condition_dict.keys(), '')
        if condition_section.endswith(' AND '):
            condition_section = condition_section[:-5]
        SQL = SQL.format(table_name = self.table_name,
                   set_section = set_section,
                   condition_section = condition_section)
        sql_dict = dict(column_dict)
        sql_dict.update(condition_dict) 
        self.conn.execute(SQL, sql_dict)
        self.conn.commit()

    def delete(self, condition_dict):
        SQL = """DELETE FROM {table_name}
                 WHERE {condition_section}
              """
        condition_section = reduce(lambda sql, item: sql + item + '= :' + item + ' AND ',
                condition_dict.keys(), '')
        if condition_section.endswith(' AND '):
            condition_section = condition_section[:-5]
        SQL = SQL.format(table_name = self.table_name,
                condition_section = condition_section)
        self.conn.execute(SQL, columns_list, condition_dict)
        self.conn.commit()

    def select(self, columns_list, condition_dict):
        SQL = """SELECT {columns_section}
                 FROM {table_name}
                 WHERE {condition_section}
              """
        condition_section = reduce(lambda sql, item: sql + item + '= :' + item + ' AND ',
                condition_dict.keys(), '')
        if condition_section.endswith(' AND '):
            condition_section = condition_section[:-5]
        SQL = SQL.format(table_name = self.table_name,
                columns_section = ', '.join(columns_list),
                condition_section = condition_section)
        cursor = self.conn.cursor()
        cursor.execute(SQL, condition_dict)
        results = []
        for row in cursor.fetchall():
            result = dict()
            result.update(row)
            results.append(result)
        return results
        



if __name__ == '__main__':
    model = Model('myrio_roborio_2016_stack_dashboard')
    column_dict = {
            'validated_stack': 'Test Stack',
            'validated_stack_url': 'validated_stack_url TEST',
            'lv_version': 'lv_version TEST',
            'lv_api_version':'lv_api_version TEST',
            'safemode': 'safemode TEST',
            }
    # model.insert(column_dict)
    column_dict2 = {
            'lv_version': 'lv_version TEST2',
            'lv_api_version':'lv_api_version TEST2',
            'safemode': 'safemode TEST',
            }
    condition_dict = {
            'validated_stack': 'Test Stack',
            'validated_stack_url': 'validated_stack_url TEST',
            }
    # model.update(column_dict2, condition_dict)
    # model.delete(condition_dict)
    print model.select(column_dict.keys(), condition_dict)

