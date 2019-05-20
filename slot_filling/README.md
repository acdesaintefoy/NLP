# Your challenge, if you accept it

In the attached file, you will find over 14K queries. Each query falls under one of 7 different intents:

* SearchCreativeWork (e.g. *Find me the I, Robot television show*),
* GetWeather (e.g. *Is it windy in Boston, MA right now?*),
* BookRestaurant (e.g. *I want to book a highly rated restaurant for me and my boyfriend tomorrow night*),
* PlayMusic (e.g. *Play the last track from Beyoncé off Spotify*),
* AddToPlaylist (e.g. *Add Diamonds to my roadtrip playlist*)
* RateBook (e.g. *Give 6 stars to Of Mice and Men*)
* SearchScreeningEvent (e.g. *Check the showtimes for Wonder Woman in Paris*)

For each intent, there is a set of slots we would like to extract (see the ontology below). The dataset we are providing you with is supervised with the corresponding intent and slots. The objective of this challenge is to build a  model for each intent that is able to extract the slots from a corresponding query. You can assume that each model will only be applied to queries of the corresponding intent.
 
For example, for the PlayMusic intent, a query could be *"Is there something new you can play by Lola Monroe?"*. In that case, we would expect your model specialized on PlayMusic queries to extract the following slots:
 
- sort: new
- artist: Lola Monroe

The idea behind this problem is to extract parameters from queries in natural language, so that a smart assistant can be built that reacts accordingly. For each of these intents, you are provided  with both a dev and a validation set. 

You are free to evaluate your solution in any way you want, but you may find some inspiration from the [following benchmark](https://medium.com/@alicecoucke/benchmarking-natural-language-understanding-systems-google-facebook-microsoft-and-snips-2b8ddcf9fb19), performed on the same dataset - metrics are computed on the provided `test` set

# What we expect back from you

- a strong, working solution, with performance metrics
- a report explaining your approach, what worked and didn't, plots, etc..
- source code that we can run and test on similarly formatted data

Use any methods and tools you like, any external dataset, library, or API: the more creativity & ambition, the better. For your own sake, and to preserve equity among candidates, we just ask you not to spend a dime on the problem. ;)

Feel free to go beyond just solving the challenge itself; this is your opportunity to shine, showcase your craft and way of thinking, and ultimately outperform other candidates!

We expect you to get back to us within a week, so let us know if you need more time!

Good luck!

PS: Please do not share this challenge, your code or any associated data as it may be used with other candidates :-)

## Ontology

### SearchCreativeWork
- object_type (e.g. novel, saga)
- object_name	(e.g. Harry Potter)

### SearchCreativeWork
- start_time
- spatial_relation (e.g. nearest, closest, in the neighborhood)
- object_location_type (e.g. cinema, movie house)
- location_name (e.g. Cineplex Odeon)
- movie_name	(e.g. Fight Club)
- movie_type (e.g. film, animé)
- object_type (e.g. movie, schedule)

### BookRestaurant
- timeRange
- spatial_relation (e.g. close by)
- poi	(e.g. my friend's house)
- city
- country
- state
- party_size_description	(e.g. me and my mother)
- party_size_number
- facility (e.g. spa, parking)
- restaurant_name
- restaurant_type (e.g. brasserie, gastronomic)
- served_dish (e.g. sushi, pizza)
- cuisine (e.g. japanese, italian)
- sort (e.g. best)

### PlayMusic
- album
- artist
- genre
- music_item (e.g. symphony, track, song)
- playlist
- service (e.g. spotify, deezer)
- sort (e.g. best, last, top 10)
- track
- year (e.g. eighties, 2004)

### RateBook
- object_part_of_series_type	(e.g. sagas, series, chronicle)
- rating_value	(e.g. 1,2 ...)
- object_type (e.g. book, novel)
- object_select (e.g. this, current)
- object_name	(e.g Madame Bovary)
- rating_unit (e.g. stars, points)
- best_rating (it is always 6)

### AddToPlaylist
- artist
- playlist_owner (e.g. my, alfred's)
- playlist
- entity_name	(e.g. Billie Jean)
- music_item (e.g. song, artist, album)


## Data format

Each entry in the datasets provided corresponds to a query, with the following structure:
```json
 {
  "data": [
    {
      "text": "I'd like to eat at a "
    },
    {
      "text": "taverna",
      "entity": "restaurant_type"
    },
    {
      "text": " that serves "
    },
    {
      "text": "chili con carne",
      "entity": "served_dish"
    },
    {
      "text": " for a party of "
    },
    {
      "text": "10",
      "entity": "party_size_number"
    },
    {
      "text": " "
    }
  ]
}
```
In this specific case, the query is:
```
"I'd like to eat at a taverna that services chili con carne for a party of 10 "
```


For each query, the `data` key contains the list of spans that forms the query. 

Each span has :
* a mandatory `text` key
* an optional `entity` key that specifies the slot associated to the span
