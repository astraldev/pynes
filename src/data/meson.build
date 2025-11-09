subdir('icons')
subdir('css')
subdir('svg')

# Install desktop file
desktop_file_path = app_id + '.desktop'
desktop_conf = configuration_data()
desktop_conf.set('APP_ID', app_id)
desktop_conf.set('NAME_SUFFIX', name_suffix)

desktop_file = configure_file(
  input: desktop_file_path + '.in',
  output: desktop_file_path,
  configuration: desktop_conf
)

# Install appdata/metainfo file
appdata_file_path = app_id + '.metainfo.xml'
appdata_conf = configuration_data()
appdata_conf.set('APP_ID', app_id)
appdata_conf.set('NAME_SUFFIX', name_suffix)

appdata_file = configure_file(
  input: appdata_file_path + '.in',
  output: appdata_file_path,
  configuration: appdata_conf
)

# Install menu XML
install_data(
  'menu.xml',
  install_dir: pkgdatadir
)

# Validate desktop file
desktop_file_validate = find_program('desktop-file-validate', required: false)
if desktop_file_validate.found()
  test(
    'validate-desktop',
    desktop_file_validate,
    args: [meson.current_build_dir() / desktop_file]
  )
endif
