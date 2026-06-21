import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from Utils.db_connection import get_connection


OUTPUT_FILE = os.path.join(
    os.path.dirname(__file__),
    "DataSchema.txt"
)


def extract_schema():

    conn = get_connection()
    cursor = conn.cursor()

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        print("\nGENERATING DATA SCHEMA...\n")

        cursor.execute("""
            SELECT name
            FROM sys.schemas
            WHERE name NOT IN (
                'dbo',
                'guest',
                'INFORMATION_SCHEMA',
                'sys'
            )
            ORDER BY name
        """)

        schemas = [
            row[0]
            for row in cursor.fetchall()
        ]

        for schema in schemas:

            cursor.execute(f"""
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = '{schema}'
                ORDER BY TABLE_NAME
            """)

            tables = [
                row[0]
                for row in cursor.fetchall()
            ]

            for table in tables:

                f.write("\n")
                f.write("=" * 120)
                f.write("\n")

                f.write(
                    f"System Name : {schema}\n"
                )

                f.write(
                    f"Table Name  : {table}\n"
                )

                f.write(
                    "-" * 120
                )

                f.write("\n")

                try:

                    cursor.execute(f"""
                        SELECT
                            COLUMN_NAME,
                            DATA_TYPE,
                            CHARACTER_MAXIMUM_LENGTH,
                            NUMERIC_PRECISION,
                            NUMERIC_SCALE
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_SCHEMA = '{schema}'
                        AND TABLE_NAME = '{table}'
                        ORDER BY ORDINAL_POSITION
                    """)

                    columns = cursor.fetchall()

                    f.write("\nColumns:\n\n")

                    for col in columns:

                        col_name = col[0]
                        dtype = col[1]
                        char_len = col[2]
                        precision = col[3]
                        scale = col[4]

                        if dtype in (
                            "varchar",
                            "nvarchar",
                            "char",
                            "nchar"
                        ):

                            if char_len == -1:

                                final_type = (
                                    f"{dtype.upper()}(MAX)"
                                )

                            else:

                                final_type = (
                                    f"{dtype.upper()}({char_len})"
                                )

                        elif dtype in (
                            "decimal",
                            "numeric"
                        ):

                            final_type = (
                                f"{dtype.upper()}({precision},{scale})"
                            )

                        else:

                            final_type = dtype.upper()

                        f.write(
                            f"   {col_name:<40} {final_type}\n"
                        )

                    try:

                        cursor.execute(
                            f"SELECT TOP 2 * FROM {schema}.{table}"
                        )

                        rows = cursor.fetchall()

                        col_names = [
                            desc[0]
                            for desc in cursor.description
                        ]

                        f.write(
                            "\nSample Data (Top 2 rows):\n\n"
                        )

                        if rows:

                            for row in rows:

                                row_dict = dict(
                                    zip(
                                        col_names,
                                        row
                                    )
                                )

                                f.write(
                                    f"   {row_dict}\n"
                                )

                        else:

                            f.write(
                                "   No data found\n"
                            )

                    except Exception as e:

                        f.write(
                            f"\nSample Data Error : {str(e)}\n"
                        )

                except Exception as e:

                    f.write(
                        f"\nERROR : {str(e)}\n"
                    )

        print(
            f"\nData schema written to:\n{OUTPUT_FILE}"
        )

    cursor.close()
    conn.close()


if __name__ == "__main__":
    extract_schema()