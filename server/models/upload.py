from storages.backends.gcloud import GoogleCloudStorage
from datetime import datetime

storage = GoogleCloudStorage()

# 이미지 업로드 하는 모델,리뷰, target_path
class Upload:
    @staticmethod
    def upload_image(file, directory):
        try:
            target_path = f"/{directory}/{datetime.timestamp(datetime.now())}.jpg"
            path = storage.save(target_path, file)
            return storage.url(path)
        except Exception as e:
            print(e)
