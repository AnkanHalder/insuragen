import json
import os
import constants.paths as base_paths

class DocMeta:
    """
    This class provides static methods to manage document metadata stored in a JSON file.
    The metadata is stored as an array of dictionaries, where each dictionary
    represents the metadata for a single document and includes a 'key' field.
    """
    _file_path = os.path.join(base_paths.DOC_META_BASE_PATH, "metadata.json")  # Class-level file path

    @staticmethod
    def _load_all_meta():
        """
        Loads all document metadata from the JSON file.

        Returns:
            list: A list of metadata dictionaries, or an empty list if loading fails or the file doesn't exist.
        """
        os.makedirs(base_paths.DOC_META_BASE_PATH, exist_ok=True)
        try:
            with open(DocMeta._file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {DocMeta._file_path}")
            return []
        except Exception as e:
            print(f"Error loading all metadata: {e}")
            return []

    @staticmethod
    def _save_all_meta(all_meta):
        """
        Saves the array of all document metadata to the JSON file.

        Args:
            all_meta (list): A list of metadata dictionaries.
        """
        try:
            with open(DocMeta._file_path, 'w') as f:
                json.dump(all_meta, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving all metadata: {e}")
            return False

    @staticmethod
    def add_update_meta(key, data):
        """
        Adds or updates a document's metadata.

        Args:
            key (str): The unique key for the document.
            data (dict): The metadata for the document.
        """
        all_metadata = DocMeta._load_all_meta()
        found = False
        for i, meta in enumerate(all_metadata):
            if meta.get('key') == key:
                all_metadata[i] = {'key': key, **data}
                found = True
                break
        if not found:
            all_metadata.append({'key': key, **data})
        DocMeta._save_all_meta(all_metadata)
        print(f"Metadata for key '{key}' added/updated in: {DocMeta._file_path}")

    @staticmethod
    def get_meta(key):
        """
        Retrieves the metadata for a document.

        Args:
            key (str): The unique key for the document.

        Returns:
            dict or None: The metadata dictionary if found, otherwise None.
        """
        all_metadata = DocMeta._load_all_meta()
        for meta in all_metadata:
            if meta.get('key') == key:
                return meta
        print(f"Metadata not found for key '{key}' in: {DocMeta._file_path}")
        return None

    @staticmethod
    def delete_meta(key):
        """
        Deletes the metadata for a document.

        Args:
            key (str): The unique key for the document.

        Returns:
            bool: True if the document was deleted, False otherwise.
        """
        all_metadata = DocMeta._load_all_meta()
        initial_length = len(all_metadata)
        updated_metadata = [meta for meta in all_metadata if meta.get('key') != key]
        if len(updated_metadata) < initial_length:
            DocMeta._save_all_meta(updated_metadata)
            print(f"Metadata for key '{key}' deleted from: {DocMeta._file_path}")
            return True
        else:
            print(f"Metadata not found for key '{key}' in: {DocMeta._file_path}")
            return False
