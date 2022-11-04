import io
from pickle import TRUE
import random
from datetime import datetime, timedelta
from types import GetSetDescriptorType
from typing import List
from app.services.minio.schemas.CopySchema import CopySchema
from app.services.minio.schemas.GetListChildren import GetListChildrenSchema
from .schemas.OptionEnum import OptionEnum
from config import get_config
from minio import Minio
from minio.commonconfig import REPLACE, CopySource


class MinioService:
    # __instance = None

    # @staticmethod
    # def get_instance():
    #     if not MinioService.__instance:
    #         MinioService.__instance = MinioService()
    #     return MinioService.__instance

    def __init__(self):
        self.minio_url = get_config("MINIO_URL")
        self.access_key = get_config("MINIO_ACCESS_KEY")
        self.secret_key = get_config("MINIO_SECRET_KEY")
        self.bucket_name = get_config("MINIO_BUCKET_NAME")
        self.client = Minio(
            self.minio_url,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=True,
        )
        self.make_bucket()

    def make_bucket(self) -> str:
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
        return self.bucket_name

    def presigned_get_object(self, bucket_name, object_name):
        # Request URL expired after 7 days
        url = self.client.presigned_get_object(
            bucket_name=bucket_name,
            object_name=object_name,
            expires=timedelta(days=7)
        )
        return url

    def check_file_name_exists(self, bucket_name, file_name):
        try:
            self.client.stat_object(
                bucket_name=bucket_name, object_name=file_name)
            return True
        except Exception as e:
            print(f'[x] Exception: {e}')
            return False

    def create_folder(self, folder_path):
        try:
            objects = self.client.list_objects(
                self.bucket_name, prefix=folder_path, recursive=False)

            list = [obj for obj in objects]

            if len(list) != 0:
                return False

            result = self.client.put_object(
                bucket_name=get_config("MINIO_BUCKET_NAME"), object_name=folder_path, data=io.BytesIO(b"hello"), length=5)

        except Exception as e:
            if e.__dict__["_code"] != 'XMinioObjectExistsAsDirectory':
                return False

        return True

    # region List all sub directories.
    def list_all_sub_directories(self, params: GetListChildrenSchema):
        selectedPath = params.selectedPath
        page_size = params.page_size
        page_index = params.page_index
        type = params.type

        objects = []
        if selectedPath:
            objects = self.client.list_objects(
                self.bucket_name, prefix=selectedPath, recursive=False)
        else:
            objects = self.client.list_objects(
                self.bucket_name, recursive=False)

        response = {}

        if type == OptionEnum.FOLDER:
            list = []
            # Get only folder from objects array retrieved above
            folder_list = [obj for obj in objects if obj.__dict__[
                "_object_name"][-1:] == "/"]

            for folder in folder_list:
                folder_name = folder.__dict__["_object_name"]
                children_objects = objects = self.client.list_objects(
                    self.bucket_name, prefix=folder_name, recursive=True)
                children_files = [obj for obj in children_objects if obj.__dict__[
                    "_object_name"][-1:] != "/"]

                list.append({"folder_name": folder_name,
                            "children": len(children_files)})
            response = {"totalChildren": len(list), "children": list}
            return response

        else:
            # Get only file from objects array retrieved above
            children_files = [obj for obj in objects if obj.__dict__[
                "_object_name"][-1:] != "/"]

            start = page_size * page_index
            end = start + page_size
            children = []

            paginated_list = children_files[start:end]
            for obj in paginated_list:
                obj_dict = obj.__dict__
                obj_name = obj_dict["_object_name"]
                child = {"object_name": obj_dict["_object_name"],
                         "last_modified": obj_dict["_last_modified"],
                         "size": obj_dict["_size"]}

                objectURL = self.client.get_presigned_url(
                    "GET", object_name=obj_name,
                    expires=timedelta(days=1),
                    bucket_name=get_config("MINIO_BUCKET_NAME"))
                child["url"] = objectURL

                children.append(child)

            response = {"totalChildren": len(
                children_files), "children": children}

        return response
    # endregion

    def move_object(self,  sourceObject, destinationObject):
        bucket = get_config("MINIO_BUCKET_NAME")
        # Check destination object exist in source object
        check_objects = self.client.list_objects(
            bucket_name=bucket, prefix=destinationObject, recursive=False)
        obj_list = [obj for obj in check_objects]

        # If it does exist then append _1 to file name
        if len(obj_list) != 0:
            file_name = destinationObject.split("/")[-1]
            newFilename = file_name.split(".")[0] + "_1"
            extension = file_name.split(".")[1]
            destinationObject = destinationObject.replace(
                file_name, newFilename + "." + extension)

        result = self.client.copy_object(
            bucket,
            destinationObject,
            CopySource(bucket, sourceObject),
            metadata_directive=REPLACE,
        )
        self.client.remove_object(bucket, sourceObject)
        result_dict = result.__dict__
        objects = self.client.list_objects(
            bucket_name=bucket, prefix=result_dict["_object_name"])

        response = {}
        for obj in objects:
            obj_dict = obj.__dict__
            response = {"object_name": obj_dict["_object_name"],
                        "last_modified": obj_dict["_last_modified"],
                        "size": obj_dict["_size"]}
            break
        return response

    # region Move objects to another destination
    def move_objects(self, body: List[CopySchema]):
        responses = []
        for obj in body:
            responses.append(self.move_object(
                obj.sourcePath, obj.destinationPath))

        file_path = body[0].sourcePath
        parent_folder = "/".join(file_path.split('/')[:-1]) + "/"

        children = self.client.list_objects(
            self.bucket_name, prefix=parent_folder, recursive=False)
        children_list = [obj for obj in children]

        # if parent folder is removed, recreate it
        if len(children_list) == 0:
            self.create_folder(parent_folder)
        return responses
    # endregion

    # region Move folder to another destination
    def move_folder(self, srcPath, dstPath):
        bucket = get_config("MINIO_BUCKET_NAME")

        # Check folder name of srcPath whether exist in dstPath
        folder_name = srcPath.split('/')[-2]
        newSrcPath = dstPath + folder_name

        objects = self.client.list_objects(
            bucket_name=bucket, prefix=newSrcPath, recursive=False)
        obj_list = [obj for obj in objects]

        # If exist then append suffix to it
        if len(obj_list) != 0:
            folder_name += "_1"
            newSrcPath += "_1"
        newSrcPath += "/"

        children_objects = self.client.list_objects(
            bucket_name=bucket, prefix=srcPath, recursive=True)
        children_files = [obj for obj in children_objects]

        # If src folder is empty
        if len(children_files) == 0:
            print("Create folder: " + newSrcPath)
            self.create_folder(newSrcPath)
            self.remove_folder(srcPath)

        else:
            for obj in children_files:
                obj_dict = obj.__dict__
                obj_name = obj_dict["_object_name"]
                discard_src_path = obj_name.replace(srcPath, folder_name + "/")
                destinationObject = dstPath + discard_src_path
                self.move_object(obj_name, destinationObject)

            parent_folder = "/".join(srcPath.split('/')[:-2]) + "/"
            children = self.client.list_objects(
                self.bucket_name, prefix=parent_folder, recursive=False)
            children_list = [obj for obj in children]

            # if parent folder is removed, recreate it
            if len(children_list) == 0:
                self.create_folder(parent_folder)

        return {"message": "Move folder successfully"}
    # endregion

    # region Delete folder
    def remove_folder(self,  folder_path):
        bucket = get_config("MINIO_BUCKET_NAME")
        objects = self.client.list_objects(
            self.bucket_name, prefix=folder_path, recursive=True)

        obj_list = [obj for obj in objects]

        if len(obj_list) == 0:
            self.client.put_object(
                bucket_name=bucket, object_name=folder_path + "removing", data=io.BytesIO(b"hello"), length=5)
            self.client.remove_object(bucket, folder_path + "removing")

        else:
            for obj in obj_list:
                self.client.remove_object(bucket, obj.object_name)
            parent_folder = "/".join(folder_path.split('/')[:-2]) + "/"
            children = self.client.list_objects(
                self.bucket_name, prefix=parent_folder, recursive=False)
            children_list = [obj for obj in children]

            # if parent folder is removed, recreate it
            if len(children_list) == 0:
                self.create_folder(parent_folder)

        return True
    # endregion

    # region Delete file
    def remove_file(self, file_path):
        bucket = get_config("MINIO_BUCKET_NAME")
        self.client.remove_object(bucket, file_path)

        parent_folder = "/".join(file_path.split('/')[:-1]) + "/"

        children = self.client.list_objects(
            self.bucket_name, prefix=parent_folder, recursive=False)
        children_list = [obj for obj in children]

        # if parent folder is removed, recreate it
        if len(children_list) == 0:
            self.create_folder(parent_folder)
        return True
    # endregion

    # region get statistic
    def get_statistics(self, warehouse: str):
        objects = self.client.list_objects(
            self.bucket_name, prefix=warehouse, recursive=False)

        objects = [obj for obj in objects if obj.__dict__[
            "_object_name"][-1:] == "/"]

        statistics = []
        for obj in objects:
            obj_dict = obj.__dict__
            obj_name = obj_dict["_object_name"].split('/')[1]
            size = 0
            sub_objects = self.client.list_objects(
                self.bucket_name, prefix=obj_dict["_object_name"], recursive=True)
            for sub_obj in sub_objects:
                size += sub_obj.__dict__["_size"]
            statistics.append({"folder_name": obj_name, "size": size})

        return statistics
    # endregion

    # region create object
    def create_object(self, file, folder):
        bucket = get_config("MINIO_BUCKET_NAME")
        object_name = folder + file.filename

        data = file.file.read()
        byte_data = io.BytesIO(data)

        result = self.client.put_object(
            bucket_name=bucket, object_name=object_name, data=byte_data,
            content_type=file.content_type, length=len(data))

        obj_dict = result.__dict__
        response = {"object_name": obj_dict["_object_name"], "size": len(data)}
        return response
    # endregion
