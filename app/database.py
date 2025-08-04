from motor.motor_asyncio import AsyncIOMotorClient
import ssl

# Option 1: Add SSL parameters to connection string
MONGO_URI = "mongodb+srv://ayush2211207:koLO50CvMTHHJ1Wg@cluster0.d7fkhvy.mongodb.net/immigration?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

client = AsyncIOMotorClient(MONGO_URI)
db = client.immigration

# Option 2: Configure SSL in client options
MONGO_URI_CLEAN = "mongodb+srv://ayush2211207:koLO50CvMTHHJ1Wg@cluster0.d7fkhvy.mongodb.net/immigration"

client = AsyncIOMotorClient(
    MONGO_URI_CLEAN,
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
    tlsAllowInvalidCertificates=True
)
db = client.immigration

# Option 3: Most robust configuration
client = AsyncIOMotorClient(
    MONGO_URI_CLEAN,
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    socketTimeoutMS=10000
)
db = client.immigration

# Test connection
async def test_connection():
    try:
        # Test the connection
        await client.admin.command('ping')
        print("MongoDB connection successful!")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False