# TODO: docs (BR: [ocaml-]odoc)
#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	OCaml binding to libuv: cross-platform asynchronous I/O
Summary(pl.UTF-8):	Wiązania OCamla do libuv - wieloplatformowego asynchronicznego we/wy
Name:		ocaml-luv
Version:	0.5.10
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/aantron/luv/releases
Source0:	https://github.com/aantron/luv/releases/download/%{version}/luv-%{version}.tar.gz
# Source0-md5:	583feee83bd0ff577ca8c59c3408b413
URL:		https://github.com/aantron/luv
BuildRequires:	libuv-devel
BuildRequires:	ocaml >= 1:4.02.0
BuildRequires:	ocaml-ctypes-devel >= 0.14.0
BuildRequires:	ocaml-dune >= 2.0.0
BuildRequires:	ocaml-result-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{without ocaml_opt}
%define		no_install_post_strip	1
# no opt means no native binary, stripping bytecode breaks such programs
%define		_enable_debug_packages	0
%endif

%description
Luv is a binding to libuv, the cross-platform C library that does
asynchronous I/O in Node.js and runs its main loop.

This package contains files needed to run bytecode executables using
luv library.

%description -l pl.UTF-8
Luv to wiązanie do libuv - wieloplatformowej biblioteki C,
odpowiadającej za asynchroniczne we/wy oraz głowną pętlę w Node.js.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających biblioteki luv.

%package devel
Summary:	OCaml binding to libuv - development part
Summary(pl.UTF-8):	Wiązania OCamla do libuv - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using luv
library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
biblioteki luv.

%prep
%setup -q -n luv-%{version}

%build
LUV_USE_SYSTEM_LIBUV=yes \
dune build --verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/luv/{,*/}*.ml
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/luv_unix/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/{luv,luv_unix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllluv_c_stubs.so
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllluv_unix_stubs.so
%dir %{_libdir}/ocaml/luv
%{_libdir}/ocaml/luv/META
%{_libdir}/ocaml/luv/*.cma
%dir %{_libdir}/ocaml/luv/c
%{_libdir}/ocaml/luv/c/*.cma
%dir %{_libdir}/ocaml/luv/c_function_descriptions
%{_libdir}/ocaml/luv/c_function_descriptions/*.cma
%dir %{_libdir}/ocaml/luv/c_type_descriptions
%{_libdir}/ocaml/luv/c_type_descriptions/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/luv/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/luv/c/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/luv/c_function_descriptions/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/luv/c_type_descriptions/*.cmxs
%endif
%dir %{_libdir}/ocaml/luv_unix
%{_libdir}/ocaml/luv_unix/META
%{_libdir}/ocaml/luv_unix/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/luv_unix/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/luv/dune-package
%{_libdir}/ocaml/luv/opam
%{_libdir}/ocaml/luv/*.cmi
%{_libdir}/ocaml/luv/*.cmt
%{_libdir}/ocaml/luv/*.cmti
%{_libdir}/ocaml/luv/*.mli
%{_libdir}/ocaml/luv/c/*.cmi
%{_libdir}/ocaml/luv/c/*.cmt
%{_libdir}/ocaml/luv/c_function_descriptions/*.cmi
%{_libdir}/ocaml/luv/c_function_descriptions/*.cmt
%{_libdir}/ocaml/luv/c_type_descriptions/*.cmi
%{_libdir}/ocaml/luv/c_type_descriptions/*.cmt
%if %{with ocaml_opt}
%{_libdir}/ocaml/luv/*.a
%{_libdir}/ocaml/luv/*.cmx
%{_libdir}/ocaml/luv/*.cmxa
%{_libdir}/ocaml/luv/c/*.a
%{_libdir}/ocaml/luv/c/*.cmx
%{_libdir}/ocaml/luv/c/*.cmxa
%{_libdir}/ocaml/luv/c_function_descriptions/*.a
%{_libdir}/ocaml/luv/c_function_descriptions/*.cmx
%{_libdir}/ocaml/luv/c_function_descriptions/*.cmxa
%{_libdir}/ocaml/luv/c_type_descriptions/*.a
%{_libdir}/ocaml/luv/c_type_descriptions/*.cmx
%{_libdir}/ocaml/luv/c_type_descriptions/*.cmxa
%endif
%{_libdir}/ocaml/luv_unix/dune-package
%{_libdir}/ocaml/luv_unix/opam
%{_libdir}/ocaml/luv_unix/*.cmi
%{_libdir}/ocaml/luv_unix/*.cmt
%{_libdir}/ocaml/luv_unix/*.cmti
%{_libdir}/ocaml/luv_unix/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/luv_unix/*.a
%{_libdir}/ocaml/luv_unix/*.cmx
%{_libdir}/ocaml/luv_unix/*.cmxa
%endif
