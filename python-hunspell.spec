#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	hunspell
Summary:	Pyhunspell - Python 2.x bindings for the Hunspell spellchecker engine
Summary(pl.UTF-8):	Pyhunspell - wiązania Pythona 2.x do silnika sprawdzania pisowni Hunspell
Name:		python-%{module}
Version:	0.3.2
Release:	1
License:	LGPL v3+
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/h/hunspell/hunspell-%{version}.tar.gz
# Source0-md5:	39373430a1541618aea67d99d31d0ac8
Patch0:		%{name}-lib_fix.patch
URL:		http://github.com/blatinier/pyhunspell
BuildRequires:	hunspell-devel >= 1.3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with python2}
BuildRequires:	python-devel >= 2
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-distribute
BuildRequires:	python3-modules >= 1:3.2
%endif
Requires:	python-modules >= 2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pyhunspell is a set of Python bindings for the Hunspell spellchecker
engine. It lets developers load Hunspell dictionaries, check words,
get suggestions, add new words, etc. It also provides some basic
morphological analysis related methods.

%description -l pl.UTF-8
Pyhunspell to zbiór wiązań Pythona do silnika sprawdzania pisowni
Hunspell. Pozwala załadować słowniki, sprawdzać pisownię słów, uzyskać
sugestie, dodawać nowe słowa itp. Daje dostęp do podstawowywch metod
analizy morfologicznej.

%package -n python3-%{module}
Summary:	Pyhunspell - Python 3.x bindings for the Hunspell spellchecker engine
Summary(pl.UTF-8):	Pyhunspell - wiązania Pythona 3.x do silnika sprawdzania pisowni Hunspell
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
Pyhunspell is a set of Python bindings for the Hunspell spellchecker
engine. It lets developers load Hunspell dictionaries, check words,
get suggestions, add new words, etc. It also provides some basic
morphological analysis related methods

%description -n python3-%{module} -l pl.UTF-8
Moduł interfejsu do słownika Hunspell. Pozwala załadować słowniki,
sprawdzać pisownie, uzyskać sugestie, dodawać słowa itp. Daje dostęp
do podstawowywch metod analizy morfologicznej.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%if %{with python2}
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build \
	--build-base build-2
%endif

%if %{with python3}
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python3} setup.py build \
	--build-base build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{py_sitedir}/hunspell.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/hunspell-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{py3_sitedir}/hunspell.cpython-*.so
%{py3_sitedir}/hunspell-%{version}-py*.egg-info
%endif
