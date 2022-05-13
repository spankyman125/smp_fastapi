settings = {
    "analysis": {
        "filter": {
            "ru_Ru": {
                "type": "hunspell",
                "locale": "ru_RU",
                "dedup" : True
            },
            "ru_stop": {
                "type": "stop",
                "stopwords": "_russian_"
            },
            "ru_stemmer": {
                "type": "stemmer",
                "language": "russian"
            },
            "en_US": {
                "type": "hunspell",
                "locale": "en_US",
                "dedup" : True
            },
            "english_stop": {
                "type":       "stop",
                "stopwords":  "_english_" 
            },
            "english_stemmer": {
                "type":       "stemmer",
                "language":   "english"
            },
            "english_possessive_stemmer": {
                "type":       "stemmer",
                "language":   "possessive_english"
            }
        },
        "analyzer": {
            "default": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": [
                    "lowercase",
                    "ru_Ru",
                    "ru_stop",
                    "ru_stemmer",
                    "en_US",
                    "english_stop",
                    "english_stemmer",
                    "english_possessive_stemmer"
                ]
            }
        }
    }
}

mappings_albums = {
    "properties": {
        "title": {
            "type": "text"
        },
        "release_date": {
            "type": "date",
            "format": "yyyy-MM-dd"
        },
        "artists": {
            "type": "text"
        }
    }
}

mappings_artists = {
    "properties": {
        "name": {
            "type": "text"
        }
    }
}

mappings_songs = {
    "properties": {
        "title": {
            "type": "text"
        },
        "duration": {
            "type": "date",
            "format": "epoch_second"
        },
        "tags": {
            "type": "keyword"
        },
        "album": {
            "type":"text"
        },
        "artists": {
            "type": "text"
        }
    }
}