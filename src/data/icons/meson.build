icon_sizes = ['scalable']

foreach size : icon_sizes
  icon_dir = get_option('datadir') / 'icons' / 'hicolor' / size / 'apps'
  if size == 'scalable'
    install_data(
      'scalable' / 'apps' / 'pynes.svg',
      install_dir: icon_dir,
      rename: app_id + '.svg'
    )
  else
    install_data(
      size / 'apps' / 'pynes.png',
      install_dir: icon_dir,
      rename: app_id + '.png'
    )
  endif
endforeach
