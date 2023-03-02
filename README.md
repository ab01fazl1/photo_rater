# photo_rater
an async fast api that recieves a 2d array of urls (pictures) and rates each picture 
based on background color, watermark, picture aspect raio, picture size,the space between the main object and the picture edges

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install

```bash
pip install requirements.txt
```

## Usage
to run the api:

```bash
uvicorn main:app --reload
```
