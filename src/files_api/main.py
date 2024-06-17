import json
from datetime import datetime
from typing import Optional

from fastapi import (
    FastAPI,
    Response,
    UploadFile,
)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from files_api.config import BUCKET_NAME
from files_api.s3.read_objects import (
    fetch_s3_object,
    fetch_s3_object_body,
    fetch_s3_objects_metadata,
    fetch_s3_objects_using_page_token,
)
from files_api.s3.write_objects import upload_s3_object

#####################
# --- Constants --- #
#####################

APP = FastAPI()

# CLIENT = boto3.client("s3")

####################################
# --- Request/response schemas --- #
####################################


# read (cRud)
class FileMetadata(BaseModel):
    file_path: str
    last_modified: datetime
    size_bytes: int


# more pydantic models ...
class Status(BaseModel):
    code: int


# def _get_uploaded_fpath(file_path):
#     return DATA_DIR / file_path


##################
# --- Routes --- #
##################


@APP.put("/files/{file_path:path}")
async def upload_file(file_path: str, file: UploadFile, response: Response) -> Response:
    """Upload a file."""

    upload_s3_object(
        bucket_name=BUCKET_NAME,
        file_content=file.file,
        object_key=file_path,
        content_type=file.content_type,
    )

    return Response(content=json.dumps({"filename": file.filename}), status_code=201)


@APP.get("/files")
async def list_files(
    max_keys: Optional[int] = 100, prefix: str = "", continuation_token: Optional[str] = None
) -> Response:
    """List files with pagination."""
    if continuation_token is None:
        objects, continuation_token = fetch_s3_objects_metadata(
            bucket_name=BUCKET_NAME, max_keys=max_keys, prefix=prefix
        )
    else:
        objects, continuation_token = fetch_s3_objects_using_page_token(
            bucket_name=BUCKET_NAME, continuation_token=continuation_token, max_keys=max_keys
        )
    return {"objects": objects, "continuation_token": continuation_token}


@APP.head("/files/{file_path:path}")
async def get_file_metadata(file_path: str, response: Response) -> FileMetadata:
    """Retrieve file metadata.

    Note: by convention, HEAD requests MUST NOT return a body in the response.
    """
    # uploaded_path = _get_uploaded_fpath(file_path)
    obj = fetch_s3_object(bucket_name=BUCKET_NAME, object_key=file_path)

    return FileMetadata(file_path=file_path, last_modified=obj["LastModified"], size_bytes=obj["ContentLength"])


@APP.get("/files/{file_path:path}")
async def get_file(
    file_path: str,
) -> StreamingResponse:
    """Retrieve a file."""
    object = fetch_s3_object_body(bucket_name=BUCKET_NAME, object_key=file_path)

    print(object)
    return object  # StreamingResponse(content=object)


@APP.delete("/files/{file_path:path}")
async def delete_file(
    file_path: str,
    response: Response,
) -> Response:
    """Delete a file.

    NOTE: DELETE requests MUST NOT return a body in the response."""
    return


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(APP, host="0.0.0.0", port=8000)
