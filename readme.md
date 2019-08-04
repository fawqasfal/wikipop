This is a music recommendation algorithm that determines the popularity of artists and helps recommend you artists based on artists you currently like. It scrapes articles from Wikipedia, uses a naive Bayesian classifier to seperate articles about artists from articles that are not about artists, and implements a PageRank-like algorithm to build a directed weighted graph between artists that represent their relative popularity and similar artists (where "similarity" is determined by whether an artist's Wikipedia article links to another artist's Wikpedia article). 


Go into the src folder and run "python run.py restart". And then wait a long while. Like, hours.

-- 
I wrote a paper that explains each individual mechanism of this project. The conclusion shows what you're supposed to see after aforementioned "hours" :

https://docs.google.com/document/d/1xjjz74L_Ts5RWeeMrp9x3AouA5l3it92eWtZdfI67sE/edit?usp=sharing

The paper is also included here as a PDF. 

The abstract : 
"Music recommendation engines, such as Spotify or Pandora, are currently built through a variety of methods depending on the service. Pandora employs a manual discovery model in which musicologists take 20 to 30 minutes to assign weight values for 450 musical attributes for every song on the service. While The Music Genome Project has a wide array of songs,  this algorithm by it’s nature cannot scale as fast as an automated service --  It took Pandora over 10 years to accumulate 1 million songs. By comparison, a well-designed automated service can analyze over 10 million artists in a much shorter amount of time.
 iTunes Genius, Amazon, and Last.fm employ collaborative filtering models in which customers with a few common interests are used for recommendation sources between each other.This algorithm makes the naive assumption that just because 2 customers have one common interest, they will also have many other common interests. Furthermore, it’s focus on existing user data can lead to perpetuating already known interests.
Acoustic analysis engines such as Muffin often turn a blind eye to the cultural aspects of music and have trouble boiling down musical tastes to statistical analyses of signals.
 A newer approach is to analyze and develop an artist network, focusing purely on online articles about artists. By seeing which of these articles link to each other, and which artist articles have the highest amount and most popular incoming links, the algorithm can determine which artists are most related and which artists customers will have the highest probability of liking. Unlike all other mentioned models, it is automated, focuses on the community of artists as opposed to user data, and looks at a corpus of text written about the artists instead of analyzing audio files."

--

Some fun screenshots! :D 

![alt text](http://imgur.com/usR0sOE.png "Final probabilities for some of the most popular artists on a specific run")

![alt text](http://imgur.com/lmrX7Jx.png "Client telling me who I'd like given I like Tupac")
