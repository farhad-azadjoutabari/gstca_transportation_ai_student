# Initial Setup

## Step 1: Sign in to Google
Open a browser and sign in to a Google account.

You must use the same Google account for:

- Google Drive
- The shared dataset folder
- Google Colab

## Step 2: Add the dataset folder to My Drive
Open the Google Drive link provided by the instructor.

Then:
1. Open the shared ```data``` folder.
2. Click the folder name or right-click the folder.
3. Select **Organize** or **Add shortcut to Drive**.
4. Choose **My Drive**.
5. Confirm the shortcut.

The folder should now be accessible through:
```My Drive/data/```

## Step 3: Open the assigned notebook in Google Colab
You may open the notebook from the GitHub repository.

One method is:

1. Open Google Colab.
2. Select **File** → **Open notebook**.
3. Select the **GitHub** tab.
4. Paste the GitHub repository URL.
5. Select the assigned challenge notebook.

Opening a notebook from GitHub loads the notebook itself, but it does not necessarily place all repository helper files in the Colab runtime. Therefore, students must still run the repository setup cell.

## Step 4: Save the notebook imediately
When you open your notebook from GitHub, the first thing you should do is:

***File** -> **Save a copy in Drive**

You should rename it using a consistent format:

```Team_1_Challenge_1_Working_Notebook.ipynb```

The saved notebook will normally appear in:

```My Drive/Colab Notebooks/```

# Colab Setup Cells
Place the following cells near the beginning of every challenge notebook.

## Cell 1: Clone the GitHub repository
Replace the example URL and repository folder name with the actual values.

```python
import os

REPOSITORY_URL = "https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git"
REPOSITORY_PATH = "/content/YOUR_REPOSITORY"

if not os.path.exists(REPOSITORY_PATH):
    !git clone {REPOSITORY_URL} {REPOSITORY_PATH}
    print("Repository cloned successfully.")
else:
    print("Repository already exists in this Colab session.")
```
## Cell 2: Set the repository as the working directory
This allows Python to locate folders such as ```helpers```

```python
import os 
import sys 
os.chdir(REPOSITORY_PATH) 
if REPOSITORY_PATH not in sys.path: 
    sys.path.insert(0, REPOSITORY_PATH) 
print("Current working directory:") 
print(os.getcwd())
```

## Cell 3: Verify the repository files
```!find {REPOSITORY_PATH} -maxdepth 2 -type f | sort | head -100```

You should be able to see the files.

## Cell 4: Import help functions
Example:
```python
from helpers.data_loading import load_dataset 
from helpers.preprocessing import clean_columns 
from helpers.visualization import plot_distribution 

print("Helper functions imported successfully.")
```

If Python still cannot find the helper module, verify:

```python
import os

print(os.getcwd())
print(os.listdir(REPOSITORY_PATH)) 
print(os.listdir(f"{REPOSITORY_PATH}/helpers"))
```

## Cell 5: Install required packages

```!pip install -q -r requirements.txt```

## Cell 6: Mount Google Drive
```python
from google.colab import drive

drive.mount("/content/drive")
```
Colab will display an authorization process. You must authorize access using the same Google account that has access to the shared data folder.

After successful mounting, My Drive is normally available at:
```/content/drive/MyDrive/```

## Cell 7: Define the data path
```python
from pathlib import Path 

DATA_ROOT = Path("/content/drive/MyDrive/data") 
DATA_PATH = DATA_ROOT / "required dataset folder" 

print("Data folder:", DATA_PATH) 
print("Folder exists:", DATA_PATH.exists())
```

## Cell 8: Verify Access to the data
```python
if not DATA_PATH.exists(): 
    raise FileNotFoundError( 
        f"Data folder was not found: {DATA_PATH}\n" 
        "Confirm that you added the shared data folder " 
        "as a shortcut inside My Drive." ) 

files = sorted(DATA_PATH.rglob("*")) 
print(f"Found {len(files)} items:\n") 

for file in files[:50]: 
    print(file)
```

## Cell 9: Load a dataset
```python
file_path = DATA_PATH / "dataset_name.csv" 
df = pd.read_csv(file_path) 
print("Dataset shape:", df.shape) 
df.head()
```
