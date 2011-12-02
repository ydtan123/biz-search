from dbs.dbapi import open_db, Business, Email

def run():
    with open_db("bizsearch") as conn:
        brecords = [ ["biz2", "biz21.com", "4044898763", "AGY", "US", "P", "Jack0"],
                    ["biz3", "biz31.com", "4044898764", "TUR", "US", "P", "Jack2"],
                    ["biz4", "biz41.com", "4044898765", "RLS", "US", "P", "Jack3"],
                    ["biz5", "biz51.com", "4044898766", "EDU", "US", "P", "Jack4"]
                  ]
        Business.insert_one_by_value(conn, "biz1", "biz1.com", "4044898763", "AGY", "US", "P", "Jack")
        Business.insert_a_batch(conn, brecords)
        
        erecords = [ ["a@b", 1, "2011-11-11", 1],
                     ["a@c", 22, "2011-11-11", 1],
                     ["a@d", 23, "2011-11-11", 2],
                     ["a@e", 24, "2011-11-11", 3]
                   ]
        Email.insert_one_by_value(conn, "a@b", 1, "2011-11-11", 0)
        Email.insert_a_batch(conn, erecords)
        
        results = Email.fetch_by(conn, ["*"], address="a@b")
        for r in results:
            print r
    

if __name__=="__main__":
    run()
