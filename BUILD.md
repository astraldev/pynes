# Building Pynes

This document describes how to build this project using Meson / Flatpak.

## Prerequisites

### System Dependencies
- Python 3.10 or higher
- Meson >= 1.4.0
- GTK4 >= 4.16.0
- Libadwaita >= 1.6.0
- PyGObject >= 3.42.0

### Python Dependencies
- pygobject
- timeutilities

## Building Locally

### Meson setup

```bash
# Create build directory (opt: --prefix=/usr/local)
meson setup builddir

# Compile
meson compile -C builddir

# Install
meson install -C builddir
```

## Building with Flatpak

### Install GNOME SDK

```bash
flatpak install flathub org.gnome.Platform//47 org.gnome.Sdk//47
```

### Build Flatpak

```bash
flatpak-builder --force-clean --user --install build-dir build-aux/flatpak/org.astralco.pynes.json
```

## Development Build

```bash
meson setup builddir -Dprofile=development
meson compile -C builddir
meson install -C builddir
```

## Uninstalling

### Local Install
```bash
sudo ninja -C builddir uninstall
```

### Flatpak
```bash
flatpak uninstall org.astralco.pynes
```

## Troubleshooting

### GTK/Adwaita version errors

Ensure you have the correct versions:
```bash
pkg-config --modversion gtk4
pkg-config --modversion libadwaita-1
```
