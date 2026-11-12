import os
from dataclasses import dataclass

from core.errors import NotFound, ValidationFailed

MAX_FILES = 4
MAX_FILE_BYTES = 10 * 1024 * 1024

# tipo MIME -> verificação da "assinatura" real do arquivo
_SIGNATURES = {
    "image/png": lambda d: d.startswith(b"\x89PNG\r\n\x1a\n"),
    "image/jpeg": lambda d: d.startswith(b"\xff\xd8\xff"),
    "image/gif": lambda d: d.startswith((b"GIF87a", b"GIF89a")),
    "image/webp": lambda d: d[:4] == b"RIFF" and d[8:12] == b"WEBP",
    "video/mp4": lambda d: d[4:8] == b"ftyp",
    "video/webm": lambda d: d.startswith(b"\x1a\x45\xdf\xa3"),
    "application/pdf": lambda d: d.startswith(b"%PDF"),
}
ALLOWED_TYPES = tuple(_SIGNATURES)


@dataclass(frozen=True)
class MediaFile:
    filename: str
    content_type: str
    data: bytes


class MediaService:
    def __init__(self, media_repository):
        self._repo = media_repository

    def validate(self, files, already_attached=0):
        files = list(files)
        if already_attached + len(files) > MAX_FILES:
            raise ValidationFailed(f"Cada publicação aceita no máximo {MAX_FILES} arquivos.")
        for f in files:
            name = os.path.basename(f.filename) or "arquivo"
            if f.content_type not in _SIGNATURES:
                raise ValidationFailed(
                    f"'{name}': tipo não permitido. Use imagem (PNG, JPG, GIF, WEBP), vídeo (MP4, WEBM) ou PDF."
                )
            if len(f.data) > MAX_FILE_BYTES:
                raise ValidationFailed(f"'{name}' excede {MAX_FILE_BYTES // (1024 * 1024)} MB.")
            if not _SIGNATURES[f.content_type](f.data):
                raise ValidationFailed(f"'{name}' não corresponde ao tipo informado.")

    def store_many(self, files, already_attached=0):
        files = list(files)
        self.validate(files, already_attached)
        saved = []
        try:
            for f in files:
                name = (os.path.basename(f.filename) or "arquivo")[:120]
                file_id = self._repo.save(name, f.content_type, f.data)
                saved.append(
                    {"id": file_id, "filename": name, "content_type": f.content_type, "size": len(f.data)}
                )
        except Exception:
            self.delete_many([m["id"] for m in saved])
            raise
        return saved

    def get(self, file_id):
        media = self._repo.get(file_id)
        if media is None:
            raise NotFound("Arquivo não encontrado.")
        return media

    def delete_many(self, file_ids):
        for file_id in file_ids:
            self._repo.delete(file_id)
