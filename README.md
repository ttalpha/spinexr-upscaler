# X-ray Upscaler

## Goal
The goal of this project is to develop an AI model that can upscale X-ray images, improving their resolution and clarity for better medical analysis.

## Project Setup

### Prerequisites
- Anaconda or Miniconda (for `server/` and `ai/` only)
- CUDA 12.6 (for `server/` and `ai/` only)
- Node.js 18 or higher (for `web/` and `desktop/` only)

### Installation

#### AI Model
1. Navigate to the `ai` directory:
    ```sh
    cd ai
    ```
2. Create a conda environment:
    ```sh
    conda create -n ai python=3.12.7
    ```
3. Activate the conda environment:
    ```sh
    conda activate ai
    ```
4. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```
5. Download the dataset in either JPEG or DICOM format (WARNING: very heavy):
    - [JPEG (~570GB)](https://physionet.org/content/mimic-cxr-jpg/2.1.0/)
    - [DICOM (~4.7TB)](https://physionet.org/content/mimic-cxr/2.1.0/)
6. Flatten the directories and place 99% images in `ai/dataset/train` and 1% in `ai/dataset/test`
7. Train the model:
    ```sh
    python main.py
    ```

#### Desktop Application
1. Navigate to the `desktop/` directory:
    ```sh
    cd desktop
    ```
2. Install the required npm packages:
    ```sh
    npm install
    ```
3. Run the desktop application:
    ```sh
    npm start
    ```

#### Web Application
1. Navigate to the `web` directory:
    ```sh
    cd web
    ```
2. Install the required npm packages:
    ```sh
    npm install
    ```
3. Run the web application:
    ```sh
    npm run dev
    ```
4. Open the browser at [http://localhost:5173](http://localhost:5173)

### Server
1. Navigate to the `server` directory:
    ```sh
    cd server
    ```
2. Create a conda environment:
    ```sh
    conda create -n server python=3.12.7
    ```
3. Activate the conda environment:
    ```sh
    conda activate server
    ```
4. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```
5. Run the server:
    ```sh
    flask --app . run --debug
    ```
6. Open the browser at [http://localhost:5000](http://localhost:5000)

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## Acknowledgments
- Special thanks to all contributors and supporters of this project.