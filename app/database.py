from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://ayush2211207:koLO50CvMTHHJ1Wg@cluster0.d7fkhvy.mongodb.net:27017/immigration?ssl=false&authSource=admin"

client = AsyncIOMotorClient(MONGO_URI)
db = client.immigration