import os

from configparser import SafeConfigParser, NoSectionError, NoOptionError

directory = os.path.dirname(os.path.realpath(__file__))
source = os.path.join(directory, "i18n.ini")

translations = SafeConfigParser(allow_no_value=True)
translations.read(source)


def gettext(txt):
    try:
        return translations.get("en", txt) # XXX: hard-coded locale
    except (NoSectionError, NoOptionError): # XXX: should not be necessary?
        return txt


def ngettext(singular, plural, n):
    pass # TODO
