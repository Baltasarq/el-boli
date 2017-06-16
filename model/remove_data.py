#!/usr/bin/env python
# MIT License
# (c) baltasar 2017


from google.appengine.ext import ndb

from model.chapter import Chapter
from model.section import Section
from model.character import Character


@ndb.transactional(propagation=ndb.TransactionOptions.INDEPENDENT)
def remove_character(chr_key):
    """Removes a given character

        :param chr_key: The character key."""
    chr_key.delete()


@ndb.non_transactional
def remove_all_characters_of(story_key):
    characters_keys = Character.query(Character.story == story_key.id()).fetch(keys_only=True)
    ndb.delete_multi(characters_keys)


@ndb.transactional(propagation=ndb.TransactionOptions.INDEPENDENT)
def remove_section(section_key):
    """Removes a given section
    
        :param section_key: The section key."""
    section_key.delete()


@ndb.non_transactional
def remove_all_sections_of(chapter_key):
    sections_keys = Section.query(Section.chapter == chapter_key.id()).fetch(keys_only=True)
    ndb.delete_multi(sections_keys)


@ndb.transactional
def remove_chapter(chapter_key):
    """Removes a given chapter

        :param chapter_key: The chapter key."""
    remove_all_sections_of(chapter_key)
    chapter_key.delete()

@ndb.non_transactional
def remove_all_chapters_of(story_key):
    chapters_keys = Chapter.query(Chapter.story == story_key.id()).fetch(keys_only=True)

    for chapter_key in chapters_keys:
        remove_all_sections_of(chapter_key)

    ndb.delete_multi(chapters_keys)


@ndb.transactional
def remove_story(story_key):
    """Removes a given story

        :param story_key: The story key."""
    remove_all_chapters_of(story_key)
    remove_all_characters_of(story_key)
    story_key.delete()
