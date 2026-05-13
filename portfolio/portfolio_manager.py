from database.db import conn, cursor

def add_stock(user_id, stock):
    cursor.execute(
        "INSERT INTO portfolio VALUES (?, ?)",
        (user_id, stock)
    )
    conn.commit()

def remove_stock(user_id, stock):
    cursor.execute(
        "DELETE FROM portfolio WHERE user_id=? AND stock=?",
        (user_id, stock)
    )
    conn.commit()

def get_portfolio(user_id):
    cursor.execute(
        "SELECT stock FROM portfolio WHERE user_id=?",
        (user_id,)
    )
    rows = cursor.fetchall()
    return [row[0] for row in rows]
