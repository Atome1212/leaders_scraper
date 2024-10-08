# 🌍 Country Leaders Scraper
<p align="center">
  <a href="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1">
      <img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDU3aGpncjZheW1hNGtvbzN5eGxyM2o1YXk0eTMwa3U1N2pvcW4wayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/mcsPU3SkKrYDdW3aAU/giphy.webp" alt="Click me !" width="300" />
  </a>
</p>

## 🔣 Language
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)


## 📑 Table of Contents
-  [📝 Description](#-description)
-  [📥 Installation](#-installing-dependencies)
-  [🚀 Usage](#-usage)
-  [🔍 Function Descriptions](#-function-descriptions)
-  [📌 Notes](#-notes)
-  [👥 Authors](#-authors)
-  [🌳 Project Tree](#-project-tree)

## 📝 Description

This Python script retrieves information about leaders from various countries through an API and extracts the first paragraph of their biography from their Wikipedia page. The data is then saved to a JSON file.

## 📥 Installation

```bash
git clone git@github.com:Atome1212/leaders_scraper.git
cd wine-market-analysis
pip install -r requirements.txt
```

## 🚀 Usage

1. Copy the script to your local machine.
2. Run the script using Python:

```sh
python ./leaders_scraper/leaders_scraper.py
```

## 🔍 Function Descriptions

`get_first_paragraph(url: str, session) -> str` 

This function retrieves the first paragraph of a given Wikipedia article. It uses a requests session to perform the HTTP request and BeautifulSoup to parse the HTML.

- `url`: URL of the Wikipedia page
- `session`: HTTP requests session

`get_cookies() -> requests.cookies.RequestsCookieJar` 

This function retrieves the cookies necessary to access the API.

`get_leaders() -> Dict[str, List[str]]`

This function retrieves the list of countries and their leaders from the API. For each leader, it extracts the first paragraph of their Wikipedia biography.

`save(leaders_per_country: Dict[str, List[str]]) -> None`

This function saves the leaders' data to a JSON file.

`check(leaders_per_country: Dict[str, List[str]]) -> None`

This function verifies that the saved data matches the original data by loading the JSON file and comparing the two datasets.

`main() -> None`

Main function that orchestrates the execution of the various steps: retrieving leaders, saving, and verification.

## 📌 Notes

- The script handles errors in fetching the biography by adding a "Bio not available" entry in case of failure.
- If an API request is rejected (403 status code), the script will attempt to retrieve new cookies before retrying.

## 👥 Author

**👷‍♂️ [Atome1212](https://github.com/Atome1212)**: Data Engineer

## 🌳 Project Tree

```
/leaders_scraper
├── Data
│   └── leaders.json
├── README.md
├── leaders_scraper.py
└── requirements.txt
```

This tree provides an overview of the project structure, showing where each file and directory is located.
