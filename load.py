import pickle

dbfile = open('DB_12345', 'rb')      
db = pickle.load(dbfile) 
for keys in db: 
    print(keys, '=>', db[keys]) 
dbfile.close() 
print(len(db))
# db = {}
# print(len(db))
# f = open('examplePickle3', 'ab')
# aa = {0: 1 , 00: 11, 000:111}
# pickle.dump(aa , f)
# f.close()

# dbfile = open('DB_234', 'rb')      
# db = pickle.load(dbfile) 
# # for keys in db: 
# #     print(keys, '=>', db[keys]) 
# dbfile.close() 
# print(len(db))
