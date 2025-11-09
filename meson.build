project(
  'pynes',
  version: '3.2.0',
  meson_version: '>= 1.4.0',
  default_options: [
    'warning_level=2',
    'werror=false',
  ],
)

gnome = import('gnome')
python = import('python')

py_installation = python.find_installation('python3',
  modules: ['gi', 'timeutilities']
)

# Dependencies
dependency('pygobject-3.0', version: '>= 3.42.0')
dependency('gtk4', version: '>= 4.16.0')
dependency('libadwaita-1', version: '>= 1.6.0')

pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = py_installation.get_install_dir() / 'pynes'

profile = get_option('profile')
if profile == 'development'
  app_id = 'org.astralco.pynes.Devel'
  prefix = '/org/astralco/pynes/Devel'
  name_suffix = ' (Development)'
elif profile == 'default'
  app_id = 'org.astralco.pynes'
  prefix = '/org/astralco/pynes'
  name_suffix = ''
endif

conf = configuration_data()
conf.set('PYTHON', py_installation.full_path())
conf.set('VERSION', meson.project_version())
conf.set('APP_ID', app_id)
conf.set('APP_PREFIX', prefix)
conf.set('pkgdatadir', pkgdatadir)
conf.set('bindir', get_option('prefix') / get_option('bindir'))

subdir('src')

gnome.post_install(
#   glib_compile_schemas: true,
  gtk_update_icon_cache: true,
#   update_desktop_database: true,
)