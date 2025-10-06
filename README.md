# IA-Data-Collector
## About The Project
A Streamlit-based tool that automates the process of identifying and analyzing viral YouTube videos.
Based on category filters and specifications, the application utilizes the Gemini API (Google GenAI) to generate a list
of relevant channels. Then, using the YouTube Data API, it retrieves the most popular videos from those 
channels and extracts their key metrics (views, likes, title, creator, date, etc.).

Finally, the results are automatically stored in a Google Sheet, organized into columns with key information such as 
video name, creator, view count, likes, publication date, and more. This workflow streamlines the exploration of YouTube 
trends by combining generative AI, automated analysis, and cloud services.

### Built With
* ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) 
* ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
* ![Gemini API](https://img.shields.io/badge/Gemini_API-34A853?logo=google&logoColor=white)
* ![YouTube Data API](https://img.shields.io/badge/YouTube_Data_API-FF0000?logo=youtube&logoColor=white)
* ![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?logo=googlecloud&logoColor=white)

## Tool working
[![](https://img.youtube.com/vi/9ECP1U9GGZ0/maxresdefault.jpg)](https://youtu.be/9ECP1U9GGZ0)

## How to prove it your self
1. **Go to the app:**  
   👉 [YouTube Data Collector Tool (Live Demo)](https://ia-youtube-datacollector-gblv6hxmvyttqnblgiztyl.streamlit.app/)

2. **If the app is asleep**, click **"Wake up"** and wait a few seconds for it to start.  
   *(This may happen because the app is hosted on a free server that pauses when inactive.)*

3. **Test it out:**
   <br>Enter the required prompt information and start the tool.
   <br>*(Pd: The tool is spanish because it was for a Mexican company)*
4. **View the results in real time:**  
   The collected information will automatically appear in this shared Google Sheet:  
   📊 [Live Demo Sheet](https://docs.google.com/spreadsheets/d/1_Ui8UWVdmZ8vtm_eYVeEEXaRX2p-OWMztg9PddANclY/edit?gid=0#gid=0)