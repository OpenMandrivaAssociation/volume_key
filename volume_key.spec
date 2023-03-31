%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define major 1
%define libname %mklibname volume_key %{major}
%define devname %mklibname -d volume_key

Summary:	An utility for manipulating storage encryption keys and passphrases
Name:		volume_key
Version:	0.3.12
Release:	5
License:	GPLv2
URL:	https://pagure.io/volume_key/
Source0:	https://releases.pagure.org/volume_key/volume_key-%{version}.tar.gz
Patch0:		volume_key-0.3.12-support_LUKS2_and_more.patch
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(gpgme)
BuildRequires:	gnupg
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(libcryptsetup)
BuildRequires:	swig
Requires:	%{libname} = %{EVRD}

%description
This package provides a command-line tool for manipulating storage volume
encryption keys and storing them separately from volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package provides libvolume_key, a library for manipulating storage volume
encryption keys and storing them separately from volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.

%package -n %{libname}
Summary:	This package provides libvolume_key library
Group:		System/Libraries

%description -n %{libname}
This package provides libvolume_key, a library for manipulating storage volume
encryption keys and storing them separately from volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.

%package -n python-volume_key
Summary: Python bindings for libvolume_key
Requires: %{libname} = %{EVRD}

%description -n python-volume_key
This package provides Python bindings for libvolume_key, a library for
manipulating storage volume encryption keys and storing them separately from
volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.

volume_key currently supports only the LUKS volume encryption format.  Support
for other formats is possible, some formats are planned for future releases.

%prep
%autosetup -n %{name}-%{name}-%{version} -p1


sed -e 's/-lpython\$(PYTHON_VERSION)/-lpython%{python3_version}m/' -i Makefile.am
autoreconf -fiv

%build
export GPG_PATH=/usr/bin/gpg
%configure --with-python3
%make_build PYTHON_CFLAGS="$(pkg-config --cflags python3)"

%install
%make_install
rm -rf %{buildroot}%{python_sitearch}/__pycache__/

# Remove libtool archive
find %{buildroot} -type f -name "*.la" -delete

%find_lang volume_key

%files
%doc README contrib
%{_bindir}/volume_key
%{_mandir}/man8/volume_key.8*

%files -n %{devname} -f volume_key.lang
%doc AUTHORS COPYING ChangeLog NEWS
%{_includedir}/volume_key
%{_libdir}/libvolume_key.so

%files -n %{libname}
%{_libdir}/libvolume_key.so.%{major}*

%files -n python-volume_key
%{python_sitearch}/_volume_key.so
%{python_sitearch}/volume_key.py*
%{python_sitearch}/__pycache__/*.pyc
