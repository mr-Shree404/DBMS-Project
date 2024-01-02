import pandas as pd
import csv

# List of keywords to check for
keywords_to_check = [
    'ADD', 'ALL', 'ALTER', 'ANY', 'AS', 'ASC', 'AUTHORIZATION', 'BACKUP', 'BEGIN', 'BETWEEN', 'BREAK', 'BROWSE',
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
    'myappadmin', 'sp_', 'utl_', 'xp_', 'WAITFOR', 'WHERE', 'WITH', 'WRITETEXT', 'ADMIN', 'CONNECT'
]

# List of common wild characters
wild_characters = ['%', '_', '[', ']']

def analyze_sql_query(sql_query):
    # Initialize counters
    comment_count = 0
    semicolon_count = 0
    logical_operator_count = 0
    true_condition_count = 0
    keyword_count = {keyword: 0 for keyword in keywords_to_check}
    wild_char_count = {char: 0 for char in wild_characters}

    # Split the query into words
    words = sql_query.split()

    for word in words:
        # Count comments
        if '--' in word:
            comment_count += 1

        # Count semicolons
        semicolon_count += word.count(';')

        # Count logical operators
        logical_operators = ['AND', 'OR', 'NOT']
        if word.upper() in logical_operators:
            logical_operator_count += 1

        # Count true conditions
        true_conditions = ['TRUE', '1=1', '1=1--']
        if word.upper() in true_conditions:
            true_condition_count += 1

        # Count keywords
        if word.upper() in keywords_to_check:
            keyword_count[word.upper()] += 1

        # Count wildcard characters
        for char in wild_characters:
            wild_char_count[char] += word.count(char)

    return comment_count, semicolon_count, logical_operator_count, true_condition_count, keyword_count, wild_char_count

def process_excel_and_save_results(excel_path, output_csv_path):
    # Read SQL queries from Excel sheet
    df = pd.read_excel(excel_path)

    # Initialize result lists
    results = []

    # Analyze each SQL query
    for index, row in df.iterrows():
        sql_query = str(row['SQL_Query'])
        result = analyze_sql_query(sql_query)
        results.append(result)

    # Write the results to a CSV file
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Comment Characters', 'Number of semicolons', 'Logical Operator', 'True conditions'] + keywords_to_check + wild_characters
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow({
                'Comment Characters': result[0],
                'Number of semicolons': result[1],
                'Logical Operator': result[2],
                'True conditions': result[3],
                **result[4],  # Keywords
                **result[5]   # Wild characters
            })

if __name__ == "__main__":
    excel_path = 'SQLiV3.xlsx'  # Replace with the actual path to your Excel file
    output_csv_path = 'sql_analysis_result.csv'  # Replace with the desired output CSV file path
    process_excel_and_save_results(excel_path, output_csv_path)
