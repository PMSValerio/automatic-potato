import json

class EnemyData():
    __instance = None

    def get(): 
        if not EnemyData.__instance:
            EnemyData()
        return EnemyData.__instance

    def __init__(self):
        if EnemyData.__instance:
            raise Exception("EnemyData singleton class already initialised")
        else:
            EnemyData.__instance = self
            self.load_data()
        
    # read enemy.json and put the data on a dictionary that will be readily available
    # be readily available in other classes 

    # will be used in enemy.py to create different types of enemies 

    # load data and parse the keys to int so they coincide with the EnemyType enum of enemies
    # parse values as ints as well, if that's the case
    def load_data(self): 
        self.data = {}
        with open("./json/enemy.json") as f:         
            self.data = json.load(f, object_pairs_hook=lambda pairs: {int(k) if k.isdigit() else k: v for k, v in pairs}, parse_int=int)

    def get_data(self):
        return self.data
