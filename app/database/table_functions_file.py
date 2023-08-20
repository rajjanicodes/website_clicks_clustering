from sqlalchemy import CHAR, Column, Float, Integer, MetaData, Table, select, text

from database.instance import *

metadata = MetaData()


class TableFunctions:

    def __init__(self) -> None:
        # --->  CHAR is limited to 14 to match the page_uuid length from the
        #       test.py.
        self.table = Table(
            "click_history",
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("x", Float, nullable=False),
            Column("y", Float, nullable=False),
            Column("page_uuid", CHAR(14), nullable=False),
            Column("cluster_id", Integer, nullable=False),
        )

    def create_table(self):
        """
        Creates a table as per the given representation in the variable table.
        ASSUMPTION: The table does not exist when running the code.
        I tried doing:

            if table_functions.table_exists:
                try:
                    table_functions.drop_from_table()
                except:
                    print("COULD NOT DELETE ROWS FROM THE TABLE.")

        but got stuck into errors as runing ``sudo docker-compose up``
        creates multiple ports, and thus, keeps emptying the table for
        every new port.
        """
        try:
            self.table.create(db_instance._engine)
            print("Table created.")
        except Exception:
            print("THE TABLE ALREADY EXISTS.")

    def print_table(self) -> None:
        """
        Prints the table into the console.
        """
        with safe_session() as session:
            stmt = select(self.table)
            result = session.execute(stmt).fetchall()
            if result:
                print("ID\tX\tY\t\t\tPAGE_UUID\t\t\t\tCLUSTER_ID")
                print("-" * 80)
                for row in result:
                    print(f"{row.id}\t{row.x}\t{row.y}\t{row.page_uuid}\t\t{row.cluster_id}")
            else:
                print("Table is empty")

    def delete_table(self, table_name="click_history") -> None:
        """
        Deletes the table.
        """
        with safe_session() as session:
            session.execute("DROP TABLE IF EXISTS click_history")
            print(f"DELETED THE TABLE: {table_name}")

    def table_exists(self, table_name="click_history") -> bool:
        """
        Checks if table exists or not.
        """
        with safe_session() as session:
            query = f"""SELECT EXISTS (SELECT FROM information_schema.tables
                        WHERE table_name = '{table_name}')"""
            result = session.execute(query)
            result = result.scalar()
            return result

    def fetch(self, column_name: str, table_name="click_history", where=None) -> list:
        """
        Returns a list of the values of the passed column_name from the table.

        Faced an issue of inverted quotes not being a part of the query
        variable at page_uuid = 'example_uuid\1'. Thus, inserting two
        separate clauses, one with a condition (for x and y columns) and
        one without it was a workaround.
        """
        with safe_session() as session:
            if not where:
                query = text(f"SELECT {column_name} FROM {table_name};")
            else:
                query = text(f"""
                    SELECT {column_name} FROM click_history
                    WHERE page_uuid = '{where}';
                    """)
            output = session.execute(query).fetchall()
            return [row[0] for row in output]

    def drop_from_table(self, table_name="click_history") -> None:
        """
        Deletes all entries from the table.
        """
        with safe_session() as session:
            session.execute("DELETE FROM click_history;")
            print(f"DELETED ALL PREVIOUS ENTRIES FROM TABLE: {table_name}")


table_functions = TableFunctions()
