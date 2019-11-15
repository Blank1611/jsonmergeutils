# jsonmergeutils
Merges a series of files containing JSON array of Objects into a single file containing one JSON object.
* **Accepts** 
  * **A Folder Path** to where the JSON files are stored,
  * **Input prefix:** The common prefix all file names share
  
    e.g. test in test1.json, test2.json, test3.json......
    
    The program will read all files in the Folder Path that begin with the Input File
    Base Name, and process them in increasing order of the number added as a
    suffix to each file (1,2,3,....,12,13,...).
   * **Output Prefix:** The program will ensure that the output files are named using the Output File
     Base Name as a prefix, and a counter as a suffix.
     
     e.g for output prefix 'merge' output files will be named as merge1.json, merge2.json, merge3.json.....
    * **Max File Size:** The maximum file size (in bytes) that each merged file should have.
  
* _Can merge json files containing multiple root keys given that they are of type 'array'._ 

* _Since the merged json files are encoded in UTF-8, it can also support any unicode characters._

* _Removes Redundant json objects if any exst within the array._

## **Dependencies:**

* **os module**(builtin)
* **json module**(builtin)

* **jsonmerge module** [[link]](https://pypi.org/project/jsonmerge/)
```bash
pip install jsonmerge
```
* **genson module** [[link]](https://pypi.org/project/genson/)
```bash
pip install genson
```
## **Usage:**
* Download the repository and run the 'jsonmerge_utils.py' file from command line.
```bash
python3 jsonmerge_utils.py
```
![](https://github.com/Blank1611/jsonmergeutils/blob/master/screenshot/1st.PNG)

Or you can load it in an IDE and run it.

* Give the Folder path where the json files are located.
* Input the 'Input Prefix' of the json files to be processed, the 'Output Prefix' the merged file should be named with, 'Max File         Size' (_**in bytes**_) the merged file should not exceed.
![](https://github.com/Blank1611/jsonmergeutils/blob/master/screenshot/2nd.PNG)

![](https://github.com/Blank1611/jsonmergeutils/blob/master/screenshot/3rd.PNG)

- Incase the merged files are to be stored in a separate folder change [line 47](https://github.com/Blank1611/jsonmergeutils/blob/0d0f8488754141d11d9f70d88090d34bea52424c/jsonmerge_utils.py#L47) in [jsonmerge_utils](jsonmerge_utils.py)

from 
```python
merge = Merge(data_dir, output_prefix, max_file_size, merger, root_keys)
```
to
```python
merge = Merge(output_folder(DATADIR), output_prefix, max_file_size, merger, root_keys)
```
The program will create a 'MergedFiles' folder and store all the merged files in it.
