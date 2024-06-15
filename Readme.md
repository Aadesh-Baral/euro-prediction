# Data Extractor
Install dependencies in requirements.txt with:
`pip3 install -r requirements.txt`

#### To extract data from predictions page into csv file follow the following steps:
1. Open predictons page in the link: Example: https://euros.predictthefootball.com/minileague/predictions/15333.
2. Click on icon -> 🔍 and a modal is opened with all the predictons.
3. Inspect the page and copy it's html content
4. Paste the html content in `score.html`, create `score.html` in the project root folder if it doesn't exist.
5. To extract all the predictions made run the following command. It will create a csv file with username and predictions.
    ```python main.py extract_predictions```
6. To find the winner run the following command:
    ```python main.py find_winners --score=<SCORE>```

