Name:          volk
Version:       3.0.0
Release:       1
Summary:       The Vector Optimized Library of Kernels
License:       GPLv3+
URL:           https://github.com/gnuradio/%{name}
Source0:       %{name}-%{version}.tar.gz

BuildRequires: make
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: python3-devel
BuildRequires: python3-mako
BuildRequires: orc-devel
BuildRequires: sed
Conflicts:     python3-gnuradio < 3.9.0.0
Conflicts:     gnuradio-devel < 3.9.0.0

%description
VOLK is the Vector-Optimized Library of Kernels. It is a library that contains
kernels of hand-written SIMD code for different mathematical operations.
Since each SIMD architecture can be very different and no compiler has yet
come along to handle vectorization properly or highly efficiently, VOLK
approaches the problem differently. VOLK is a sub-project of GNU Radio.

%package devel
Summary:       Development files for VOLK
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

# fix shebangs
pushd python/volk_modtool
sed -i '1 {/#!\s*\/usr\/bin\/env\s\+python/ d}' __init__.py cfg.py
popd

%build
mkdir -p build
pushd build
# workaround, the code is not yet compatible with the strict-aliasing
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS="$CFLAGS"
%cmake ..
%make_build
popd

%install
pushd build
%make_install
popd

# drop list_cpu_features, not needed, just some demo binary,
# unavailable on s390x, for details see:
# https://github.com/gnuradio/volk/issues/442#issuecomment-772059840
rm -f %{buildroot}%{_bindir}/list_cpu_features

# drop static objects
rm -f %{buildroot}%{_libdir}/libcpu_features.a

%files
%license COPYING
%doc README.md docs/CHANGELOG.md
%{_bindir}/volk-config-info
%{_bindir}/volk_modtool
%{_bindir}/volk_profile
%{_libdir}/libvolk*.so.*
%{python3_sitearch}/volk_modtool

%files devel
%{_includedir}/volk
%ifnarch s390x
%{_includedir}/cpu_features
%{_libdir}/cmake/CpuFeatures
%endif
%{_libdir}/libvolk.so
%{_libdir}/cmake/volk
%{_libdir}/pkgconfig/*.pc
