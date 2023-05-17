from neo4j import GraphDatabase


class App:

    def __init__(self):
        return

    def create_author(self, name, age):
        cypher_query = "CREATE (a:Author {name: $name, age: $age }) RETURN a"

        def execute_create_author(tx):
            tx.run(cypher_query, name=name, age=age)

        with driver.session() as session:
            session.execute_write(execute_create_author)
            print("Author created with success")

    def create_book(self, title, publication_year):
        cypher_query = "CREATE (b:Book {title: $title, publication_year: $publication_year}) RETURN b"

        def execute_create_book(tx):
            tx.run(cypher_query, title=title, publication_year=publication_year)

        with driver.session() as session:
            session.execute_write(execute_create_book)
            print("Book created with success")

    def create_relationship(self, author_name, book_title):
        cypher_query = ("MATCH (a:Author {name: $author_name}) MATCH (b:Book {title: $book_title}) "
                        "CREATE (a)-[:WROTE]->(b)")

        def execute_create_relationship(tx):
            tx.run(cypher_query, author_name=author_name, book_title=book_title)

        with driver.session() as session:
            session.execute_write(execute_create_relationship)
            print("Relationship created with success")

    def find_author_by_name(self, name):
        cypher_query = "MATCH (a) WHERE a.name = $name RETURN a"

        with driver.session() as session:
            result = session.run(cypher_query, name=name)
            record = result.single()
            if record:
                return record["a"]
            else:
                return None


    def find_book_by_author(self, name):
        cypher_query = "MATCH (a:Author)-[:WROTE]-(b:Book) WHERE a.name = $name RETURN b"

        with driver.session() as session:
            result = session.run(cypher_query, name=name)
            book = []
            for record in result:
                book.append(record)
            if len(book) > 0:
                return book
            else:
                return None

    def find_author_by_book(self, title):
        cypher_query = "MATCH (a:Author)-[:WROTE]-(b:Book) WHERE b.title = $title RETURN a"

        with driver.session() as session:
            result = session.run(cypher_query, title=title)
            author = []
            for record in result:
                author.append(record)
            if len(author) > 0:
                return author
            else:
                return None


if __name__ == "__main__":
    uri = "neo4j+s://4a528dde.databases.neo4j.io"
    user = "neo4j"
    password = "tNnoY5jpA94DuM_-_Md0ennLwkjOemwD0AbZUII_Xo4"
    driver = GraphDatabase.driver(uri, auth=(user, password))
    app = App()
    app.create_author("J. K. Rowling", "57")
    app.create_author("Suzanne Collins", "60")
    app.create_book("Harry Potter and the Philosopher's Stone", "1997")
    app.create_book("Harry Potter and the Chamber of Secrets", "1998")
    app.create_book("The Hunger Games", "2008")
    app.create_book("Catching Fire", "2009")
    app.create_relationship("J. K. Rowling", "Harry Potter and the Philosopher's Stone")
    app.create_relationship("J. K. Rowling", "Harry Potter and the Chamber of Secrets")
    app.create_relationship("Suzanne Collins", "The Hunger Games")
    app.create_relationship("Suzanne Collins", "Catching Fire")
    print(app.find_author_by_name("J. K. Rowling"))
    print(app.find_book_by_author("Suzanne Collins"))
    print(app.find_author_by_book("Harry Potter and the Chamber of Secrets"))
    driver.close()
