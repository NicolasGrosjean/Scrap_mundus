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

We need to replace manually the words *Aujourd'hui* and *Hier* by valid dates.

## Convert the data in CSV

Run the following script to convert the data into a CSV file.

```
python json_to_csv.py mundus_article.json
```

## Extract data of a month

Run the following script to extract posts of a month (December 2021 in example) to help to write the Diarium Strategorum.

```
python extract_month_posts.py mundus_article.csv 2021-12
```

The generated BBcode is written in the file *Diarium_Strategorum_2021-12.txt* (2021-12 is the input in the command).

## Run notebook to compute graphs

Run the following commands.

```
cd notebook
jupyter notebook
```
