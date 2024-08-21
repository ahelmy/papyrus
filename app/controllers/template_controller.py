from pathlib import Path

from ..services.template_service import render_template
from ..dtos.render_dto import RenderTemplateRequest
from fastapi import (
    APIRouter,
    File,
    UploadFile,
    HTTPException,
)
from fastapi.responses import FileResponse

TEMPLATES_DIR = Path("app/templates")
template_router = APIRouter()


@template_router.post("/upload-template/")
async def upload_template(file: UploadFile = File(...)):
    # Save the uploaded template
    file_path = TEMPLATES_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}


@template_router.post("/render-template/")
async def render_template_endpoint(template: RenderTemplateRequest):
    try:
        rendered_file = render_template(template.template_id, template.data, template.format)
        return FileResponse(rendered_file, media_type='application/octet-stream')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
