# 代码生成时间: 2025-08-24 01:56:35
import zipfile
def decompress_file(file_path):    """Decompress a ZIP file to a specified directory.

    Args:
        file_path (str): The path to the ZIP file.

    Returns:
# 增强安全性
        bool: True if decompression is successful, False otherwise.
    """    try:        # Change to the directory where you want to decompress files        import os        os.makedirs('decompressed', exist_ok=True)        with zipfile.ZipFile(file_path, 'r') as zip_ref:            zip_ref.extractall('decompressed')        return True    except zipfile.BadZipFile:        print('The file is not a zip file or it is corrupted.')        return False    except FileNotFoundError:        print('The file does not exist.')        return False    except Exception as e:        print(f'An error occurred: {e}')        return False

# Example usage:
# result = decompress_file('path/to/your/file.zip')
# if result:
#     print('Decompression successful.')
# 增强安全性
# else:
# 增强安全性
#     print('Decompression failed.')