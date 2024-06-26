{
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "name": "python",
      "version": "3.10.13",
      "mimetype": "text/x-python",
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "pygments_lexer": "ipython3",
      "nbconvert_exporter": "python",
      "file_extension": ".py"
    },
    "kaggle": {
      "accelerator": "none",
      "dataSources": [
        {
          "sourceId": 10211,
          "databundleVersionId": 111096,
          "sourceType": "competition"
        },
        {
          "sourceId": 15520,
          "sourceType": "datasetVersion",
          "datasetId": 11167
        },
        {
          "sourceId": 38454,
          "sourceType": "datasetVersion",
          "datasetId": 2709
        }
      ],
      "isInternetEnabled": false,
      "language": "python",
      "sourceType": "notebook",
      "isGpuEnabled": false
    },
    "colab": {
      "name": "Exercise: Underfitting and Overfitting",
      "provenance": [],
      "include_colab_link": true
    }
  },
  "nbformat_minor": 0,
  "nbformat": 4,
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/tamyabradley/IST679/blob/main/Exercise_Underfitting_and_Overfitting.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "source": [
        "\n",
        "# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES\n",
        "# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,\n",
        "# THEN FEEL FREE TO DELETE THIS CELL.\n",
        "# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON\n",
        "# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR\n",
        "# NOTEBOOK.\n",
        "\n",
        "import os\n",
        "import sys\n",
        "from tempfile import NamedTemporaryFile\n",
        "from urllib.request import urlopen\n",
        "from urllib.parse import unquote, urlparse\n",
        "from urllib.error import HTTPError\n",
        "from zipfile import ZipFile\n",
        "import tarfile\n",
        "import shutil\n",
        "\n",
        "CHUNK_SIZE = 40960\n",
        "DATA_SOURCE_MAPPING = 'home-data-for-ml-course:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-competitions-data%2Fkaggle-v2%2F10211%2F111096%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240423%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240423T192107Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3Da79ab739220350bc82fce3713227e8042f85554b88732704a594d8c73016e3d738e0e844a06f5db498cf1656c2e34570300ca1d9992aa9645bf8fa52aee2f2362ad056733a6a363b5a9cd63d32b3a1924564b442058db86235c1b3e09d62dca2f2a3309eafd6a03b39f2edc16692b5d924efe315030fe5f1cc377c885ec829b0c1c3e22e9d1591de1c70b9389d1e08d84d3815beeb520967012bc783d9474d7efeb2e3ce3948229ee235f152047a6d72022aab1fc644b580863136485467289f5f57bbda98d2bcfe8c6b5abceb0bc87eae53fddeae0a5c8a38739c4dd0c8be7b33d34f78646dfc58842e6a579975f0c7ba0dfb713ce3798ef998e89e47a63277,mobile-price-classification:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F11167%2F15520%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240423%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240423T192107Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D19f2358f235830a3f5766cb2e82f7a05bed308d49400a98835148d22be3b3dc3195e079a6f865a19dfd54bf8828e04836da09aec50bc76bbca3fda3eb03ebd9c06271808b79b57768becaa70dd2fa2fa8e72466582d644ff8474188308fbd84ddb3accb4ed254c7a511a9f300f6b08bb25800b0d823a41ca882481511f53fd3b445a7f5f43f19426a2dce0f432d0c8bea6f04c28ee79f9db706bb25ba58304c22d68da2ccdebee7ce3da2a1f4948d5cae925bfad9a8711863ad88e05e4d05bee4d6b08d5b377ac0616f4243fd4f6b4e75950666be891c65c01e5b5d115a38316b80fe795ae7f80070904bf0a4797c99670e0f3e043d3c21005d0e93115b59b30,melbourne-housing-snapshot:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F2709%2F38454%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240423%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240423T192107Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3Da6c7ef4df2bd10be5f57caa30901c8c4804aace09cd8e8287c982fa4fbbbd4306968dc6fff4d8d7e3e051119cb9e6c4d598cae821dab0e1d63026821e112fc7cf9e955ed2f3a0cf9778bdd2d2ba2eda9da926a90b4e95edf9db7c748f13b36ff16f2682f7e9e5278f689bd56a1eafef7fb2ed3898841c840a760bc01759a8e89d0c65bdb0044a4e98e96da1b32c82e8cc4455ab93414c4fa97740ababcb1e1a774b71fec56d55a3f3648120ed60ca978c7ab7732cdad68e584f9c8e0ce83ce8da76c6d1272821c16966f0171c631894a38c2d2e377ea8c677b902907d1a415747af2ae48e0df44e6922acd922582d81915dfce553fff3cda6f2a93e959342339'\n",
        "\n",
        "KAGGLE_INPUT_PATH='/kaggle/input'\n",
        "KAGGLE_WORKING_PATH='/kaggle/working'\n",
        "KAGGLE_SYMLINK='kaggle'\n",
        "\n",
        "!umount /kaggle/input/ 2> /dev/null\n",
        "shutil.rmtree('/kaggle/input', ignore_errors=True)\n",
        "os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)\n",
        "os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)\n",
        "\n",
        "try:\n",
        "  os.symlink(KAGGLE_INPUT_PATH, os.path.join(\"..\", 'input'), target_is_directory=True)\n",
        "except FileExistsError:\n",
        "  pass\n",
        "try:\n",
        "  os.symlink(KAGGLE_WORKING_PATH, os.path.join(\"..\", 'working'), target_is_directory=True)\n",
        "except FileExistsError:\n",
        "  pass\n",
        "\n",
        "for data_source_mapping in DATA_SOURCE_MAPPING.split(','):\n",
        "    directory, download_url_encoded = data_source_mapping.split(':')\n",
        "    download_url = unquote(download_url_encoded)\n",
        "    filename = urlparse(download_url).path\n",
        "    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)\n",
        "    try:\n",
        "        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:\n",
        "            total_length = fileres.headers['content-length']\n",
        "            print(f'Downloading {directory}, {total_length} bytes compressed')\n",
        "            dl = 0\n",
        "            data = fileres.read(CHUNK_SIZE)\n",
        "            while len(data) > 0:\n",
        "                dl += len(data)\n",
        "                tfile.write(data)\n",
        "                done = int(50 * dl / int(total_length))\n",
        "                sys.stdout.write(f\"\\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded\")\n",
        "                sys.stdout.flush()\n",
        "                data = fileres.read(CHUNK_SIZE)\n",
        "            if filename.endswith('.zip'):\n",
        "              with ZipFile(tfile) as zfile:\n",
        "                zfile.extractall(destination_path)\n",
        "            else:\n",
        "              with tarfile.open(tfile.name) as tarfile:\n",
        "                tarfile.extractall(destination_path)\n",
        "            print(f'\\nDownloaded and uncompressed: {directory}')\n",
        "    except HTTPError as e:\n",
        "        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')\n",
        "        continue\n",
        "    except OSError as e:\n",
        "        print(f'Failed to load {download_url} to path {destination_path}')\n",
        "        continue\n",
        "\n",
        "print('Data source import complete.')\n"
      ],
      "metadata": {
        "id": "jNsKLM06Z57f"
      },
      "cell_type": "code",
      "outputs": [],
      "execution_count": null
    },
    {
      "cell_type": "markdown",
      "source": [
        "**This notebook is an exercise in the [Introduction to Machine Learning](https://www.kaggle.com/learn/intro-to-machine-learning) course.  You can reference the tutorial at [this link](https://www.kaggle.com/dansbecker/underfitting-and-overfitting).**\n",
        "\n",
        "---\n"
      ],
      "metadata": {
        "id": "EN8SfDimZ57k"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Recap\n",
        "You've built your first model, and now it's time to optimize the size of the tree to make better predictions. Run this cell to set up your coding environment where the previous step left off."
      ],
      "metadata": {
        "id": "5PRBmri5Z57l"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Code you have previously used to load data\n",
        "import pandas as pd\n",
        "from sklearn.metrics import mean_absolute_error\n",
        "from sklearn.model_selection import train_test_split\n",
        "from sklearn.tree import DecisionTreeRegressor\n",
        "\n",
        "\n",
        "# Path of the file to read\n",
        "iowa_file_path = '../input/home-data-for-ml-course/train.csv'\n",
        "\n",
        "home_data = pd.read_csv(iowa_file_path)\n",
        "# Create target object and call it y\n",
        "y = home_data.SalePrice\n",
        "# Create X\n",
        "features = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']\n",
        "X = home_data[features]\n",
        "\n",
        "# Split into validation and training data\n",
        "train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)\n",
        "\n",
        "# Specify Model\n",
        "iowa_model = DecisionTreeRegressor(random_state=1)\n",
        "# Fit Model\n",
        "iowa_model.fit(train_X, train_y)\n",
        "\n",
        "# Make validation predictions and calculate mean absolute error\n",
        "val_predictions = iowa_model.predict(val_X)\n",
        "val_mae = mean_absolute_error(val_predictions, val_y)\n",
        "print(\"Validation MAE: {:,.0f}\".format(val_mae))\n",
        "\n",
        "# Set up code checking\n",
        "from learntools.core import binder\n",
        "binder.bind(globals())\n",
        "from learntools.machine_learning.ex5 import *\n",
        "print(\"\\nSetup complete\")"
      ],
      "metadata": {
        "execution": {
          "iopub.status.busy": "2024-04-23T19:10:45.439556Z",
          "iopub.execute_input": "2024-04-23T19:10:45.439956Z",
          "iopub.status.idle": "2024-04-23T19:10:48.373493Z",
          "shell.execute_reply.started": "2024-04-23T19:10:45.439926Z",
          "shell.execute_reply": "2024-04-23T19:10:48.372311Z"
        },
        "trusted": true,
        "id": "RwsOnhWYZ57m",
        "outputId": "6c9d474d-7576-4171-b155-6edcda31e3c4"
      },
      "execution_count": null,
      "outputs": [
        {
          "name": "stdout",
          "text": "Validation MAE: 29,653\n\nSetup complete\n",
          "output_type": "stream"
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Exercises\n",
        "You could write the function `get_mae` yourself. For now, we'll supply it. This is the same function you read about in the previous lesson. Just run the cell below."
      ],
      "metadata": {
        "id": "UGdRPOBdZ57n"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):\n",
        "    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)\n",
        "    model.fit(train_X, train_y)\n",
        "    preds_val = model.predict(val_X)\n",
        "    mae = mean_absolute_error(val_y, preds_val)\n",
        "    return(mae)"
      ],
      "metadata": {
        "execution": {
          "iopub.status.busy": "2024-04-23T19:11:24.610448Z",
          "iopub.execute_input": "2024-04-23T19:11:24.610868Z",
          "iopub.status.idle": "2024-04-23T19:11:24.617461Z",
          "shell.execute_reply.started": "2024-04-23T19:11:24.610839Z",
          "shell.execute_reply": "2024-04-23T19:11:24.616204Z"
        },
        "trusted": true,
        "id": "3_YZcjLIZ57n"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Step 1: Compare Different Tree Sizes\n",
        "Write a loop that tries the following values for *max_leaf_nodes* from a set of possible values.\n",
        "\n",
        "Call the *get_mae* function on each value of max_leaf_nodes. Store the output in some way that allows you to select the value of `max_leaf_nodes` that gives the most accurate model on your data."
      ],
      "metadata": {
        "id": "4XVBZTPNZ57o"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "candidate_max_leaf_nodes = [5, 25, 50, 100, 250, 500]\n",
        "# Write loop to find the ideal tree size from candidate_max_leaf_nodes\n",
        "scores = {leaf_size: get_mae(leaf_size, train_X, val_X, train_y, val_y) for leaf_size in candidate_max_leaf_nodes}\n",
        "\n",
        "# Store the best value of max_leaf_nodes (it will be either 5, 25, 50, 100, 250 or 500)\n",
        "best_tree_size = min(scores, key=scores.get)\n",
        "\n",
        "# Check your answer\n",
        "step_1.check()"
      ],
      "metadata": {
        "execution": {
          "iopub.status.busy": "2024-04-23T19:14:19.328499Z",
          "iopub.execute_input": "2024-04-23T19:14:19.328926Z",
          "iopub.status.idle": "2024-04-23T19:14:19.383805Z",
          "shell.execute_reply.started": "2024-04-23T19:14:19.328898Z",
          "shell.execute_reply": "2024-04-23T19:14:19.382769Z"
        },
        "trusted": true,
        "id": "mhXEAYmFZ57o",
        "outputId": "8daf3a6c-d3e2-45f5-9a7a-363955202417"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": "<IPython.core.display.Javascript object>",
            "application/javascript": "parent.postMessage({\"jupyterEvent\": \"custom.exercise_interaction\", \"data\": {\"outcomeType\": 1, \"valueTowardsCompletion\": 0.5, \"interactionType\": 1, \"questionType\": 1, \"questionId\": \"1_BestTreeSize\", \"learnToolsVersion\": \"0.3.4\", \"failureMessage\": \"\", \"exceptionClass\": \"\", \"trace\": \"\"}}, \"*\")"
          },
          "metadata": {}
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": "Correct",
            "text/markdown": "<span style=\"color:#33cc33\">Correct</span>"
          },
          "metadata": {}
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# The lines below will show you a hint or the solution.\n",
        "#step_1.hint()\n",
        "#step_1.solution()"
      ],
      "metadata": {
        "trusted": true,
        "id": "RqstL6_1Z57p"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "## Step 2: Fit Model Using All Data\n",
        "You know the best tree size. If you were going to deploy this model in practice, you would make it even more accurate by using all of the data and keeping that tree size.  That is, you don't need to hold out the validation data now that you've made all your modeling decisions."
      ],
      "metadata": {
        "id": "0MBX16d2Z57p"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# Fill in argument to make optimal size and uncomment\n",
        "final_model = DecisionTreeRegressor(max_leaf_nodes=best_tree_size, random_state=1)\n",
        "\n",
        "# fit the final model and uncomment the next two lines\n",
        "final_model.fit(X, y)\n",
        "\n",
        "# Check your answer\n",
        "step_2.check()"
      ],
      "metadata": {
        "execution": {
          "iopub.status.busy": "2024-04-23T19:16:35.600807Z",
          "iopub.execute_input": "2024-04-23T19:16:35.601302Z",
          "iopub.status.idle": "2024-04-23T19:16:35.620577Z",
          "shell.execute_reply.started": "2024-04-23T19:16:35.601269Z",
          "shell.execute_reply": "2024-04-23T19:16:35.619439Z"
        },
        "trusted": true,
        "id": "bMv7_HjKZ57p",
        "outputId": "dea0369c-014b-480b-ec03-8d9c6832b2b0"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": "<IPython.core.display.Javascript object>",
            "application/javascript": "parent.postMessage({\"jupyterEvent\": \"custom.exercise_interaction\", \"data\": {\"outcomeType\": 1, \"valueTowardsCompletion\": 0.5, \"interactionType\": 1, \"questionType\": 2, \"questionId\": \"2_FitModelWithAllData\", \"learnToolsVersion\": \"0.3.4\", \"failureMessage\": \"\", \"exceptionClass\": \"\", \"trace\": \"\"}}, \"*\")"
          },
          "metadata": {}
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": "Correct",
            "text/markdown": "<span style=\"color:#33cc33\">Correct</span>"
          },
          "metadata": {}
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# step_2.hint()\n",
        "#step_2.solution()"
      ],
      "metadata": {
        "trusted": true,
        "id": "cVzze3eEZ57p"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "You've tuned this model and improved your results. But we are still using Decision Tree models, which are not very sophisticated by modern machine learning standards. In the next step you will learn to use Random Forests to improve your models even more.\n",
        "\n",
        "# Keep Going\n",
        "\n",
        "You are ready for **[Random Forests](https://www.kaggle.com/dansbecker/random-forests).**\n"
      ],
      "metadata": {
        "id": "4Lmh-JWuZ57q"
      }
    },
    {
      "cell_type": "markdown",
      "source": [
        "---\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "*Have questions or comments? Visit the [course discussion forum](https://www.kaggle.com/learn/intro-to-machine-learning/discussion) to chat with other learners.*"
      ],
      "metadata": {
        "id": "y7LA66m1Z57q"
      }
    }
  ]
}
