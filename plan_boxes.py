import sqlite3


def plan_boxes():
    # activate cursor
    conn = sqlite3.connect('planner.db')
    c = conn.cursor()

    # clean temporarly tables
    c.execute("DELETE FROM tempS")
    c.execute("DELETE FROM tempL")
    c.execute("DELETE FROM tempP")

    # count nubmer of lines in table sku
    c.execute("SELECT COUNT(*) FROM sku")
    count1 = c.fetchone()
    count = int(count1[0])

    # count number of lines in table load
    c.execute("SELECT COUNT(*) FROM load")
    count2 = c.fetchone()
    countL = int(count2[0])

    # select everything from table sku and alocate values to variables
    c.execute("SELECT * FROM sku")
    temp = c.fetchall()
    for i in range(0, count):
        product = temp[i][0]
        small = temp[i][3]
        large = temp[i][4]
        pallet = temp[i][5]

        # select all products which must be packed only in small boxes
        if large is None and pallet is None:
            small = int(small)

            for j in range(0, countL):
                c.execute("SELECT sku FROM load")
                a = c.fetchall()
                bought = str(a[j][0])
                c.execute("SELECT quantity FROM load")
                b = c.fetchall()
                bought_quantity = int(b[j][0])

                # select only products which are in both tables, sku and load
                if product == bought:
                    # if ordered quantity is smaller or equal to full smal box quantity,
                    # execute below:
                    if bought_quantity <= small:
                        c.execute("INSERT INTO tempS(sku, ordered) VALUES(?, ?)",
                                  (bought, bought_quantity))
                    else:
                        # if ordered quanaity is larger than full small box quantity, split it
                        a = int(bought_quantity / small)
                        rest = bought_quantity - (a * small)
                        for x in range(0, a):
                            # if it is split to full box quantity execute below
                            c.execute("INSERT INTO tempS(sku, ordered) VALUES(?, ?)",
                                      (bought, small))
                        # if there is a rest after splip, add the rest to its own box
                        if rest != 0:
                            c.execute("INSERT INTO tempS(sku, ordered) VALUES(?, ?)",
                                      (bought, rest))

        else:
            # select all products which are left after first option
            small = int(small)
            large = int(large)
            pallet = 0 if pallet == None else int(pallet)

            for j in range(0, countL):
                c.execute("SELECT sku FROM load")
                a = c.fetchall()
                bought = str(a[j][0])
                c.execute("SELECT quantity FROM load")
                b = c.fetchall()
                bought_quantity = int(b[j][0])

                # select only products which are in both tables, sku and load
                if product == bought:
                    if bought_quantity / small < 3:
                        # if ordered quantity is smaller or equal to full smal box quantity,
                        # execute below:
                        if bought_quantity <= small:
                            c.execute("INSERT INTO tempS(sku, ordered) VALUES(?, ?)",
                                      (bought, bought_quantity))
                        else:
                            # if ordered quanaity is larger than full small box quantity, split it
                            a = int(bought_quantity / small)
                            rest = bought_quantity - (a * small)
                            for x in range(0, a):
                                # if it is split to full box quantity execute below
                                c.execute("INSERT INTO tempS(sku, ordered) VALUES(?, ?)",
                                          (bought, small))
                            # if there is a rest after splip, add the rest to its own box
                            if rest != 0:
                                c.execute("INSERT INTO tempS(sku, ordered) VALUES(?, ?)",
                                          (bought, rest))

                    elif bought_quantity / small >= 3 and bought_quantity / large < 6:
                        # if ordered quantity is smaller or equal to full large box quantity,
                        # execute below:
                        if bought_quantity <= large:
                            c.execute("INSERT INTO tempL(sku, ordered) VALUES(?, ?)",
                                      (bought, bought_quantity))
                        else:
                            # if ordered quanaity is larger than full large box quantity, split it
                            a = int(bought_quantity / large)
                            rest = bought_quantity - (a * large)
                            for x in range(0, a):
                                # if it is split to full box quantity execute below
                                c.execute("INSERT INTO tempL(sku, ordered) VALUES(?, ?)",
                                          (bought, large))
                            # if there is a rest after splip, add the rest to its own box
                            if rest != 0:
                                c.execute("INSERT INTO tempL(sku, ordered) VALUES(?, ?)",
                                          (bought, rest))

                    elif bought_quantity / large >= 6:
                        # if ordered quantity is smaller or equal to full pallet box quantity,
                        # execute below:
                        if bought_quantity <= pallet:
                            c.execute("INSERT INTO tempP(sku, ordered) VALUES(?, ?)",
                                      (bought, bought_quantity))
                        else:
                            # if ordered quanaity is larger than full pallet box quantity, split it
                            a = int(bought_quantity / pallet)
                            rest = bought_quantity - (a * pallet)
                            for x in range(0, a):
                                # if it is split to full box quantity execute below
                                c.execute("INSERT INTO tempP(sku, ordered) VALUES(?, ?)",
                                          (bought, pallet))
                            # if there is a rest after splip, add the rest to its own box
                            if rest != 0:
                                c.execute("INSERT INTO tempP(sku, ordered) VALUES(?, ?)",
                                          (bought, rest))

    conn.commit()
    conn.close()
