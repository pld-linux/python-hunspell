#
# Conditional build:
%bcond_with	doc		# don't build doc
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module

%define 	module	hunspell
Summary:	Pyhunspell is a set of Python bindings for the Hunspell spellchecker engine
Summary(pl.UTF-8):	Moduł interfejsu do słownika Hunspell
# Name must match the python module/package name (as in 'import' statement)
Name:		python-%{module}
Version:	0.2.1
Release:	1
License:	GPL
Group:		Libraries/Python
# https://pypi.python.org/packages/source/h/hunspell/hunspell-0.2.1.tar.gz#md5=a228fbbedad209fb7691abe6d46add53
Source0:	https://pypi.python.org/packages/source/h/hunspell/hunspell-%{version}.tar.gz
# Source0-md5:	a228fbbedad209fb7691abe6d46add53
Patch0:		%{name}-lib_fix.patch
URL:		http://github.com/blatinier/pyhunspell
BuildRequires:	hunspell-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219



%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pyhunspell is a set of Python bindings for the Hunspell spellchecker
engine. It lets developers load Hunspell dictionaries, check words,
get suggestions, add new words, etc. It also provides some basic
morphological analysis related methods

%description -l pl.UTF-8
Moduł interfejsu do słownika Hunspell. Pozwala załadować słowniki,
sprawdzać pisownie, uzyskać sugestie, dodawać słowa itp. Daje dostęp
do podstawowywch metod analizy morfologicznej.

%package -n python3-%{module}
Summary:	Pyhunspell is a set of Python bindings for the Hunspell spellchecker engine
Summary(pl.UTF-8):	Moduł interfejsu do słownika Hunspell
Group:		Libraries/Python

%description -n python3-%{module}

%description -n python3-%{module} -l pl.UTF-8

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
# fix #!%{_bindir}/env python -> #!%{_bindir}/python:
#%{__sed} -i -e '1s,^#!.*python,#!%{__python},' %{name}.py

%build
%if %{with python2}
# CC/CFLAGS is only for arch packages - remove on noarch packages
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
# CC/CFLAGS is only for arch packages - remove on noarch packages
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

# %if %{with doc}
# cd docs
# %{__make} -j1 html
# rm -rf _build/html/_sources
# %endif

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

# in case there are examples provided
#%if %{with python2}
#install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
#cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
#%endif
#%if %{with python3}
#install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
#cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
#find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
#	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
#%endif

# when files are installed in other way that standard 'setup.py
# they need to be (re-)compiled
## change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
#%%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
#%%py_comp $RPM_BUILD_ROOT%{py_sitedir}
#%%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
# %{py_sitedir}/*.py[co]
%attr(755,root,root) %{py_sitedir}/*.so
%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-*.egg-info
%endif
# %{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS CHANGES LICENSE
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
# %{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
# %doc docs/_build/html/*
%endif
