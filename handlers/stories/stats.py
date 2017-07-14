# Count chars, words, and pages

from model.chapter import Chapter
from model.section import Section


def extend_dictionary(d1, d2):
    """Extends the contents of d1 with the values in d2.

        :param d1: The dict to extend.
        :param d2: The dict to take values from.
    """
    for key in d2.keys():
        if key not in d1:
            d1[key] = d2[key]
        else:
            d1[key] += d2[key]


def count_text(text):
    """Calculates the stats for a given text.
       250 pages are estimated as 60000 words.
    
        :param text: The text to be accounted.
    """
    toret = {}
    text = text.strip()
    
    toret["crs"] = len(text)
    toret["ws"] = len(text.split())
    toret["pgs"] = (toret["ws"] * 250) // 60000
    
    return toret


def count_chapter(chapter_id):
    toret = { "crs": 0, "ws": 0, "pgs": 0 }
    sections = Section.query(Section.chapter == chapter_id)
        
    for section in sections:
        extend_dictionary(toret, count_text(section.text))

    return toret


def count(story_id):
    """Extracts the stats from a complete story.
        
        :param story_id: The id for a story to extract stats from.
    """
    toret = { "crs": 0, "ws": 0, "pgs": 0 }
    chapter_keys = Chapter.query(
                        Chapter.story == story_id).fetch(keys_only=True)

    # Access all chapters
    for chapter_key in chapter_keys:
        extend_dictionary(toret, count_chapter(chapter_key.id()))

    return toret
