# GenreGuesser: Guessing a Song's Genre from its Lyrics

**Team (alphabetical by last name):**
[Marc Dunker](https://github.com/Dunkerm)
[Rob Pasternak](https://github.com/robpasternak) (project lead)
[Jules Pastor](https://github.com/JJPPastor)
[Julia Welchering](https://github.com/julia-welch)

### Overview

- Different genres of music have differing tendencies with respect to their lyrical content.
    * Stereotypes: country songs are about trucks and freedom, pop songs are about romance, etc.
- **GenreGuesser** is a machine-learning classification algorithm trained on the lyrics of thousands of songs, which takes a string of lyrics and returns a predicted genre (along with probabilities for each genre in its domain of possibilities).
- The model will be trained locally but hosted on the cloud, with an API that will be accessed by a user-friendly app hosted on Heroku.

![productdiagram](productdiagram.png)

### Front End

- Hosted on Heroku, developed on Streamlit
- Textbox requesting a single song's lyrics; upon entering the lyrics the app will show:
    1. The predicted genre
    2. The probabilities assigned to each genre of those the model is trained on

### Back End

- Modelling pipeline trained locally:
    * Data scraped from [Genius.com](https://www.genius.com), using song metadata scraped from [Dave Tompkins's Music Database](https://cs.uwaterloo.ca/~dtompkin/music/) and the [Billboard](https://www.billboard.com/charts/hot-100/).
    * Initial genres: **Country**, **Folk**, **Jazz**, **Pop**, **Rap**, **Rock**
    * Data cleaned and vectorized for a bag-of-words model using term frequency-inverse document frequency (TF-IDF)
    * Result is fed to a *k-nearest neighbors* model (current settings: 5 neighbors, weighted by distance)
- Model uploaded to Google Cloud, where it is used to serve an API that makes predictions for new data
- API is accessed by front end to deliver user-friendly results

### Finishing the Minimal Viable Product (MVP)

1. Finish obtaining the scraped data
2. Test and train the base model locally
    * Code for testing and training model is finished, just need data
3. Move base model to Google Cloud
4. Finish code to create the API, start it up
5. Develop front end and push to Heroku

### Potential Extensions to the MVP

* Accumulating more data for training
* Decisions about what genres to include/exclude
* Improving upon the model
    * Finetune parameters using grid search (code already in place) or random search
    * Try different classifiers for bag-of-words
        * support vector machine
        * naive Bayes
        * decision tree
        * ensemble methods
        * etc.
    * Transitioning to deep learning models (requires more data)
        * recurrent neural networks (including LSTM and GRU)
        * convolutional neural networks
    * Potentially intresting but beyond the scope of the project: using transformers (BERT, RoBERTa)
* Switching to cloud-based training over local (especially useful for more complex deep learning models)
* Improving the app, possibly by switching from Streamlit to a more customizable format