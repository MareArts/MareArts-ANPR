from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import cv2
import numpy as np
from PIL import Image
from importlib.metadata import version, PackageNotFoundError
from marearts_anpr import ma_anpr_detector, ma_anpr_detector_v14, ma_anpr_ocr, marearts_anpr_from_pil
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




app = FastAPI()
security = HTTPBasic()

try:
    marearts_anpr_version = version("marearts_anpr")
except PackageNotFoundError:
    marearts_anpr_version = "Package not found"
except Exception as e:
    marearts_anpr_version = f"Error retrieving version: {str(e)}"

def get_current_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    return credentials


# Security setup
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Global variables for ANPR instances
anpr_d = None
anpr_r = None

# Function to initialize ANPR models
current_detection_version = None
current_ocr_version = None

def get_current_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    return credentials


# Define a Pydantic model for input data
class ANPRInput(BaseModel):
    detection_model_version: str
    ocr_model_version: str

# Dependency for API key validation
async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == "your_secret_api_key":
        return api_key_header
    raise HTTPException(status_code=403, detail="Could not validate credentials")

# Dependency to get current credentials
def get_current_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    return credentials


def initialize_anpr(user_name, serial_key, detection_model_version, ocr_model_version, signature=None, backend="cpu"):
    global anpr_d, anpr_r, current_detection_version, current_ocr_version
    
    # Check if models need to be initialized or reinitialized
    if (anpr_d is None or anpr_r is None or 
        detection_model_version != current_detection_version or 
        ocr_model_version != current_ocr_version):
        
        logger.info(f"Initializing ANPR models")
        logger.info(f"Detection model: {detection_model_version}")
        logger.info(f"OCR model: {ocr_model_version}")
        
        # Check if V14 model and initialize accordingly
        if detection_model_version.startswith("v14_"):
            logger.info(f"V14 model detected, backend: {backend}")
            # V14 models require V2 (Current) license with signature
            if not signature:
                raise HTTPException(status_code=400, detail="V14 models require signature parameter")
            
            # Initialize V14 detector with signature and backend
            anpr_d = ma_anpr_detector_v14(
                detection_model_version, 
                user_name, 
                serial_key, 
                signature, 
                backend=backend
            )
        else:
            # Legacy detector (V13 and earlier)
            anpr_d = ma_anpr_detector(detection_model_version, user_name, serial_key, conf_thres=0.3, iou_thres=0.5)
        
        # OCR is same for all versions
        anpr_r = ma_anpr_ocr(ocr_model_version, user_name, serial_key)
        
        # Update current versions
        current_detection_version = detection_model_version
        current_ocr_version = ocr_model_version
    else:
        logger.info("Using existing ANPR models")

# Endpoint to process an image and perform ANPR
@app.post("/process_image")
async def process_image(
    detection_model_version: str = Form(...),
    ocr_model_version: str = Form(...),
    signature: str = Form(None),  # Optional for V2 keys with V14 models
    backend: str = Form("cpu"),  # Default to CPU for compatibility
    image: UploadFile = File(...),
    api_key: str = Depends(get_api_key),
    credentials: HTTPBasicCredentials = Depends(get_current_credentials)
):
    user_name = credentials.username  
    serial_key = credentials.password  
    
    logger.info(f"Processing request from user: {user_name}")
    logger.info(f"Detection model: {detection_model_version}")
    logger.info(f"OCR model: {ocr_model_version}")
    
    # Log V14-specific parameters if present
    if detection_model_version.startswith("v14_"):
        logger.info(f"V14 signature: {signature[:8]}...{signature[-8:] if signature else 'None'}")
        logger.info(f"V14 backend: {backend}")

    # Initialize ANPR models with signature and backend support
    initialize_anpr(user_name, serial_key, detection_model_version, ocr_model_version, signature, backend)
    
    # Read the uploaded image
    contents = await image.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # Perform ANPR processing
    # Perform ANPR processing
    output = marearts_anpr_from_pil(anpr_d, anpr_r, pil_image)

    # Prepare results
    results = []
    for item in output['results']:  # Ensure we iterate over the correct part of the output
        results.append({
            'ocr': item['ocr'],
            'ocr_conf': int(item['ocr_conf']),  # Assuming the confidence is already a percentage
            'ltrb': item['ltrb'],
            'ltrb_conf': int(item['ltrb_conf'])  # Assuming the confidence is already a percentage
        })

    # Return the formatted result without processing time calculations
    return {
        'results': results,
        'ltrb_proc_sec' : output['ltrb_proc_sec'],
        'ocr_proc_sec' : output['ocr_proc_sec']
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "marearts_anpr_version": marearts_anpr_version
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
