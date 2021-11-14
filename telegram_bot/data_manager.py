import datetime
from io import BytesIO

from minio import Minio

from telegram_bot.config import (ACCESS_KEY, OBJECT_STORAGE_IP,
                                 OBJECT_STORAGE_PORT, SECRET_KEY)
from telegram_bot.helper import ArgsGetGifsEnum

USER_ID = "X-Amz-Meta-User_id"

PRIVATE = "X-Amz-Meta-Private"


class MinioStore:
    def __init__(self, api, port, access_key, secret_key):

        self.client = Minio(
            f"{api}:{port}",
            access_key,
            secret_key,
            secure=False,
        )

    def get_gifs(self, user_id, amount: ArgsGetGifsEnum):
        all_bucket_objects = self.client.list_objects(
            "gifs", include_user_meta=True
        )
        return self.select_gifs(
            amount, all_bucket_objects, user_id
        )

    def select_gifs(self, amount, all_bucket_objects_metadata, user_id):
        condition = {
            ArgsGetGifsEnum.all_gifs: lambda file: self.is_private(file)
            or self.check_user_id(file, user_id),
            ArgsGetGifsEnum.my_gifs: lambda file: self.check_user_id(
                file, user_id
            ),
        }
        retrieved_object = [
            self.client.get_object("gifs", obj.object_name)
            for obj in all_bucket_objects_metadata
            if condition.get(amount)(obj)
        ]

        return len(retrieved_object), retrieved_object

    @staticmethod
    def check_user_id(file, user_id):
        return file.metadata[USER_ID] == str(user_id)

    @staticmethod
    def is_private(file):
        return file.metadata[PRIVATE] == "False"

    def add_gif_to_storage(
        self, bucket: str, file: BytesIO, user_id: int, private
    ) -> None:
        self.check_bucket(bucket)
        file_name = f"{user_id}{datetime.datetime.now()}"
        file_length = file.getbuffer().nbytes
        self.client.put_object(
            bucket,
            file_name,
            file,
            file_length,
            "gif",
            metadata={"user_id": user_id, "private": private},
        )

    def add_image_to_storage(
            self, bucket: str, file: BytesIO,
            user_id: int) -> None:
        self.check_bucket(bucket)
        file_name = f"{user_id}{datetime.datetime.now()}"
        file_length = file.getbuffer().nbytes
        self.client.put_object(
            bucket, file_name, file,
            file_length, "gif", metadata={"user_id": user_id}
        )

    def check_bucket(self, bucket):
        found = self.client.bucket_exists(bucket)
        if not found:
            self.client.make_bucket(bucket)


minio_storage_manager = MinioStore(
    api=OBJECT_STORAGE_IP,
    port=OBJECT_STORAGE_PORT,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
)
