import sqlite3


def palletise():
    # activate cursor
    conn = sqlite3.connect('planner.db')
    c = conn.cursor()

    # clean temporarly tables
    c.execute("DELETE FROM Lbox")
    c.execute("DELETE FROM Pbox")
    c.execute("DELETE FROM Sbox")

    # count small boxes and pallets with small boxes
    c.execute("SELECT COUNT(*) FROM tempS")
    sb = c.fetchone()
    small_boxes = int(sb[0])

    if small_boxes % 30 == 0:
        small_pallets = int(small_boxes / 30)
    else:
        small_pallets = int(small_boxes / 30) + 1

    # count large boxes and pallets with large boxes
    c.execute("SELECT COUNT(*) FROM tempL")
    lb = c.fetchone()
    large_boxes = int(lb[0])

    if large_boxes % 6 == 0:
        large_pallets = int(large_boxes / 6)
    else:
        large_pallets = int(large_boxes / 6) + 1

    # count pallet boxes
    c.execute("SELECT COUNT(*) FROM tempP")
    pb = c.fetchone()
    pallet_boxes = int(pb[0])

    total_pallets = 1

    # plan all pallets with small boxes
    for pallet in range(total_pallets, small_pallets + 1):
        for y in range(30):
            c.execute("INSERT INTO Sbox(pallet_number) VALUES(?)", (pallet,))
    c.execute("SELECT * FROM tempS")
    temp = c.fetchall()
    for i in range(1, small_boxes + 1):
        pr = str(temp[i - 1][0])
        qty = int(temp[i - 1][1])
        c.execute("UPDATE Sbox SET product=? WHERE row=?", (pr, i))
        c.execute("UPDATE Sbox SET quantity=? WHERE row=?", (qty, i))
    c.execute("DELETE FROM Sbox WHERE product IS null")
    total_pallets = total_pallets + small_pallets - 1

    # plan all pallets with large boxes
    for pallet in range(1, large_pallets + 1):
        for y in range(6):
            palletL = pallet + total_pallets
            c.execute("INSERT INTO Lbox(pallet_number) VALUES(?)", (palletL,))
    c.execute("SELECT * FROM tempL")
    temp = c.fetchall()
    for i in range(1, large_boxes + 1):
        pr = str(temp[i - 1][0])
        qty = int(temp[i - 1][1])
        c.execute("UPDATE Lbox SET product=? WHERE row=?", (pr, i))
        c.execute("UPDATE Lbox SET quantity=? WHERE row=?", (qty, i))
    c.execute("DELETE FROM Lbox WHERE product IS null")
    total_pallets = total_pallets + large_pallets

    # plan pallet boxes
    for pallet in range(1, pallet_boxes + 1):
        palletP = pallet + total_pallets
        c.execute("INSERT INTO Pbox(pallet_number) VALUES(?)", (palletP,))
    c.execute("SELECT * FROM tempP")
    temp = c.fetchall()
    for i in range(1, pallet_boxes + 1):
        pr = str(temp[i - 1][0])
        qty = int(temp[i - 1][1])
        c.execute("UPDATE Pbox SET product=? WHERE row=?", (pr, i))
        c.execute("UPDATE Pbox SET quantity=? WHERE row=?", (qty, i))
    c.execute("DELETE FROM Pbox WHERE product IS null")

    conn.commit()
    conn.close()
