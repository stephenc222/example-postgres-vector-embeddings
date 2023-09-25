import psycopg2
from embedding_util import generate_embeddings


def run():

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        user="myuser",
        password="mypassword",
        host="localhost",
        port=5555,  # The port you exposed in docker-compose.yml
        database="mydb"
    )

    # Create a cursor to execute SQL commands
    cur = conn.cursor()

    try:
        sentences = [
            "A group of vibrant parrots chatter loudly, sharing stories of their tropical adventures.",
            "The mathematician found solace in numbers, deciphering the hidden patterns of the universe.",
            "The robot, with its intricate circuitry and precise movements, assembles the devices swiftly.",
            "The chef, with a sprinkle of spices and a dash of love, creates culinary masterpieces.",
            "The ancient tree, with its gnarled branches and deep roots, whispers secrets of the past.",
            "The detective, with keen observation and logical reasoning, unravels the intricate web of clues.",
            "The sunset paints the sky with shades of orange, pink, and purple, reflecting on the calm sea.",
            "In the dense forest, the howl of a lone wolf echoes, blending with the symphony of the night.",
            "The dancer, with graceful moves and expressive gestures, tells a story without uttering a word.",
            "In the quantum realm, particles flicker in and out of existence, dancing to the tunes of probability.",

        ]

        # Insert sentences into the items table
        for sentence in sentences:
            embedding = generate_embeddings(sentence)
            cur.execute(
                "INSERT INTO items (content, embedding) VALUES (%s, %s)",
                (sentence, embedding)
            )

        # Example query
        query = "Give me some content about the ocean"
        query_embedding = generate_embeddings(query)

        # Perform a cosine similarity search
        cur.execute(
            """SELECT id, content, 1 - (embedding <=> %s) AS cosine_similarity
               FROM items
               ORDER BY cosine_similarity DESC LIMIT 5""",
            (query_embedding,)
        )

        # Fetch and print the result
        print("Query:", query)
        print("Most similar sentences:")
        for row in cur.fetchall():
            print(
                f"ID: {row[0]}, CONTENT: {row[1]}, Cosine Similarity: {row[2]}")

    except Exception as e:
        print("Error executing query", str(e))
    finally:
        # Close communication with the PostgreSQL database server
        cur.close()
        conn.close()


if __name__ == "__main__":
    run()
