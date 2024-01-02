###  libraries

import re
import csv
import pandas as pd

##################################################

def analyze_sql_query(sql_query):
    # Counting Comment Characters
    comment_chars_count = sql_query.count('--') + sql_query.count('/*')

    # Counting Semicolons
    semicolons_count = sql_query.count(';')

    # Counting Logical Operators
    logical_operators_count = sum(1 for op in ['AND', 'OR', 'NOT'] if f' {op} ' in sql_query.upper())

    # Counting True Conditions
    true_conditions_count = sum(1 for true_cond in ['TRUE', '1=1', '1=1--'] if true_cond in sql_query.upper())

    # Counting Keywords
    keywords_count = sum(1 for keyword in [ 'ADD', 'ALL', 'ALTER', 'ANY', 'AS', 'ASC', 'AUTHORIZATION', 'BACKUP', 'BEGIN', 'BETWEEN', 'BREAK', 'BROWSE',
    'BULK', 'BY', 'CASCADE', 'CASE', 'CHECK', 'CLOSE', 'COALESCE', 'COLLATE', 'COLUMN', 'COMMIT', 'COMPUTE',
    'CONTAINS', 'CONTAINSTABLE', 'CONTINUE', 'CONVERT', 'CREATE', 'CROSS', 'CURRENT', 'CURRENT_DATE', 'CURRENT_TIME',
    'CURRENT_TIMESTAMP', 'CURRENT_USER', 'CURSOR', 'DATABASE', 'DBCC', 'DEALLOCATE', 'DECLARE', 'DEFAULT', 'DELETE',
    'DENY', 'DESC', 'DISK', 'DISTINCT', 'DOUBLE', 'DROP', 'DUMP', 'END', 'ERRLVL', 'EXCEPT', 'EXEC', 'EXECUTE',
    'EXISTS', 'EXIT', 'FETCH', 'FOR', 'FOREIGN', 'FREETEXT', 'FREETEXTTABLE', 'FROM', 'FULL', 'GOTO', 'GRANT', 'GROUP',
    'HAVING', 'HOLDLOCK', 'IDENTITY', 'IDENTITY_INSERT', 'IDENTITYCOL', 'INDEX', 'INNER', 'INSERT', 'INTERSECT', 'INTO',
    'JOIN', 'KILL', 'LEFT', 'LIKE', 'LINENO', 'LOAD', 'NOCHECK', 'OFFSETS', 'OPEN', 'OPENDATASOURCE', 'OPENQUERY',
    'OPENROWSET', 'OPENXML', 'OPTION', 'ORDER', 'OUTER', 'OVER', 'PERCENT', 'PRIMARY', 'PRINT', 'PROCEDURE', 'PUBLIC',
    'RAISEERROR', 'READ', 'READTEXT', 'RECONFIGURE', 'REFERENCES', 'REPLICATION', 'RESTORE', 'RESTRICT', 'RETURN',
    'REVOKE', 'RIGHT', 'ROLLBACK', 'ROWCOUNT', 'ROWGUIDCOL', 'RULE', 'SAVE', 'SCHEMA', 'SELECT', 'SESSION_USER', 'SET',
    'SETUSER', 'SHUTDOWN', 'SOME', 'SYSTEM_USER', 'SYS', 'TABLE', 'TEXTSIZE', 'TOP', 'TRAN', 'TRANSACTION', 'TRIGGER',
    'TRUNCATE', 'TSEQUAL', 'UNION', 'UNIQUE', 'UPDATE', 'UPDATETEXT', 'USE', 'USER', 'VALUES', 'VARYING', 'VIEW',
    'myappadmin', 'sp_', 'utl_', 'xp_', 'WAITFOR', 'WHERE', 'WITH', 'WRITETEXT', 'ADMIN', 'CONNECT'] if f' {keyword} ' in sql_query.upper())

    # Counting Wildcard Characters
    wild_char_count = sql_query.count('%') + sql_query.count('_')

    return comment_chars_count, semicolons_count, logical_operators_count, true_conditions_count, keywords_count, wild_char_count

def save_to_csv(result, filename='sql_analysis.csv'):
    fields = ['Comment Characters', 'Semicolons', 'Logical Operators', 'True Conditions', 'Keywords', 'Wild Characters']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerow({fields[i]: result[i] for i in range(len(fields))})

def analyze_sql_queries_from_excel(excel_file, output_csv='sql_analysis.csv'):
    # Read SQL queries from Excel file
    df = pd.read_excel(excel_file)
    
    # Analyze each SQL query and save the results
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        for index, row in df.iterrows():
            sql_query = str(row['SQL Query'])  # Modify column name based on your Excel structure
            analysis_result = analyze_sql_query(sql_query)
            writer.writerow({fields[i]: analysis_result[i] for i in range(len(fields))})

##################################################

def query_parser(input_query: str, inputType: int=1):
    # Define fields
    fields = ['Comment Characters', 'Semicolons', 'Logical Operators', 'True Conditions', 'Keywords', 'Wild Characters']

    # passing single query as string
    if inputType == 1:
        got_query = input_query
        got_parsed_query = analyze_sql_query(got_query)
        return got_parsed_query
    else:
    # Example Excel file containing SQL queries
        try:
            excel_file_path = input_query
            # Analyze SQL queries from Excel and save the results to CSV
            analyze_sql_queries_from_excel(excel_file_path)
            print("Saved parsed data into 'sql_analysis.csv'!")
            return True
        except:
            print("Something went wrong!!")
            return False