from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://ayush2211207:koLO50CvMTHHJ1Wg@cluster0.d7fkhvy.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URI)
db = client.immigration
