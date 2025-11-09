subdir('bin')
subdir('data')

# Configure __init__.py
init_conf = configuration_data()
init_conf.set('VERSION', meson.project_version())
init_conf.set('APP_PREFIX', prefix)
init_conf.set('APP_ID', app_id)

configure_file(
  input: './pynes/__init__.py.in',
  output: '__init__.py',
  configuration: init_conf,
  install_dir: moduledir
)

# Install the entire pynes package recursively, excluding .pyc files
install_subdir('pynes',
  install_dir: py_installation.get_install_dir(),
  strip_directory: false,
  exclude_directories: ['__pycache__'],
  exclude_files: ['*.pyc', '*.py.in', '__init__.py.in']
)