## Seawolf Search: Revolutionizing Lost & Found at Stony Brook University
![hopperhacks](https://github.com/ritessshhh/SeaWolf-Search-HopperHacks-2024/assets/81812754/bb47a6ef-a925-4c85-acb0-3332f9c90468)

Inspired by the Stony Brook University community's spirit and the frequent tales of lost belongings, we set out to create **Seawolf Search** powered by AI. Our mission was to simplify the recovery of lost items using technology, thus fostering a supportive campus environment.

## How to run?
```bash
git clone https://github.com/ritessshhh/SeaWolf-Search-HopperHacks-2024
cd SeaWolf-Search-HopperHacks-2024
pip install -r requirements.txt
cd Server
python3 server.py
cd ../Client
./index.html
```


## Inspiration

The inspiration behind **Seawolf Search** emerged from a common challenge faced by students and faculty alike within the vibrant yet sprawling campus of Stony Brook University: the frequent misplacement and loss of personal items. From textbooks left in lecture halls to keys dropped on the quad, the inconvenience and stress of losing valuable possessions are experiences shared by many. Recognizing the need for a streamlined, efficient method to reunite individuals with their lost items, we envisioned a platform that not only simplifies the process of reporting and retrieving lost items but also fosters a sense of community and collaboration.

## What It Does

**Seawolf Search** revolutionizes the traditional lost and found system by integrating advanced technology with the simplicity of human kindness. It's a comprehensive digital platform that empowers the Stony Brook community to easily report lost items and post found ones, all within a few clicks.

Upon entering the platform, users are greeted with a user-friendly interface where they can:
  
- **Search by uploading Lost Items**: Users of lost items can upload photos, which are then processed by our AI to create searchable tags and captions, making it easier to match with the existing database.
  
![Untitled-ezgif com-video-to-gif-converter-2](https://github.com/ritessshhh/SeaWolf-Search-HopperHacks-2024/assets/81812754/aaf1d6e6-5a9f-46eb-9483-33e4fa4ca821)

- **Smart Matching**: At the heart of Seawolf Search is our cosine similarity algorithm. It compares the descriptions and images of lost and found items, alerting users to potential matches potential matches from the database of found items, increasing the likelihood of recovery.

![Untitled-ezgif com-video-to-gif-converter-3](https://github.com/ritessshhh/SeaWolf-Search-HopperHacks-2024/assets/81812754/e1c14f8d-b5fd-47ab-bf99-0d175bee6d81)

- **Add Found Items**: Finders can upload images of the lost items and provide contact information so that the users of lost item can contact the finder. Our AI-powered system generates detailed descriptions and store the data in the database.
  
![Untitled-ezgif com-video-to-gif-converter](https://github.com/ritessshhh/SeaWolf-Search-HopperHacks-2024/assets/81812754/a9c4ad96-803f-424b-aa3e-9075a39a8ea5)

- **Community Engagement**: Beyond technology, Seawolf Search strengthens the communal bonds within Stony Brook University by encouraging positive actions and interactions, turning every user into an active participant in the campus-wide support network.


## What We Learned

With the progress of the project, we delved deep into **Artificial Intelligence (AI)**, specifically image recognition and natural language processing. The project was a hands-on experience in developing a full-stack application, from a user-friendly frontend to a robust backend. We also learned the importance of **user experience** design, ensuring our platform was easy to navigate. 

## How We Built It

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **AI Model**: BLIP (Bidirectional and Unidirectional Image-Text Pretraining) for image captioning
- **Text Similarity**: TF-IDF Vectorization, Cosine Similarity (Python's `scikit-learn` library)
- **Database**: SQLite for development, PostgreSQL for production
- **Version Control**: Git, GitHub

## Challenges Faced

The project was not without its hurdles. Achieving accurate image-to-text translation required fine-tuning the AI model, and we spent considerable time ensuring the platform could handle a large volume of requests efficiently. Integrating our backend with the machine learning model and frontend was a big challenge too, especially since we were all new to these technologies. Initially, it felt overwhelming, and our project didn't come together as smoothly as we hoped. But we were determined to make it work, we turned to YouTube videos and online tutorials for help. These resources were incredibly valuable, helping us piece together how each part of our project could connect effectively. Thanks to this learning process, we gradually overcame the integration hurdles. It was a great lesson in perseverance and teamwork, showing us that with the right resources and determination, we can solve even the most complex problems.

## Conclusion

Seawolf Search stands as a testament to the potential of AI in solving everyday problems. It's a bridge between technology and community, making the search for lost items a less daunting task. As we continue to improve and expand our platform, we are reminded of the power of collaboration and innovation in creating solutions that benefit everyone.

```python
print("Welcome to Seawolf Search - Where Lost Meets Found!")
