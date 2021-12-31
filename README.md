# Scrap Mundus Bellicus website to have insights

## Installation

The running environment can be installed by several ways.

### With Miniconda

Install [Miniconda](https://conda.io/miniconda.html).

Create a conda environment with the following command.

````
conda env create --file environment.yml
````

### With another install

With an alreaday installed Python environment, install the required packages with the following command.

```
pip install requirements.txt
```

## Activate the environment to run code
### Windows
````
activate scrap_websites
````

### Linux
````
source activate scrap_websites
````

## Update the data

Run the following command to scrap Mundus articles.

```
cd mundus
rm data/mundus_article.json
scrapy crawl mundus_article -o data/mundus_article.json
```

Nota: You maybe need to update MAX_PAGE constant in 
`mundus/mundus/spiders/article.py` to change the number of scraped pages.

## Convert the data in CSV

Run the following script to convert the data into a CSV file.

```
python json_to_csv.py mundus_article.json
```

## Run notebook to compute graphs

Run the following commands.

```
cd notebook
jupyter notebook
```
