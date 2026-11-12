import gridfs

from repositories.shared.mongo_utils import to_object_id


class MediaRepository:
    """Guarda arquivos de mídia no GridFS do MongoDB."""

    def __init__(self, database):
        self._fs = gridfs.GridFS(database)

    def save(self, filename, content_type, data):
        file_id = self._fs.put(
            data, filename=filename, metadata={"content_type": content_type}
        )
        return str(file_id)

    def get(self, file_id):
        oid = to_object_id(file_id)
        if oid is None or not self._fs.exists(oid):
            return None
        grid_out = self._fs.get(oid)
        return {
            "data": grid_out.read(),
            "filename": grid_out.filename,
            "content_type": (grid_out.metadata or {}).get(
                "content_type", "application/octet-stream"
            ),
        }

    def delete(self, file_id):
        oid = to_object_id(file_id)
        if oid is not None:
            self._fs.delete(oid)
