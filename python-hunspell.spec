#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	hunspell
Summary:	Pyhunspell - Python 2.x bindings for the Hunspell spellchecker engine
Summary(pl.UTF-8):	Pyhunspell - wiązania Pythona 2.x do silnika sprawdzania pisowni Hunspell
Name:		python-%{module}
Version:	0.5.5
Release:	2
License:	LGPL v3+
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/hunspell/
Source0:	https://pypi.python.org/packages/source/h/hunspell/hunspell-%{version}.tar.gz
# Source0-md5:	90b3fdccca06893837b2aff3290e7456
URL:		https://github.com/blatinier/pyhunspell
BuildRequires:	hunspell-devel >= 1.7
BuildRequires:	pkgconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with python2}
BuildRequires:	python-devel >= 2
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools
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

hunspell_abi="$(pkg-config --modversion hunspell | cut -d. -f1-2)"
%{__sed} -i -e "/libraries/s/'hunspell'/'hunspell-${hunspell_abi}'/" setup.py

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/hunspell.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/hunspell-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/hunspell.cpython-*.so
%{py3_sitedir}/hunspell-%{version}-py*.egg-info
%endif
