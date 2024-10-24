{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.virtualenv  # Optional, if you want virtualenv
  ];

  shellHook = ''
    # Optionally set up a virtual environment
    if [ ! -d "env" ]; then
      virtualenv env
    fi
    source env/bin/activate
  '';
}

