# Extraction and analysis of data about connections between students of HIgher School of Economics in St. Petersburg

## Description of the files:
- data_extraction.py is scrap the data about HSE students from VK communities
- extract_friends.py is to get their friend lists and merge them 
- to_gephi.py is to transform python objects into .csv files in order to then feed them to Gephi (to make vizualizaions and calculate needed metrics)
- vk_api_local.py is a file containing objects imported in other files (to use VK's API). You need to use your own login and password (and change the number of VK accounts you're gonna use for scrapping)
- hse_graphs_article.docs is a file where I describe and sum up the results of the work done in this project
