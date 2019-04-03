# Android Extract Translated String
Extract translated strings from one android project to another project.

## Usage

1. **set up input folder and output folder in `main.py`**

	```
	INPUT_FOLDER = ""
	OUTPUT_FOLDER = ""
	```

	The directory should be where the `values-xx` folders are. for example
	
	```
	INPUT_FOLDER = "/Users/danielkao/src/androidProjectOriginal/src/main/res/"
	OUTPUT_FOLDER = "/Users/danielkao/src/androidProjectNew/src/main/res/"
	```

	**REMEMBER to add the tailing / in the end of the folder name**
	
2. **call following command line in terminal:**

	`python main.py original_string_key new_string_key[optional]`
	

After running the command, the strings defined in original android project under various `values-xx/stringx.xml` files will be copied to new android project.
