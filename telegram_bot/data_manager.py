import datetime
from io import BytesIO
from typing import Tuple

from minio import Minio

from telegram_bot.config import (ACCESS_KEY, OBJECT_STORAGE_IP,
                                 OBJECT_STORAGE_PORT, SECRET_KEY, USER_ID, PRIVATE)
from telegram_bot.helper import ArgsGetGifsEnum


class MinioStore:
    """
    Initialize client and manage MinIo storage
    """
    def __init__(self, api, port, access_key, secret_key):

        self.client = Minio(
            f"{api}:{port}",
            access_key,
            secret_key,
            secure=False,
        )

    def select_gifs(self, amount: ArgsGetGifsEnum,
                    user_id: int) -> Tuple[int, list]:
        """
        Selects files which fit to condition
        :param amount: condition how many files should be taken
        about all objects in the bucket
        :param user_id: int
        :return: Tuple[int, list]
        """
        all_bucket_objects_metadata = self.client.list_objects(
            "gifs", include_user_meta=True
        )
        condition = {
            ArgsGetGifsEnum.all_gifs: lambda file: self.is_private(file)
            or self.check_user_id(file, user_id),
            ArgsGetGifsEnum.my_gifs: lambda file: self.check_user_id(
                file, user_id
            ),
        }
        retrieved_objects = [
            self.client.get_object("gifs", obj.object_name)
            for obj in all_bucket_objects_metadata
            if condition.get(amount)(obj)
        ]

        return len(retrieved_objects), retrieved_objects

    @staticmethod
    def check_user_id(file, user_id: int) -> bool:
        """
        Checks if file belongs to particular user
        :param file: MinIo file
        :param user_id: int
        :return: bool
        """
        return file.metadata[USER_ID] == str(user_id)

    @staticmethod
    def is_private(file):
        return file.metadata[PRIVATE] == "False"

    def add_gif_to_storage(
        self, bucket: str, file: BytesIO, user_id: int, private: bool
    ) -> None:
        """
        Puts GIF to MinIo storage
        :param bucket: str
        :param file: BytesIO
        :param user_id: int
        :param private: bool
        :return: None
        """
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
        """
        Puts image to MinIo storage
        :param bucket: str
        :param file: BytesIO
        :param user_id: int
        :return: None
        """
        self.check_bucket(bucket)
        file_name = f"{user_id}{datetime.datetime.now()}"
        file_length = file.getbuffer().nbytes
        self.client.put_object(
            bucket, file_name, file,
            file_length, "gif", metadata={"user_id": user_id}
        )

    def check_bucket(self, bucket: str) -> None:
        """
        Checks is there are necessary buckets in MinIo storage and creates them if there are not
        :param bucket: str
        :return: None
        """
        found = self.client.bucket_exists(bucket)
        if not found:
            self.client.make_bucket(bucket)


minio_storage_manager = MinioStore(
    api=OBJECT_STORAGE_IP,
    port=OBJECT_STORAGE_PORT,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
)
