import openai
from .apikey.py import key
import psycopg2

def query_chatgpt(api_key,userId, query,maxWords=100,):
    # Set up your OpenAI API key
    openai.api_key = api_key
    sufface=f'  Make sure your response is not more than {maxWords} words long.'
    
    base = buildQuery(userId)
    query=base+query+sufface
    # Call the OpenAI API with your query
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # You can change this to "gpt-3.5-turbo" or another available model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ],
        max_tokens=maxWords*2 # Adjust this to the desired response length
    )
    
    # Extract the response text
    answer = response['choices'][0]['message']['content']
    
    return answer, query


def buildQuery(userId):
    query= "You are a vetinary health/advice assistant. "
    

    # Database connection parameters
    db_config = {
        'dbname': 'mascota',
        'user': 'postgres',
        'password': 'yetheyt8',
        'host': 'localhost',  # or your database host
        'port': '5432'        # default PostgreSQL port
    }

    try:
        # Establish a connection to the database
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Execute the query to select rows where id = 2
        cursor.execute("SELECT breed, species, name, age  FROM pet WHERE customer_id = %s", (userId,))

        
        rows = cursor.fetchall()

        for row in rows:
            # Assuming the table columns are (id, name, age, etc.)
            formatted_row = f"I have a {row[0]} {row[1]} called {row[2]} who is {row[3]} years old. "
            query=query+ formatted_row
            
        

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")
            return query



# Example usage
if __name__ == "__main__":
    api_key = key  # Replace with your API key
    question="how can i get deebo to stop barking?"
    response,query = query_chatgpt(api_key,2, question,100)
    print(query+'\n \n')
    print(response)
    print('bosh')