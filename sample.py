from dbtsdk import Dbt
import os
import json

# Read the DBT API key from env or assign it here
api_key = os.environ['DBT_API_KEY']

# Instantiate the DBT SDK
dbt = Dbt.Dbt(api_key)

# Get the current API version
response = dbt.get_api_version()
json_response = json.loads(response)
for k, v in json_response.items():
    print("{k}: {v}".format(**locals()))

# Get the root locations of audio files
response = dbt.get_audio_location(protocol='http')
roots = json.loads(response)
for r in roots:
    root_path = f"{r['protocol']}://{r['server']}{r['root_path']}/"
    print(root_path)

# Get a list of all languages for which one or more audio volumes are available
response = dbt.get_library_volumelanguagefamily(media='audio')
languages = json.loads(response)
for lang in languages:
    print(lang['language_family_code'], lang['language_family_english'])

# Get a list of all languages for which one or more text volumes are available
response = dbt.get_library_volumelanguagefamily(media='text')
languages = json.loads(response)
for lang in languages:
    print(lang['language_family_code'], lang['language_family_english'])

# Get a list of English volumes
response = dbt.get_library_volume(language_code='ENG', media='text', delivery='web')
volumes = json.loads(response)
for v in volumes:
    print(v['dam_id'], v['volume_name'])

# Get a list of books for a volume
response = dbt.get_library_book(dam_id='ENGNASN2ET') # NAS New American Standard Bible
books = json.loads(response)
for b in books:
    print(b)

# Get a verse range
response = dbt.get_text_verse(dam_id='ENGKJVN2ET', book_id='John', chapter_id=3, verse_start=16)
verses = json.loads(response)
for verse in verses:
    b = verse['book_name']
    c = verse['chapter_id']
    v = verse['verse_id']
    print("{b} {c}:{v}".format(**locals()))
    print(verse['verse_text'])

# Get Genesis 1:1-2 from the KJV
response = dbt.get_text_verse(dam_id='ENGKJVO1ET', book_id='Gen', chapter_id=1, verse_start=1, verse_end=2)
verses = json.loads(response)
for verse in verses:
    b = verse['book_name']
    c = verse['chapter_id']
    v = verse['verse_id']
    print("{b} {c}:{v}".format(**locals()))
    print(verse['verse_text'])
