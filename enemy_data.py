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

    # read enemy.json and put the data on a dictionary that will be readily available
    # be readily available in other classes 

    # will be used in enemy.py to create different types of enemies 