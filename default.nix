let
  pkgs = import (builtins.fetchGit {
    url = "https://github.com/nixos/nixpkgs/";
    ref = "refs/heads/nixos-unstable";
    rev = "a64b73e07d4aa65cfcbda29ecf78eaf9e72e44bd"; # 9-06-2023
    # obtain via `git ls-remote https://github.com/nixos/nixpkgs nixos-unstable`
  }) { config = {}; };
  pythonPkgs = python-packages: with python-packages; [
    tasklib
    icalendar

    # TODO: split into dev and app
    pytest
    ptpython # nicer repl
  ];
  pythonCore = pkgs.python310;
  myPython = pythonCore.withPackages pythonPkgs;
in
pkgs.mkShell {
  buildInputs =
  with pkgs;
  [
    git
    gnumake
    myPython
    pyright
    ncftp
  ];
}
