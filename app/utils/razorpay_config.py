import razorpay
import os
from dotenv import load_dotenv

load_dotenv()

# Default fallback values
DEFAULT_RAZORPAY_KEY_ID = "rzp_test_defaultKeyId"
DEFAULT_RAZORPAY_KEY_SECRET = "defaultSecretKey"

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", DEFAULT_RAZORPAY_KEY_ID)
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", DEFAULT_RAZORPAY_KEY_SECRET)

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
