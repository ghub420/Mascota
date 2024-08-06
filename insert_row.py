import psycopg2
from psycopg2 import sql

def get_table_columns(conn, table_name):
    """Retrieve column names and types, excluding primary key, from a table."""
    with conn.cursor() as cur:
        query = sql.SQL("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s AND column_name NOT IN (
                SELECT kcu.column_name
                FROM information_schema.table_constraints tco
                JOIN information_schema.key_column_usage kcu 
                    ON kcu.constraint_name = tco.constraint_name
                WHERE tco.constraint_type = 'PRIMARY KEY' AND tco.table_name = %s
            )
        """)
        cur.execute(query, (table_name, table_name))
        columns = cur.fetchall()
    return [col[0] for col in columns]

def insert_row(conn, table_name, columns, values):
    """Insert a row into the specified table with given columns and values."""
    with conn.cursor() as cur:
        query = sql.SQL("""INSERT INTO {table} ({fields}) VALUES ({placeholders})""").format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
            placeholders=sql.SQL(', ').join(sql.Placeholder() * len(values))
        )
        cur.execute(query, values)
    conn.commit()




def insert_tool(table_name,conn):
        
        try:
            
            columns = get_table_columns(conn, table_name)

            if not columns:
                print(f"No columns found for table {table_name} or it only has a primary key.")
                return

            values = []
            for column in columns:
                value = input(f"Enter value for {column}: ")

                if type(value)== str:
                    value=value.lower()
                values.append(value)

            insert_row(conn, table_name, columns, values)
            print("Row inserted successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
        



def main(conn):
    

    while True:
        insert_tool('pet',conn)

    


if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="mascota",
        user="postgres",
        password="yetheyt8",
        host="localhost",
        port="5432"
    )
    
    
    main(conn)

    conn.close()


    print('done')

