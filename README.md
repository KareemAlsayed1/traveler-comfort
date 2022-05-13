# Traveler Recommendation System using Expert Systems
## Excutive Summary:

In our modern global economy, international tourism represents a key sector in the world economy. The travel and tourism sector is estimated to represent approximately 10% of the worldwide economy ​​(World Travel & Tourism Council, 2021). When international tourists travel to a foreign country for the first time, they encounter some challenges due to limited knowledge about that country. However, not all travelers experience the same challenges and levels of comfort when traveling to the same destination. Based on a literature review, there are three main areas where this project assesses the comfort levels and challenges for travelers: Climate, Infrastructure & Accessibility, and Political & Economic consideration. This project aims to build an expert system backed by first predicate logic by utilizing Prolog as a logic programming language. The AI Models use Certainty factors to give recommendations with certainty values. The AI logic relies on the traveler's profile to provide a personalized recommendation. Thus, different traveler profiles could get various assessments for the same destination. To provide an interactive user experience, the AI logic and the inference engine are wrapped within a web application. The web application gathers traveler's information by asking questions then presents the results on an interactive map. 

Each of the primary assessment areas includes subfactors to give an inclusive overall assessment. The subfactors include the following variables:
 - Climate Subfactors: 
    - Temperature
    - Precipitation
 - Infrastructure & Accessibility: 
    - ICT readiness Index
    - Ground Infrastructure Index
    - Health and Hygiene Index
 - Political & Economic considerations: 
    - Safety and Security Index
    - Purchasing Power
    - Civil & Political Freedom Index

![image](https://user-images.githubusercontent.com/44312799/168241905-bc2a4de7-5587-4895-a6b4-cab483f63a4f.png)


The following illustration shows the architecture of the project. Starting from the user interface, the traveler will interact with a website that asks questions to build a traveler profile. Also, that website would present the results in the form of an interactive world map. The frontend is developed using ReactJS, and it communicates with the Backend (which is built using Django Framework) through RESTful APIs. The backend has two main functionalities: tracking the user sessions and scheduling the Prolog functions (by communicating with the task scheduler server). The servers are running Prolog on Pyswib, so it is not a thread-safe function. Thus, the task scheduler utilizes multiprocessing to run the inference engine. Once the inference engine is running, it consults the knowledge base built based on the destinations data and predicate logic. The inference engine would either ask the user more questions or return the assessment results based on the input.  

The results would be presented as a broken-down analysis of each main area. The outcome would be a percentage that shows how much the system is certain that the traveler would feel comfortable under certain factor groups. These results would be reflected on a color-coded map for the user. 

## Files Structure:
```
traveler-comfort
│   Alpha Version Climate Expert System --> This folder holds the early version of the AI Models
│   Beta Version Expert System --> This folder holds the second version of teh AI Models (the dynamic models)
│   Archive Work --> This folder holds the early pervious stages of the project
│   .gitignore
│   README.md
└─── Interactive Website Expert System --> This is the main folder that holds the most recent version of the interactive website
│   │   frontend_server --> This Folder holds the frontend Reactjs server
│   │   prolog_backend --> This Folder holds the backend of the website including the prolog logic and knowledge base
└───────────────
```

## Getting Started: 
1. To get started, you need to clone the current github repo to your local machine.
2. Ensure that Git is installed on your machine, and install git-lfs for downloading large files. You can run `brew install git-lfs` if you are using MacOS
   - For more information to install that requriment, check out `https://git-lfs.github.com/`
3. Run `git clone https://github.com/KareemAlsayed1/traveler-comfort.git`
4. Go to the `Interactive Website Expert System`, and follow the steps mentioned in the README.md of each subfolder
