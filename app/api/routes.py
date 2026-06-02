from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import vision_service, llm_service # Import both services

router = APIRouter()

@router.post("/analyze-scene")
async def analyze_scene(image: UploadFile = File(...)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    try:
        # 1. Read the file
        file_bytes = await image.read()
        
        # 2. Perception: Get the bounding boxes and spatial math
        detected_objects = await vision_service.process_image(file_bytes)
        
        # 3. Cognition: Pass image, math, AND file type to Gemini
        natural_description = await llm_service.generate_scene_description(
            file_bytes, 
            detected_objects, 
            image.content_type  # Passes 'image/png' or 'image/jpeg' dynamically
        )
        
        return {
            "status": "success",
            "description": natural_description, # The polished sentence for the user
            "raw_detections": detected_objects  # We keep this just for our own debugging
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")