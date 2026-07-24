from markitdown import MarkItDown, StreamInfo
from pathlib import Path
from typing import BinaryIO
import io

md = MarkItDown(enable_plugins=False)

def convertToMarkdown(data: BinaryIO, filename: str, content_type: str | None = None,)->str:
    buffer = io.BytesIO(data.read())
   
    stream_info = StreamInfo(
        extension=Path(filename).suffix or None,
        filename=filename,
        mimetype=content_type,
        )
    
    result = md.convert(source=buffer, stream_info=stream_info)
    return result.markdown

