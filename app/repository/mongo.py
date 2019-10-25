import os
from pymongo import MongoClient

COLLECTION_NAME = 'kudos'

class MongoRepository(object):
 def __init__ (self):
   mongo_url = os.environ.get('mongodb://kpi_owner:login123@ds263156.mlab.com:63156/mern_kpi')
   self.db = MongoClient(mongo_url).kudos

 def find_all(self, selector):
   return self.db.kudos.find(selector)

 def find(self, selector):
   return self.db.kudos.find_one(selector)

 def create(self, kudo):
   return self.db.kudos.insert_one(kudo)

 def update(self, selector, kudo):
   return self.db.kudos.replace_one(selector, kudo).modified_count

 def delete(self, selector):
   return self.db.kudos.delete_one(selector).deleted_count