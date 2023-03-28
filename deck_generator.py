import genanki

# Load results from JSON file
import json
with open("results.json", "r") as f:
    results = json.load(f)
    

# Generate Anki deck
my_deck = genanki.Deck(
    2055555423,
    'My Uncommon Words Deck')

# Create Anki model
my_model = genanki.Model(
    1607392319,
    'Basic Model',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        },
    ])

# Add cards to deck
for lemma in results:
    # Check if the word frequency is below a certain threshold
    if results[lemma]["frequency"] < 0.0005:
        # Create front and back of card
        front = lemma
        back = "<br>".join([f'<audio src="{occurrence["file"]}" controls><a href="{occurrence["file"]}">{occurrence["file"]}</a> ({occurrence["start"]:.1f} - {occurrence["end"]:.1f})</audio>' for occurrence in results[lemma]["occurrences"]])
        # Create note and add it to the deck
        my_note = genanki.Note(
            model=my_model,
            fields=[front, back])
        my_deck.add_note(my_note)



# Create Anki package and save it to disk
my_package = genanki.Package(my_deck)
my_package.write_to_file('my_deck.apkg')