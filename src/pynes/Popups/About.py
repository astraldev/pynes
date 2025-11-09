from gi.repository import Adw, Gtk
from pynes import VERSION, APP_PREFIX

class Definitions(object):
    developer_name = "Ekure Edem"
    developer_email = "ekureedem480@gmail.com"
    app_name = "Pynes"
    description = ""
    copyright = "Copyright © 2021 - 2025 Ekure Edem"
    developer = [f"{developer_name} <{developer_email}>"]
    website = "https://github.com/astraldev/pynes"
    issue_url = "https://github.com/astraldev/pynes/issues/new"
    license = Gtk.License.GPL_3_0

class AboutPynes:
    @staticmethod
    def create() -> Adw.AboutDialog:
        about_dialog = Adw.AboutDialog.new()
        about_dialog.set_version(VERSION)
        about_dialog.set_application_icon(APP_PREFIX)
        about_dialog.set_application_name(Definitions.app_name)
        about_dialog.set_comments(Definitions.description)
        about_dialog.set_copyright(Definitions.copyright)
        about_dialog.set_website(Definitions.website)
        about_dialog.set_license_type(Definitions.license)
        about_dialog.set_developers(Definitions.developer)
        about_dialog.set_issue_url(Definitions.issue_url)
        about_dialog.set_comments(Definitions.description)
        about_dialog.set_developer_name(Definitions.developer_name)

        # TODO: Add support for release notes and other features
        # about_dialog.set_release_notes()
        # about_dialog.set_support_url()
        # about_dialog.set_debug_info()
        # about_dialog.set_debug_info_filename()

        return about_dialog
