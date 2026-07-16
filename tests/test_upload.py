import pytest

from document_engine.upload.local import LocalUploader
from document_engine.upload.r2 import R2Uploader


class TestUpload:
    def test_local_upload(self, tmp_path):
        uploader = LocalUploader(base_path=str(tmp_path / "uploads"))
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello")
        result = uploader.upload(str(test_file))
        assert (tmp_path / "uploads" / "test.txt").exists()
        assert result["size_bytes"] == 5

    def test_r2_init(self):
        uploader = R2Uploader(
            account_id="test",
            bucket="test-bucket",
            access_key_id="key",
            secret_access_key="secret",
            public_url="https://media.example.com",
        )
        assert uploader.endpoint == "https://test.r2.cloudflarestorage.com/test-bucket"
