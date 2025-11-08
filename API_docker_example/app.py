from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import cv2
import numpy as np
from PIL import Image
from importlib.metadata import version, PackageNotFoundError
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr_v14, marearts_anpr_from_pil
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MareArts ANPR Docker API - V14 Models Only
# This API only supports V14 detector and OCR models with V2 license




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
current_region = None

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


def initialize_anpr(user_name, serial_key, detection_model_version, ocr_model_version, region, signature, backend="cpu"):
    global anpr_d, anpr_r, current_detection_version, current_ocr_version, current_region
    
    # V14 models require V2 license with signature
    if not signature:
        raise HTTPException(status_code=400, detail="V14 models require signature parameter")
    
    # Initialize or reinitialize detector only if needed
    if anpr_d is None:
        # First initialization
        logger.info(f"Initializing V14 detector: {detection_model_version} (backend: {backend})")
        anpr_d = ma_anpr_detector_v14(
            detection_model_version, 
            user_name, 
            serial_key, 
            signature, 
            backend=backend
        )
        current_detection_version = detection_model_version
        
    elif detection_model_version != current_detection_version:
        # Different model requested - reinitialize
        logger.info(f"Switching detector from {current_detection_version} to {detection_model_version}")
        anpr_d = ma_anpr_detector_v14(
            detection_model_version, 
            user_name, 
            serial_key, 
            signature, 
            backend=backend
        )
        current_detection_version = detection_model_version
    else:
        # Same detector model - reuse existing
        logger.info(f"Reusing existing detector: {current_detection_version}")
    
    # Initialize or reinitialize OCR only if needed
    if anpr_r is None:
        # First initialization
        logger.info(f"Initializing V14 OCR: {ocr_model_version} (region: {region})")
        anpr_r = ma_anpr_ocr_v14(ocr_model_version, region, user_name, serial_key, signature)
        current_ocr_version = ocr_model_version
        current_region = region
        
    elif ocr_model_version != current_ocr_version:
        # Different OCR model requested - reinitialize
        logger.info(f"Switching OCR from {current_ocr_version} to {ocr_model_version} (region: {region})")
        anpr_r = ma_anpr_ocr_v14(ocr_model_version, region, user_name, serial_key, signature)
        current_ocr_version = ocr_model_version
        current_region = region
        
    elif region != current_region:
        # Same OCR model, different region - use set_region() (>3.7.0)
        logger.info(f"Switching region from {current_region} to {region} (keeping OCR: {current_ocr_version})")
        anpr_r.set_region(region)
        current_region = region
    else:
        # Same OCR model and region - reuse existing
        logger.info(f"Reusing existing OCR: {current_ocr_version} (region: {current_region})")

# Endpoint to process an image and perform ANPR
@app.post("/process_image")
async def process_image(
    detection_model_version: str = Form(...),
    ocr_model_version: str = Form(...),
    region: str = Form("univ"),  # Optional - Default: univ (universal), Options: kr, eup, na, cn, univ
    signature: str = Form(...),  # Required for V14 models
    backend: str = Form("cpu"),  # Default to CPU, options: cpu, cuda, directml
    image: UploadFile = File(...),
    api_key: str = Depends(get_api_key),
    credentials: HTTPBasicCredentials = Depends(get_current_credentials)
):
    user_name = credentials.username  
    serial_key = credentials.password  
    
    logger.info(f"Processing request from user: {user_name}")
    logger.info(f"Detection model: {detection_model_version}")
    logger.info(f"OCR model: {ocr_model_version}")
    logger.info(f"Region: {region}")
    logger.info(f"Backend: {backend}")

    # Initialize V14 ANPR models with signature and backend
    initialize_anpr(user_name, serial_key, detection_model_version, ocr_model_version, region, signature, backend)
    
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
