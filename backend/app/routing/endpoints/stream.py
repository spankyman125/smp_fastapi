import os

from typing import List, Optional
from fastapi import APIRouter, Header
from fastapi.responses import StreamingResponse

router = APIRouter()

CONTENT_CHUNK_SIZE = 100*1024

def get_file(name:str):
    f = open("/container/app/static/songs/" + name,'rb')
    return f, os.path.getsize("/container/app/static/songs/" + name)

def chunk_generator(stream, chunk_size, start, size):
    bytes_read = 0
    stream.seek(start)
    while bytes_read < size:
        bytes_to_read = min(chunk_size,size - bytes_read)
        yield stream.read(bytes_to_read)
        bytes_read = bytes_read + bytes_to_read
    stream.close()

@router.get("/static/songs/{name}")
async def stream(name:str, range: Optional[str] = Header(None)):

    asked = range or "bytes=0-"
    stream,total_size = get_file(name)
    start_byte = int(asked.split("=")[-1].split('-')[0])

    return StreamingResponse(
        chunk_generator(
            stream,
            start=start_byte,
            chunk_size=CONTENT_CHUNK_SIZE,
            size=total_size
        )
        ,headers={
            "Accept-Ranges": "bytes",
            "Content-Range": f"bytes {start_byte}-{start_byte+CONTENT_CHUNK_SIZE}/{total_size}",
            "Content-Type": "audio/mpeg"
        },
        status_code=206)