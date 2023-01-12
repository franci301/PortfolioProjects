import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
	#  adding to firebase ez
# db.collection('main').add({'name':'Filippo Gregotti','DOB':'24 January 2005'})