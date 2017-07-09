%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define major 1
%define libname	%mklibname volume_key %{major}
%define devname	%mklibname -d volume_key

Summary: An utility for manipulating storage encryption keys and passphrases
Name: volume_key
Version: 0.3.9
Release: 1
License: GPLv2
URL: https://pagure.io/volume_key/
Requires: %{libname} = %{EVRD}

Source0: https://releases.pagure.org/volume_key/volume_key-%{version}.tar.xz
# Upstream commit 04991fe8c4f77c4e5c7874c2db8ca32fb4655f6e
Patch1: volume_key-0.3.9-fips-crash.patch
# Upstream commit 8f8698aba19b501f01285e9eec5c18231fc6bcea
Patch2: volume_key-0.3.9-config.h.patch
Patch3:	volume_key-0.3.9-find_python.patch
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	gettext-devel
BuildRequires:	python-devel
BuildRequires:	nss-devel
BuildRequires:	gpgme-devel
BuildRequires:	pkgconfig(blkid)

%description
This package provides a command-line tool for manipulating storage volume
encryption keys and storing them separately from volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.


%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package provides libvolume_key, a library for manipulating storage volume
encryption keys and storing them separately from volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.

%package -n	%{libname}
Summary:	This package provides libvolume_key library
Group:		System/Libraries

%description -n	%{libname}
This package provides libvolume_key, a library for manipulating storage volume
encryption keys and storing them separately from volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.

%package -n python-volume_key
Summary: Python bindings for libvolume_key
Requires: %{libname} = %{version}-%{release}

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
%setup -q
%apply_patches

%build
%configure
%make

%install
%makeinstall_std

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
