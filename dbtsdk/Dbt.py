#!/usr/bin/env python3
"""
DBT API Client SDK for DPT API v2

Copyright (c) 2018 Rob Dunham (https://robdunham.info)

This software is available under the MIT license. See http://opensource.org/licenses/MIT for more info.

Documentation for DBT API calls is located at http://www.digitalbibleplatform.com/docs/

This is a Python fork of the DBT API Client PHP SDK (dbt-sdk-php)
https://bitbucket.org/faithcomesbyhearing/dbt-sdk-php

Source: https://github.com/Nilpo/dbt-sdk-python.git

"""

from typing import Dict, Optional
from urllib.request import urlopen
from urllib.parse import urlencode
import json
import time


class Dbt:
    """DBT Class"""

    # Configuration

    _api_endpoint: str = 'http://dbt.io'

    # API Version
    _api_version: str = '2'

    # Pointer to method that returns the response format constructed for the object
    # made public so that a user can change response type after initialization (mostly for debugging)
    response: str

    def __init__(self, application_key: str, api_uri: str = None, reply: str = None, response_type: str = None, echo: str = None, callback: str = None) -> None:
        """
        :param application_key: The identity of the app in the form of an application key
        :param api_uri: URL to use instead of default url
        :param reply: reply protocol
        :param response_type: return type of function (json[default]| list[python List]|url[only returns api url])
        :param echo: [true|false] whether or not to echo the call parameters
        :param callback: function name to use for JSONP reply
        """

        # URI to which to GET
        self._api_uri: str = api_uri or self._api_endpoint

        # Params which are shared on every API call
        self._dbt_params: Dict[str, str] = {
            'v': self._api_version,
            'key': application_key,
            'reply': reply or 'json',
            'callback': callback,
            'echo': echo
        }

        if 'array' in response_type:
            self._response = '_get_list_response'
        elif 'url' in response_type:
            self._response = '_get_api_uri'
        else:
            self._response = '_get_json_response'

    def __getattribute__(self, item):
        return self[item]

    def _get_list_response(self, resource_group: str, resource: str, params: Dict[str, str]) -> Optional[Dict]:
        """Imports a JSON api response to a Python List to be used by the server.

        :param resource_group: api resource group to call
        :param resource: api resource to call
        :param params: resource group resource method params
        :return: return from API as Python List or None
        """

        # feed = self.get_json_response(resource_group, resource, params)
        # if feed is not None:
        #     return json.loads(feed)
        # else:
        #     return None
        return json.loads(self._get_json_response(resource_group, resource, params)) or None

    def _get_json_response(self, resource_group: str, resource: str, params: Dict[str, str]) -> Optional[str]:
        """Queries DBT API and returns the response in JSON format.

        :param resource_group: api resource group to call
        :param resource: api resource to call
        :param params: resource group resource method params
        :return: JSON return from API or None
        """

        feed = None
        uri = self._get_api_uri(resource_group, resource, params) or None
        if uri is not None:
            with urlopen(uri) as response:
                feed = response.read().decode()

        return feed

    def _get_api_uri(self, resource_group: str, resource: str, params: Dict[str, str]) -> str:
        """Builds a specific API call URL depending on passed parameters

        :param resource_group: api resource group to call
        :param resource: api resource to call
        :param params: resource group resource method params
        :return: API endpoint URL
        """

        # request_params = dict(self._dbt_params)
        # request_params.update(params)
        request_params = dict(self._dbt_params, **params)
        query_string = urlencode(request_params)

        return self._api_uri + '/' + resource_group + '/' + resource + '?' + query_string

    def get_api_version(self) -> Optional[str]:
        """Wrapper method for /api/apiversion call"""

        return self[self._response]('api', 'apiversion', {})

    def get_api_reply(self) -> Optional[str]:
        """Wrapper method for /api/reply call"""

        return self[self._response]('api', 'reply', {})

    def get_audio_location(self, protocol: str = '') -> Optional[str]:
        """Wrapper method for /audio/location call

        :param protocol: Allows the caller to filter out servers that do not support a specified protocol (e.g http, https, rtmp, rtmp-amazon)
        """

        params = {'protocol': protocol}

        return self[self._response]('audio', 'location', params)

    def get_audio_path(self, dam_id: str, book_id: str = None, chapter_id: str = None) -> Optional[str]:
        """Wrapper method for /audio/path call

        :param dam_id: DAM ID of volume
        :param book_id: book id of the book to get chapters for
        :param chapter_id: chapter id of the chapter to get audio for
        """

        params = {
            'dam_id': dam_id,
            'book_id': book_id,
            'chapter_id': chapter_id
        }

        return self[self._response]('audio', 'path', params)

    def get_audio_zippath(self, dam_id: str) -> Optional[str]:
        """Wrapper method for /audio/zippath call

        :param dam_id: DAM ID of volume
        """

        params = {'dam_id': dam_id}

        return self[self._response]('audio', 'zippath', params)

    def get_verse_start(self, dam_id: str, book_id: str, chapter_id: str) -> Optional[str]:
        """Wrapper method for /audio/versestart call

        :param dam_id: DAM ID of volume
        :param book_id: book id of the book to get chapters for
        :param chapter_id: chapter id of the chapter to get audio for
        """

        params = {
            'dam_id': dam_id,
            'osis_code': book_id,
            'chapter_number': chapter_id
        }

        return self[self._response]('audio', 'versestart', params)

    def get_library_language(self, code: str = None, name: str = None, sort_by: str = None, full_word: str = None, family_only: str = None) -> Optional[str]:
        """Wrapper method for /library/language call

        :param code: language code on which to filter
        :param name: language name in either native language or English on which to filter
        :param sort_by: [code|name|english]
        :param full_word: [true|false] interpret name: as full words only
        :param family_only: [true|false] return only language families
        """

        params = {
            'code': code,
            'name': name,
            'full_word': full_word,
            'family_only': family_only,
            'sort_by': sort_by
        }

        # return self[self._response]('library', 'language', params)
        return getattr(self, self._response, None)('library', 'language', params)

    def get_library_version(self, code: str = None, name: str = None, sort_by: str = None) -> Optional[str]:
        """Wrapper method for /library/version call

        :param code: language code on which to filter
        :param name: language name in either native language or English on which to filter
        :param sort_by: [code|name|english]
        """

        params = {
            'code': code,
            'name': name,
            'sort_by': sort_by
        }

        # return self[self._response]('library', 'version', params)
        return self.__getattribute__(self._response)('library', 'version', params)

    def get_library_volume(self, dam_id: str = None, fcbh_id: str = None, media: str = None, delivery: str = None, language: str = None, language_code: str = None, version_code: str = None, updated: time.time = None, status: str = None, expired: str = None, org_id: int = None, full_word: str = None, language_family_code: str = None) -> Optional[str]:
        """Wrapper method for /library/volume call

        :param dam_id: DAM ID of volume
        :param fcbh_id:
        :param media: [text|audio|video] the format of languages the caller is interested in. All by default.
        :param delivery: [streaming|download|mobile|any|none] a criteria for approved delivery method. 'any' means any of the supported methods (this list may change over time). 'none' means assets that are not approved for any of the supported methods. All returned by default.
        :param language: Filter the versions returned to a specified language. For example return all the 'English' volumes.
        :param language_code: Filter the volumes returned to a specified language code. For example return all the 'eng' volumes.
        :param version_code: Filter the volumes returned to a specified version code. For example return all the 'ESV' volumes.
        :param updated: This is a unix timestamp in UTC to restrict volumes returned only if they were modified since the specified time.
        :param status: publishing status of volume
        :param expired: [true|false] whether or not the volume is expired
        :param org_id: Id of organization to which volume belongs
        :param full_word: [true|false] interpret name: as full words only
        :param language_family_code: Filter the volumes returned to a specified language code for language family
        """

        params = {
            'dam_id': dam_id,
            'fcbh_id': fcbh_id,
            'media': media,
            'delivery': delivery,
            'language': language,
            'full_word': full_word,
            'language_code': language_code,
            'language_family_code': language_family_code,
            'version_code': version_code,
            'updated': str(updated),
            'status': status,
            'expired': expired,
            'organization_id': str(org_id)
        }

        return self[self._response]('library', 'volume', params)

    def get_library_volumelanguage(self, root: str = None, language_code: str = None, media: str = None, delivery: str = None, status: str = None, org_id: int = None, full_word: str = None) -> Optional[str]:
        """Wrapper method for /library/volumelanguage call

        :param root: the language name root. Can be used to restrict the response to only languages that start with 'Quechua' for example
        :param language_code: (optional) 3 letter language code
        :param media: [text|audio|both] the format of languages the caller is interested in. This specifies if you want languages available in text or languages available in audio or only languages available in both. All are returned by default.
        :param delivery: [streaming|download|mobile|any|none] a criteria for approved delivery method. 'any' means any of the supported methods (this list may change over time). 'none' means assets that are not approved for any of the supported methods. All returned by default.
        :param status:
        :param org_id:
        :param full_word: [true|false] interpret $name as full words only
        """

        params = {
            'root': root,
            'language_code': language_code,
            'media': media,
            'delivery': delivery,
            'status': status,
            'organization_id': str(org_id),
            'full_word': full_word
        }

        return self[self._response]('library', 'volumelanguage', params)

    def get_library_volumelanguagefamily(self, root: str = None, language_code: str = None, media: str = None, delivery: str = None, status: str = None, org_id: int = None, full_word: str = None) -> Optional[str]:
        """Wrapper method for /library/volumelanguagefamily call

        :param root: the language name root. Can be used to restrict the response to only languages that start with 'Quechua' for example
        :param language_code: (optional) 3 letter language code
        :param media: [text|audio|both] the format of languages the caller is interested in. This specifies if you want languages available in text or languages available in audio or only languages available in both. All are returned by default.
        :param delivery: [streaming|download|mobile|any|none] a criteria for approved delivery method. 'any' means any of the supported methods (this list may change over time). 'none' means assets that are not approved for any of the supported methods. All returned by default.
        :param status:
        :param org_id:
        :param full_word: [true|false] interpret $name as full words only
        """

        params = {
            'root': root,
            'language_code': language_code,
            'media': media,
            'delivery': delivery,
            'status': status,
            'organization_id': str(org_id),
            'full_word': full_word
        }

        return self[self._response]('library', 'volumelanguagefamily', params)

    def get_library_bookorder(self, dam_id: str) -> Optional[str]:
        """Wrapper method for /library/bookorder call

        :param dam_id: DAM ID of a volume
        """

        params = {
            'dam_id': dam_id
        }

        return self[self._response]('library', 'bookorder', params)

    def get_library_book(self, dam_id: str) -> Optional[str]:
        """Wrapper method for /library/book

        :param dam_id: DAM ID of a volume
        """

        params = {
            'dam_id': dam_id
        }

        return self[self._response]('library', 'book', params)

    def get_library_bookname(self, language_code: str) -> Optional[str]:
        """Wrapper method for /library/bookname call

        :param language_code: language code for book names
        """

        params = {
            'language_code': language_code
        }

        return self[self._response]('library', 'bookname', params)

    def get_library_chapter(self, dam_id: str, book_id: str = None) -> Optional[str]:
        """Wrapper method for /library/chapter call

        :param dam_id: DAM ID of volume
        :param book_id: id of the book to get chapters for
        """

        params = {
            'dam_id': dam_id,
            'book_id': book_id
        }

        return self[self._response]('library', 'chapter', params)

    def get_library_verseinfo(self, dam_id: str, book_id: str = None, chapter_id: int = None, verse_start: int = None, verse_end: int = None) -> Optional[str]:
        """Wrapper method for /library/verseinfo call

        :param dam_id: DAM ID of volume
        :param book_id: id of the book to get text for
        :param chapter_id: id of the chapter to get text for
        :param verse_start: id of the verse to get text for (starting position)
        :param verse_end: id of the verse to get text for (ending position)
        """

        params = {
            'dam_id': dam_id,
            'book_id': book_id,
            'chapter_id': str(chapter_id),
            'verse_start': str(verse_start),
            'verse_end': str(verse_end)
        }

        return self[self._response]('library', 'verseinfo', params)

    def get_library_numbers(self, language_code: str, start: int, end: int) -> Optional[str]:
        """Wrapper method for /library/numbers call

        :param language_code: language code for book names
        :param start: first number for series of consecutive numbers returned
        :param end: last number for series of consecutive numbers returned
        """

        params = {
            'language_code': language_code,
            'start': str(start),
            'end': str(end)
        }

        return self[self._response]('library', 'numbers', params)

    def get_library_metadata(self, dam_id: str = None, org_id: int = None) -> Optional[str]:
        """Wrapper method for /library/metadata

        :param dam_id: DAM ID of volume
        :param org_id: ID for organization by which to filter
        """

        params = {
            'dam_id': dam_id,
            'organization_id': str(org_id)
        }

        return self[self._response]('library', 'metadata', params)

    def get_library_asset(self, dam_id: str = None) -> Optional[str]:
        """Wrapper method for /library/asset call

        :param dam_id: DAM ID of volume
        """

        params = {
            'dam_id': dam_id
        }

        return self[self._response]('library', 'asset', params)

    def get_library_organization(self, org_name: str = None, org_id: int = None) -> Optional[str]:
        """Wrapper method for /library/organization call

        :param org_name: name of organization
        :param org_id: ID for organization by which to filter
        """

        params = {
            'name': org_name,
            'id': str(org_id)
        }

        return self[self._response]('library', 'organization', params)

    def get_text_verse(self, dam_id: str, book_id: str = None, chapter_id: int = None, verse_start: int = None, verse_end: int = None, markup: str = None) -> Optional[str]:
        """Wrapper method for /text/verse call

        :param dam_id: DAM ID of volume
        :param book_id: id of the book to get text for
        :param chapter_id: id of the chapter to get text for
        :param verse_start: id of the verse to get text for (starting position)
        :param verse_end: id of the verse to get text for (ending position)
        :param markup: If specified returns the verse text in a variety of standarized formats. Current options include OSIS, and native (the default DBT format).
        """

        params = {
            'dam_id': dam_id,
            'book_id': book_id,
            'chapter_id': str(chapter_id),
            'verse_start': str(verse_start),
            'verse_end': str(verse_end),
            'markup': markup
        }

        return self[self._response]('text', 'verse', params)

    def get_text_search(self, dam_id: str, query: str, book_id: str = None, offset: int = None, limit: int = None) -> Optional[str]:
        """Wrapper method for /text/search call

        :param dam_id: DAM ID of volume
        :param query: The text the caller wishes to search for in the specified text
        :param book_id: The book ID to limit the search to
        :param offset: The offset for the set of results to return to start from
        :param limit: The number of results to return. Default is 50.
        """

        params = {
            'dam_id': dam_id,
            'query': query,
            'book_id': book_id,
            'offset': str(offset),
            'limit': str(limit)
        }

        return self[self._response]('text', 'search', params)

    def get_text_searchgroup(self, dam_id: str, query: str) -> Optional[str]:
        """Wrapper method for /text/searchgroup call

        :param dam_id: DAM ID of volume
        :param query: The text the caller wishes to search for in the specified text
        """

        params = {
            'dam_id': dam_id,
            'query': query
        }

        return self[self._response]('text', 'searchgroup', params)

    def get_video_jesusfilm(self, dam_id: str, encoding: str, book_id: str = None, chapter_id: int = None, verse_id: int = None) -> Optional[str]:
        """Wrapper method for /video/jesusfilm call

        :param dam_id: DAM ID of volume
        :param encoding: The encoding to request. Either mp4 or m3u8.
        :param book_id: book ID of the book to get text for
        :param chapter_id: chapter ID of the chapter to get text for
        :param verse_id: Verse id ID request
        """

        params = {
            'dam_id': dam_id,
            'encoding': encoding,
            'book_id': book_id,
            'chapter_id': str(chapter_id),
            'verse_id': str(verse_id)
        }

        return self[self._response]('video', 'jesusfilm', params)

    def get_video_videopath(self, dam_id: str, encoding: str = 'mp4', resolution: str = 'lo', segment_order: int = None, book_id: str = None, chapter_id: int = None, verse_id: int = None) -> Optional[str]:
        """Wrapper method for /video/videopath call

        :param dam_id: DAM ID of volume (null to use default from the class init)
        :param encoding: The encoding to request. Either mp4 or m3u8.
        :param resolution: The video resolution: lo, med, or hi
        :param segment_order: The segment order to retrieve
        :param book_id: book ID of the book to get text for
        :param chapter_id: chapter ID of the chapter to get text for
        :param verse_id: verse ID to request
        """

        params = {
            'dam_id': dam_id,
            'encoding': encoding,
            'resolution': resolution,
            'segment_order': str(segment_order),
            'book_id': book_id,
            'chapter_id': str(chapter_id),
            'verse_id': str(verse_id)
        }

        return self[self._response]('video', 'videopath', params)
